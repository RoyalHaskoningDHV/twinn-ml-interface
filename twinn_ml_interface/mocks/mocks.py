import os
from copy import deepcopy
from dataclasses import dataclass
from functools import cached_property
from typing import Any

import pandas as pd

from twinn_ml_interface.input_data import InputData
from twinn_ml_interface.interface import ModelInterfaceV4
from twinn_ml_interface.objectmodels import (
    Configuration,
    MetaDataLogger,
    RelativeType,
    Unit,
    UnitTag,
    UnitTagTemplate,
)


@dataclass
class LocalConfig:
    """Class for configuring model adhering to ModelInterfaceV4"""

    model: ModelInterfaceV4
    train_data_path: os.PathLike
    prediction_data_path: os.PathLike
    model_path: os.PathLike
    model_name: str
    predictions_path: os.PathLike = "/my/path/predictions/predictions.parquet"


class ConfigurationMock:
    """Mock to get information from hierarchy (rooted tree) and tenant."""

    def __init__(self, target_name, modelled_unit_code, unit_properties, units, unit_tags) -> None:
        self._modelled_unit_code = modelled_unit_code
        self._target_name = target_name
        self._unit_properties = unit_properties
        self._units = units
        self._unit_tags = unit_tags

    @cached_property
    def target_name(self) -> str:
        return self._target_name

    @property
    def modelled_unit_code(self) -> str:
        return self._modelled_unit_code

    @cached_property
    def tenant_config(self) -> dict[str, Any]:
        return

    @property
    def tenant(self) -> dict[str, Any]:
        return

    def get_unit_properties(self, unit_name: str) -> dict[str, Any] | None:
        return self._unit_properties[unit_name] if unit_name in self._unit_properties else {}

    def get_units(self, unit_name: str, relative_path: list[RelativeType]) -> list[Unit] | None:
        return self._units

    def get_unit_tags(self, unit_name: str, unit_tag_template: UnitTagTemplate) -> list[UnitTag]:
        return self._unit_tags


class ExecutorMock:
    """A mock executor, that mimics some of the behaviour of a real executor.

    An executor is responsible for running a machine learning model during training
    or predicting based on a `ModelInterfaceV4` compliant class in the `darrow-ml-platform`.

    This mock executor performs both training and predicting, but only locally. Not all
    aspects of a real executor are mocked, but the basic logic flow should be the same.
    """

    metadata_logger = MetaDataLogger()

    def __init__(self, local_config: LocalConfig, infra_config: Configuration = None):
        self.local_config = local_config
        self.original_config = (
            infra_config if infra_config is not None else ConfigurationMock("", "", {}, [], [])
        )

    def _init_train(self) -> tuple[ModelInterfaceV4, Configuration]:
        model_class = self.local_config.model
        return model_class, deepcopy(self.original_config)

    def get_training_data(
        self,
        model: ModelInterfaceV4,
        infra_config: Configuration | None = None,
    ) -> InputData:
        """Get training data input for ML model

        Args:
            model (ModelInterfaceV4): ML model
            infra_config (Configuration | None, optional): Used to get info from hierarchy
                and tenant

        Returns:
            InputData: Input data for ML model
        """
        long_data = pd.read_parquet(self.local_config.train_data_path)
        return InputData.from_long_df(long_data)

    def _write_model(self, model: ModelInterfaceV4) -> None:
        # When running the model in our infra, we store all the logs and then we reset the
        # cache before dumping the model. This means that MetaDataLogger contents won't be
        # available when loading the model for predictions
        self.metadata_logger.reset_cache()
        model.dump(self.local_config.model_path, self.local_config.model_name)

    def _postprocess_model_results(self, model: ModelInterfaceV4, performance_value: float):
        # Store base features and performance value. Base features are needed to trigger
        # predictions if DataLabelConfigTemplate contains templates and not specific units
        model.base_features

    def write_results(self, model: ModelInterfaceV4, performance_value: float):
        """Save model to file.

        Args:
            model (ModelInterfaceV4): _description_
        """
        self._write_model(model=model)
        self._postprocess_model_results(model=model, performance_value=performance_value)

    def run_train_flow(self):
        """Run training flow and cache trained model"""
        model_class, infra_config = self._init_train()
        model = model_class.initialize(infra_config, self.metadata_logger)

        input_data = self.get_training_data(model, infra_config)
        preprocessed_data = model.preprocess(input_data)
        performance_value, _ = model.train(preprocessed_data)

        self.write_results(model, performance_value)

    def load_model(
        self,
        model_class: ModelInterfaceV4,
        infra_config: Configuration,
        metadata_logger: MetaDataLogger,
    ) -> ModelInterfaceV4:
        """Load saved ML model

        Args:
            model_class (ModelInterfaceV4): Name of the model class
            infra_config (Configuration): Infrastructure configuration
            metadata_logger (MetaDataLogger): New logger used for predictions

        Returns:
            ModelInterfaceV4: ML model
        """
        return model_class.load(
            self.local_config.model_path,
            self.local_config.model_name,
            infra_config,
            metadata_logger,
        )

    def get_prediction_data(self) -> InputData:
        """Get input data for predicting

        Returns:
            InputData: Input data for ML model
        """
        long_data = pd.read_parquet(self.local_config.prediction_data_path)
        return InputData.from_long_df(long_data)

    def write_predictions(self, predictions: list[pd.DataFrame]):
        """Write predictions to local path. When running the actual infrastructure,
        predictions are uploaded to the azure data lake.

        Args:
            predictions (pd.DataFrame): Predictions made by ML Model
        """
        for prediction in predictions:
            # Predictions are overwritten in the mock for demonstration purposes
            prediction.to_parquet(self.local_config.predictions_path)

    def run_predict_flow(self):
        """Run predict flow"""
        infra_config = deepcopy(self.original_config)
        metadata_logger = (
            MetaDataLogger()
        )  # New instance of the logger, information from training is not available
        model: ModelInterfaceV4 = self.load_model(
            self.local_config.model, infra_config, metadata_logger
        )

        input_data = self.get_prediction_data()
        preprocessed_data = model.preprocess(input_data)
        predictions, _ = model.predict(preprocessed_data)
        self.write_predictions(predictions)

    def run_full_flow(self):
        """Run both train and predict flows"""
        self.run_train_flow()
        self.run_predict_flow()
