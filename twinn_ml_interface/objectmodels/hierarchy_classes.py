from dataclasses import dataclass
from datetime import timedelta
from enum import Enum, IntEnum, auto
from typing import Callable

from .model_flags import TrainWindowSizePriority
from .unit_tags import TagType, UNIT_TAG_LOOKUP


class ModelCategory(Enum):
    anomaly = "anomaly"
    prediction = "prediction"
    actual = "actual"


class DataLevels(Enum):
    sensor_data = "data"
    downsampled_sensor_data = "downsampleddata"
    weather = "weather"
    availability = "availability"
    predictions = "predictions"
    anomalies = "anomalies"

    # This is needed to check equality with copies of this class.
    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if other.__class__.__name__ == self.__class__.__name__:
            return self.value == other.value and self.name == other.name
        return False


class AvailabilityLevels(IntEnum):
    """Availability levels.

    Enum for different possibilities for unit availability
    all: don't filter on unit availability
    only_available: filter on unit availability (only return available data)
    show_available: don't filter on unit availability but include availability tag
    available_until_now: filter on availability and discard if the last datapoint is
        unavailable or if the unavailable interval is in the future
    """

    all = auto()
    only_available = auto()
    show_available = auto()
    available_until_now = auto()

    # This is needed to check equality with copies of this class.
    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if other.__class__.__name__ == self.__class__.__name__:
            return self.value == other.value and self.name == other.name
        return False


class RelativeType(Enum):
    PARENT = auto()
    CHILDREN = auto()
    SELF = auto()


@dataclass
class Unit:
    unit_code: str
    unit_type_code: str
    active: bool
    name: str | None = None
    unit_type_name: str | None = None
    geometry: dict[str, list[float]] | None = None
    properties: list | None = None
    metadata: dict | None = None

    def __hash__(self):
        return hash(self.unit_code)

    def __eq__(self, other):
        if isinstance(other, Unit):
            return self.unit_code == other.unit_code
        return NotImplemented


@dataclass
class UnitTagLiteral:
    unit_code: str
    tag_name: str

    def __hash__(self):
        return hash(f"{self.unit_code}:{self.tag_name}")

    def __str__(self) -> str:
        return f"{self.unit_code}:{self.tag_name}"


@dataclass
class UnitTag:
    unit: Unit
    tag: TagType

    def __str__(self) -> str:
        unit_tag_lookup = UNIT_TAG_LOOKUP[self.tag]
        if self.unit.unit_type_code not in unit_tag_lookup:
            raise KeyError(f"{self.unit.unit_type_code} does not exist in lookup.")

        tag = unit_tag_lookup[self.unit.unit_type_code]
        return f"{self.unit.unit_code}:{tag}"

    def __hash__(self):
        return hash(f"{self.unit}:{self.tag.name}")

    def __eq__(self, other):
        if isinstance(other, UnitTag):
            return self.unit == other.unit
        return NotImplemented


@dataclass
class UnitTagTemplate:
    relative_path: list[RelativeType]
    tags: list[TagType]


class LogLevel(Enum):
    ALL = auto()  # noqa: A003
    TARGET = auto()
    NO_LOG = auto()


@dataclass
class LabelConfig:
    log_level: LogLevel | None = None
    labeling_pipelines: list[str] | None = None
    labels_to_use: list[str] | None = None


@dataclass
class DataLabelConfigTemplate:
    data_level: DataLevels
    unit_tag_templates: list[UnitTagTemplate]
    availability_level: AvailabilityLevels
    desired_tag_number: int | None = None
    label_config: LabelConfig | None = None
    max_lookback: timedelta | None = None
    train_window_size_priority: TrainWindowSizePriority = TrainWindowSizePriority.MAX

    def f(*args, **kwargs):
        return args[0]

    transform: Callable = f


@dataclass
class Node:
    val: Unit
    parent = None
    children: list | None = None