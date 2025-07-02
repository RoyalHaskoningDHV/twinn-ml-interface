from __future__ import annotations

from os import PathLike
from typing import runtime_checkable

import pandas as pd
from annotation_protocol import AnnotationProtocol

from twinn_ml_interface.input_data import InputData
from twinn_ml_interface.objectmodels import (
    Configuration,
    DataLabelConfigTemplate,
    DataLevel,
    MetaDataLogger,
    ModelCategory,
    PredictionType,
    TrainWindowSizePriority,
    UnitTag,
    UnitTagTemplate,
    WindowViability,
)


@runtime_checkable
class ModelInterfaceV4(AnnotationProtocol):
    # Unique name for each model class.
    model_type_name: str
    # Model category is based on the output of the model.
    model_category: ModelCategory
    # Features used to train the model. If not supplied, equal to get_data_config_template().
    base_features: dict[DataLevel, list[UnitTag]] | None
    # This is only needed when get_target_tag_template returns UnitTagTemplate
    target: str | None = None

    @staticmethod
    def get_target_template() -> UnitTagTemplate | UnitTag:
        """Get the UnitTag that will be the target of the model.

        Returns:
            UnitTagTemplate | UnitTag: The unit tag of the model target,
            either as template or as literal.
        """
        ...

    @staticmethod
    def get_data_config_template() -> list[DataLabelConfigTemplate]:
        """The specification of data needed to train and predict with the model.

        Result:
            list[DataLabelConfigTemplate]: The data needed to train and
                predict with the model.
        """
        ...

    @staticmethod
    def get_result_template() -> UnitTagTemplate | UnitTag:
        """The UnitTag to post the predictions/results on.

        Returns:
            UnitTagTemplate, UnitTag: The unit tag of the model's output, either as
                template or as literal.
        """
        ...

    @staticmethod
    def get_train_window_finder_config_template() -> (
        tuple[list[DataLabelConfigTemplate], TrainWindowSizePriority] | None
    ):
        """The config for running the train window finder.

        Returns:
            list[DataLabelConfigTemplate] | None: a template for getting the tags needed to run
                the train window finder. Defaults to None, then no train window finder will be
                used.
        """
        return None

    @classmethod
    def initialize(cls, configuration: Configuration, logger: MetaDataLogger) -> ModelInterfaceV4:
        """Post init function to pass metadata logger and some config to the model.

        Args:
            configuration (Configuration): an API-like object to retrieve configuration.
            logger (MetaDataLogger): A MetaDataLogger object to write logs to MLflow later.
        """
        ...

    def preprocess(self, input_data: InputData) -> InputData:
        """Preprocess input data before training.

        Args:
            data (InputData): Input data.

        Returns:
            InputData: Preprocessed input data.

        """
        return input_data

    def validate_input_data(
        self,
        input_data: InputData,
    ) -> WindowViability:
        """Validate if input data is usable for training.

        Args:
            data (InputData): Training data.

        Returns:
            WindowViability: For each PredictionType you get
                bool: Whether the data can be used for training. Default always true.
                str: Additional information about the window.
        """
        return {PredictionType.ML: (True, None)}

    def train(self, input_data: InputData, **kwargs) -> tuple[float, object]:
        """Train a model.

        Args:
            input_data (InputData): Preprocessed and validated training data.

        Returns:
            float: Number between (-inf, inf) indicating the model performance
            object: Any other object that can be used for testing. This object will be ignored
                by the infrastructure
        """
        ...

    def predict(self, input_data: InputData, **kwargs) -> tuple[list[pd.DataFrame], object]:
        """Run a prediction with a trained model.

        Args:
            input_data (InputData): Prediction data.

        Returns:
            list[pd.DataFrame]: List of dataframes with predictions
            object: Any other object that can be used for testing. This object will be ignored
                by the infrastructure
        """
        ...

    def dump(self, foldername: PathLike, filename: str) -> None:
        """
        Writes the following files:
        * prefix.pkl
        * prefix.h5
        to the folder given by foldername.

        Args:
            foldername (PathLike): configurable folder name
            filename (str): name of the file
        """
        return None

    @staticmethod
    def load(
        foldername: PathLike, filename: str, configuration: Configuration, logger: MetaDataLogger
    ) -> ModelInterfaceV4:
        """
        Reads the following files:
        * prefix.pkl
        * prefix.h5
        from the folder given by foldername.
        Output is an entire instance of the fitted model that was saved.
        Just as with `initialize`, configuration and logger are passed for you to use.

        Args:
            foldername (PathLike): configurable folder name
            filename (str): name of the file
            configuration (Configuration): an API-like object to retrieve configuration.
            logger (MetaDataLogger): A MetaDataLogger object to write logs to MLflow later.

        Returns:
            Model class with everything (except data) contained within to call the
            `predict()` method
        """
        ...
