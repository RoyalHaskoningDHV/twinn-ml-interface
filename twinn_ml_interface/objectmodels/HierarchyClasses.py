from dataclasses import dataclass
from datetime import timedelta
from enum import Enum, IntEnum, auto
from typing import Callable, Dict, List, Optional

from .UnitTags import TagType, UNIT_TAG_LOOKUP


class ModelCategory(Enum):
    anomaly = "anomaly"
    prediction = "prediction"
    actual = "actual"


class DataLevels(Enum):
    sensor_data = "data"
    downsampled_sensor_data = "downsampleddata"
    weather = "weather"

    # This class is copied to avoid circular imports. This is needed to check equality with copies of this class.
    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if other.__class__.__name__ == self.__class__.__name__:
            return self.value == other.value and self.name == other.name
        return False


class AvailabilityLevels(IntEnum):
    all = auto()
    only_available = auto()
    show_available = auto()

    # This class is copied to avoid circular imports. This is needed to check equality with copies of this class.
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
    name: Optional[str] = None
    unit_type_name: Optional[str] = None
    geometry: Optional[Dict] = None
    properties: Optional[List] = None
    metadata: Optional[Dict] = None

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
    relative_path: List[RelativeType]
    tags: List[TagType]


@dataclass
class DataLabelConfigTemplate:
    data_level: DataLevels
    unit_tag_templates: List[UnitTagTemplate]
    availability_level: AvailabilityLevels
    desired_tag_number: Optional[int] = None
    labeling_pipelines: Optional[List[str]] = None
    max_lookback: Optional[timedelta] = None

    def f(*args, **kwargs):
        return args[0]

    transform: Callable = f


@dataclass
class Node:
    val: Unit
    parent = None
    children: Optional[List] = None
