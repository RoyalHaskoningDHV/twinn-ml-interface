from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from enum import Enum, IntEnum, auto
from typing import Any


# Whether the model outputs anomalies, predictions or actuals.
# This determines the format in which the results are expected
class ModelCategory(Enum):
    ANOMALY = "anomaly"
    PREDICTION = "prediction"
    ACTUAL = "actual"


class DataLevel(str, Enum):
    SENSOR = "actuals"
    DOWNSAMPLED_SENSOR = "downsampled_sensor"
    WEATHER = "weather"
    AVAILABILITY = "availability"
    PREDICTION = "prediction"
    ANOMALY = "anomaly"
    LABEL = "label"


class AvailabilityLevel(IntEnum):
    """Availability levels.

    Enum for different possibilities for unit availability
    ALL: don't filter on unit availability
    FILTER: filter on unit availability (only return available data)
    ADD_COLUMN: don't filter on unit availability but include availability tag
    FILTER_UNTIL_NOW: filter on availability and discard if the last datapoint is
        unavailable or if the unavailable interval is in the future
    """

    ALL = auto()
    FILTER = auto()
    ADD_COLUMN = auto()
    FILTER_UNTIL_NOW = auto()


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
    properties: dict[str, Any] | None = None
    metadata: dict | None = None

    def __hash__(self):
        return hash(self.unit_code)

    def __eq__(self, other):
        if isinstance(other, Unit):
            return self.unit_code == other.unit_code
        return NotImplemented


@dataclass
class Tag:
    """The tag denotes a timeseries of the unit.

    Args:
        name (str | None): name of the tag if literal, None if mapping is used.
        mapping (dict[str, str] | None): a mapping with unit_type as key and
            the corresponding tag as value. Defaults to None.
    """

    name: str | None = None
    mapping: dict[str, str] | None = None

    def __post_init__(self):
        if (self.name is not None and self.mapping) or (self.name is None and not self.mapping):
            raise ValueError(
                "Exactly one of name or mapping must be set, but not both or neither."
            )

    def to_string(self, unit_type_code: str | None = None):
        if self.name:
            return self.name

        if not self.mapping or not unit_type_code or unit_type_code not in self.mapping:
            msg = f"Couldn't find {unit_type_code=} in {self.mapping}"
            raise LookupError(msg)

        return self.mapping[unit_type_code]

    def __hash__(self) -> int:
        if self.name is not None:
            return hash(self.name)
        return hash(frozenset(self.mapping.items()))


@dataclass
class UnitTag:
    unit: Unit
    tag: Tag

    @classmethod
    def from_string(cls, unit_tag: str, separator: str = ":") -> UnitTag:
        unit, tag = unit_tag.split(separator)
        return cls(Unit(unit, "UNKNOWN", True), Tag(tag))

    def __str__(self) -> str:
        return f"{self.unit.unit_code}:{self.tag.to_string(self.unit.unit_type_code)}"

    def __hash__(self):
        return hash(self.__str__())


@dataclass
class UnitTagTemplate:
    relative_path: list[RelativeType]
    tags: list[Tag]


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
    data_level: DataLevel
    unit_tag_templates: list[UnitTagTemplate] | list[UnitTag]
    availability_level: AvailabilityLevel = AvailabilityLevel.ALL
    desired_tag_number: int | None = None
    label_config: LabelConfig | None = None
    max_lookback: timedelta | None = None
    horizon: timedelta | None = None
