from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class TagType(AutoName):
    ...


# To add custom tagtypes, extend by subclass like this.
class ProductTagType(TagType):
    PRODUCT_TAG_1 = auto()
    PRODUCT_TAG_2 = auto()
