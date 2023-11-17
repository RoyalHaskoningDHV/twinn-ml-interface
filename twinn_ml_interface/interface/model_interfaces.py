from __future__ import annotations

from os import PathLike
from typing import (
    Any,
    Callable,
    runtime_checkable,
)

import pandas as pd
from annotation_protocol import AnnotationProtocol

from twinn_ml_interface.objectmodels import (
    Configuration,
    DataLabelConfigTemplate,
    DataLevel,
    InputData,
    MetaDataLogger,
    ModelCategory,
    PredictionType,
    UnitTag,
    UnitTagTemplate,
)

Logs = dict[str, Any]


@runtime_checkable
class ModelInterfaceV4(AnnotationProtocol):
    model_type_name: str
    # Model category is based on the output of the model.
    model_category: ModelCategory
    # Number between (-inf, inf) indicating the model performance.
    performance_value: float
    # Features used to train the model. If not supplied, equal to get_data_config_template().
    base_features: dict[DataLevel, list[UnitTag]] | None
    # This is only needed when get_target_tag_template returns UnitTagTemplate
    target: UnitTag | None = None

    @staticmethod
    def get_target_template() -> UnitTagTemplate | UnitTag:
        """Get the UnitTag that will be the target of the model.

        Returns:
            UnitTagTemplate | UnitTag: The unit tag of the model target,
            either as template or as literal.
        """
        ...

    @staticmethod
    def get_data_config_template() -> list[DataLabelConfigTemplate] | list[UnitTag]:
        """The specification of data needed to train and predict with the model.

        Result:
            list[DataLabelConfigTemplate] | list[UnitTag]: The data needed to train and
                predict with the model, either as template or as list of literals.
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
    def get_train_window_finder_config_template() -> list[DataLabelConfigTemplate] | None:
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
    ) -> dict[PredictionType, tuple[bool, str | None]]:
        """Validate if input data is usable for training.

        Args:
            data (InputData): Training data.

        Returns:
            dict[PredictionType, tuple[bool, str | None]]: For each PredictionType you get
                bool: Whether the data can be used for training. Default always true.
                str: Additional information about the window.
        """
        return True, "Input data is valid."

    def train(self, input_data: InputData, **kwargs) -> None:
        """Train a model.

        Args:
            input_data (InputData): Preprocessed and validated training data.

        Returns:
            dict[str, Any] | None: Optionally some logs collected during training.
        """
        ...

    def predict(self, input_data: InputData, **kwargs) -> list[pd.DataFrame]:
        """Run a prediction with a trained model.

        Args:
            input_data (InputData): Prediction data.

        Returns:
            list[pd.DataFrame]: List of dataframes with predictions
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

    @classmethod
    def load(cls, foldername: PathLike, filename: str) -> Callable:
        """
        Reads the following files:
        * prefix.pkl
        * prefix.h5
        from the folder given by foldername.
        Output is an entire instance of the fitted model that was saved

        Args:
            foldername (PathLike): configurable folder name
            filename (str): name of the file

        Returns:
            Model class with everything (except data) contained within to call the
            `predict()` method
        """
        ...
