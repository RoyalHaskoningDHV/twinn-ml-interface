from .configuration import Configuration
from .exceptions import (
    BaseError,
    MessageType,
    ModelException,
    construct_model_exception_text,
)
from .hierarchy import (
    AvailabilityLevel,
    DataLabelConfigTemplate,
    DataLevel,
    LabelConfig,
    LogLevel,
    ModelCategory,
    RelativeType,
    Tag,
    Unit,
    UnitTag,
    UnitTagTemplate,
)
from .logging import MetaDataLogger, Metric
from .model_flags import (
    FeatureQualityOption,
    PredictionType,
    PreprocessingMode,
    TrainWindowSizePriority,
)

WindowViability = dict[PredictionType, tuple[bool, str | None]]

__all__ = [
    "construct_model_exception_text",
    "MessageType",
    "BaseError",
    "ModelException",
    "AvailabilityLevel",
    "Configuration",
    "DataConfigTemplate",
    "DataLabelConfigTemplate",
    "DataLevel",
    "LabelConfig",
    "LogLevel",
    "FeatureQualityOption",
    "ModelCategory",
    "MetaDataLogger",
    "Metric",
    "PredictionType",
    "PreprocessingMode",
    "RelativeType",
    "Tag",
    "TrainWindowSizePriority",
    "Unit",
    "UnitTag",
    "UnitTagTemplate",
    "WindowViability",
]
