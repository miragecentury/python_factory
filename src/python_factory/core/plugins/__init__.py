"""Package for plugins."""

from enum import StrEnum, auto

from .protocols import PluginProtocol


class PluginsEnum(StrEnum):
    """Enumeration for the plugins."""

    OPENTELEMETRY_PLUGIN = auto()


__all__: list[str] = [
    "PluginsEnum",
    "PluginProtocol",
]
