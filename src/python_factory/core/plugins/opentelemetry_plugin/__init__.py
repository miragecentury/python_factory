"""OpenTelemetry Plugin Module."""

from injector import Module

from python_factory.core.protocols import BaseApplicationProtocol

from .configs import OpenTelemetryConfig
from .exceptions import OpenTelemetryPluginBaseException, OpenTelemetryPluginConfigError
from .providers import OpenTelemetryPluginModule

__all__: list[str] = [
    "OpenTelemetryConfig",
    "OpenTelemetryPluginBaseException",
    "OpenTelemetryPluginConfigError",
    "OpenTelemetryPluginModule",
]

INJECTOR_MODULE: type[Module] = OpenTelemetryPluginModule


def pre_conditions_check(application: BaseApplicationProtocol) -> bool:
    """Check the pre-conditions for the OpenTelemetry plugin.

    Args:
        application (BaseApplicationProtocol): The application.

    Returns:
        bool: True if the pre-conditions are met, False otherwise.
    """
    del application
    return True


@inject
async def on_startup(
    application: BaseApplicationProtocol,
) -> None:
    """Actions to perform on startup for the OpenTelemetry plugin.

    Args:
        application (BaseApplicationProtocol): The application.

    Returns:
        None
    """
    del application


async def on_shutdown(application: BaseApplicationProtocol) -> None:
    """Actions to perform on shutdown for the OpenTelemetry plugin.

    Args:
        application (BaseApplicationProtocol): The application.

    Returns:
        None
    """
    del application
