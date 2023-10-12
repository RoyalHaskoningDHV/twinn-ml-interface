from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    runtime_checkable,
    Tuple,
    Union,
)

import pandas as pd
from mlflow.entities import Run

from objectmodels import (
    ModelCategory,
    DataLabelConfigTemplate,
    DataLevels,
    InputData,
    RelativeType,
    TagType,
    UnitTagTemplate,
    UnitTagLiteral,
    AnnotationProtocol,
)

Logs: Dict[str, Any]


@runtime_checkable
class ModelInterfaceV4(AnnotationProtocol):

    # The name of the model type.
    model_type_name: str
    # Model category is based on the output of the model.
    model_category: ModelCategory
    # Number between (-inf, inf) indicating the model performance.
    performance_value: float
    # List of features used to train the model. If not supplied, equal to data_config().
    train_data_config: Optional[Dict[DataLevels, List]]

    @property
    def target_tag() -> Union[UnitTagTemplate, UnitTagLiteral]:
        """Get the name of the target tag to train the model.

        Returns:
            Union[UnitTagTemplate, UnitTagLiteral]: The unit tag of the model target, either as template or as literal.
        """
        ...

    @property
    def data_config() -> Union[List[DataLabelConfigTemplate], List[UnitTagLiteral]]:
        """The specification of data needed to train and predict with the model.

        Result:
            Union[List[DataLabelConfigTemplate], List[UnitTagLiteral]]: The data needed to train and predict with the model,
                either as template or as list of literals.
        """
        ...

    @property
    def result_tag() -> Union[UnitTagTemplate, UnitTagLiteral]:
        """The tag to post the predictions/results on.

        Returns:
           Union[UnitTagTemplate, UnitTagLiteral]: The unit tag of the model's output, either as template or as literal.
        """
        ...

    @property
    def unit_properties_template() -> List[TagType]:
        """Unit properties to get from the units specified in data_config.

        Returns:
            List[TagType]: The tags to request.
        """
        return []

    @property
    def unit_hierarchy_template() -> Dict[str, List[RelativeType]]:
        """Request some units from the hierarchy in a dictionary.

        Returns:
            Dict[str, List[RelativeType]]: An identifier for the units to get, and their relative path from the target unit.
        """
        return {}

    @property
    def train_window_finder_config_template() -> Optional[List[DataLabelConfigTemplate]]:
        """The config for running the train window finder.

        Returns:
            List[DataLabelConfigTemplate], optional: a template for getting the tags needed to run the train window
                finder. Defaults to None, then no train window finder will be used.
        """
        return None

    def initialize(mlflow_run: Run, tenant_config: Dict[str, Any]) -> None:
        """Post init function to pass some config to the model.

        Args:
            mlflow_run (Run): A MLflow run object to write logs to MLflow.
            tenant_config (Dict[str, Any]]): Tenant specific configuration.
        """

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
    ) -> Tuple[bool, str]:
        """Validate if input data is usable for training.

        Args:
            data (InputData): Training data.

        Returns:
            bool: Whether the data can be used for training. Default always true.
            str: Additional information about the window.
        """
        return True, "Input data is valid."

    def train(self, input_data: InputData, **kwargs) -> Optional[Logs]:
        """Train a model.

        Args:
            input_data (InputData): Preprocessed and validated training data.

        Returns:
            Optional[Logs]: Optionally some logs collected during training.
        """
        ...

    def predict(self, input_data: InputData, **kwargs) -> Tuple[List[pd.DataFrame], Optional[Logs]]:
        """Run a prediction with a trained model.

        Args:
            input_data (InputData): Prediction data.

        Returns:
            Tuple[List[pd.DataFrame], Optional[Logs]]: Dataframe of predictions and optionally some logs collected during prediction.
        """
        ...

    def dump(self, foldername: str, prefix: str) -> None:
        """
        Writes the following files:
        * prefix.pkl
        * prefix.h5
        to the folder given by foldername.

        Args:
            foldername (str): configurable folder name
            prefix (str): configurable prefix of the file
        """
        return None

    @classmethod
    def load(cls, foldername: str, prefix: str) -> Callable:
        """
        Reads the following files:
        * prefix.pkl
        * prefix.h5
        from the folder given by foldername.
        Output is an entire instance of the fitted model that was saved

        Returns:
            Model class with everything (except data) contained within to call the
            `predict()` method
        """
        ...
