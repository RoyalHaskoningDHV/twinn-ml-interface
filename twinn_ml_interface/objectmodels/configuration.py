from functools import cached_property
from typing import Any, Protocol

from .hierarchy_classes import Tag, UnitTag, UnitTagTemplate, RelativeType, Unit


class Configuration(Protocol):
    @cached_property
    def target_name(self) -> str:
        """Retrieve the target of the model in format UNIT_CODE:TAG_NAME.

        The InputData will have a corresponding column with this name."""
        ...

    @property
    def tenant(self) -> dict[str, Any]:
        ...

    @cached_property
    def unit_properties(self) -> dict[Tag, dict[str, Any]]:
        """Get and cache the unit_properties."""
        ...

    @cached_property
    def unit_hierarchies(self) -> dict[str, list[str]]:
        """Get and cache the unit_hierarchies."""
        ...

    @cached_property
    def tenant_config(self) -> dict[str, Any]:
        """Get and cache the tenant_config."""
        ...

    def get_unit_properties(self, unit_name: str) -> list[Any] | None:
        """Retrieve the property of a certain unit.

        Args:
            unit_name (str): name of the unit to get properties for.

        Returns:
            list[Any] | None: the property of the UnitTag if it exists.
        """
        ...

    def get_units(self, unit_name: str, relative_path: list[RelativeType]) -> list[Unit] | None:
        """Retrieve units from the hierarchy.

        Args:
            unit_name (str): name of the unit to search from.
            relative_path (list[RelativeType]): a path to search for relative to the given unit.

        Returns:
            list[Unit] | None: the units.
        """

    def get_unit_tags(self, unit_name: str, unit_tag_template: UnitTagTemplate) -> list[UnitTag]:
        """Retrieve UnitTags from the hierarchy.

        Args:
            unit_name (str): name of the unit to search from.
            unit_tag_template (UnitTagTemplate): a relative path from the given unit.

        Returns:
            list[UnitTag]: the UnitTags that were found.
                You can easily convert them to strings by calling str() on them.
        """
        ...
