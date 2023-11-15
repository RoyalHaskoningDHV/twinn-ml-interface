from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class PreprocessingMode(Enum):
    DEFAULT = auto()
    TRAIN = auto()
    PREDICT = auto()


class PredictionType(AutoName):
    ML = auto()
    SPC = auto()


class FeatureQualityOption(AutoName):
    STORE = auto()
    APPLY = auto()
    STORE_APPLY = auto()
    IGNORE = auto()


class TrainWindowSizePriority(AutoName):
    MIN = auto()
    MAX = auto()
