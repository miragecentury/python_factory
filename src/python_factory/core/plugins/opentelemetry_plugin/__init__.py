"""OpenTelemetry Plugin Module."""

from injector import Module, inject
from opentelemetry.instrumentation.fastapi import (  # pyright: ignore[reportMissingTypeStubs]
    FastAPIInstrumentor,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider
from structlog.stdlib import BoundLogger, get_logger

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

_logger: BoundLogger = get_logger()

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
def on_load(
    application: BaseApplicationProtocol,
) -> None:
    """Actions to perform on load for the OpenTelemetry plugin.

    Args:
        application (BaseApplicationProtocol): The application.
    """
    tracer_provider: TracerProvider = application.get_injector().get(TracerProvider)
    meter_provider: MeterProvider = application.get_injector().get(MeterProvider)
    FastAPIInstrumentor.instrument_app(  # pyright: ignore[reportUnknownMemberType]
        app=application.get_asgi_app(),
        tracer_provider=tracer_provider,
        meter_provider=meter_provider,
    )

    _logger.debug("OpenTelemetry plugin loaded.")


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
    _logger.debug("OpenTelemetry plugin started.")


async def on_shutdown(application: BaseApplicationProtocol) -> None:
    """Actions to perform on shutdown for the OpenTelemetry plugin.

    Args:
        application (BaseApplicationProtocol): The application.

    Returns:
        None
    """
    del application
    _logger.debug("OpenTelemetry plugin stopped.")
