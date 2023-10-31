from functools import cached_property
from typing import Any, Protocol


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
    def unit_properties(self) -> dict[Any, dict[str, Any]]:
        """Get and cache the ."""
        ...

    @cached_property
    def unit_hierarchies(self) -> dict[str, list[str]]:
        """Get and cache the ."""
        ...

    @cached_property
    def tenant_config(self) -> dict[str, Any]:
        """Get and cache the tenant_config."""
        ...
