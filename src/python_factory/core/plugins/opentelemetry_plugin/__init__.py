"""OpenTelemetry Plugin Module."""

import asyncio

from opentelemetry.instrumentation.fastapi import (  # pyright: ignore[reportMissingTypeStubs]
    FastAPIInstrumentor,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
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


def pre_conditions_check(application: BaseApplicationProtocol) -> bool:
    """Check the pre-conditions for the OpenTelemetry plugin.

    Args:
        application (BaseApplicationProtocol): The application.

    Returns:
        bool: True if the pre-conditions are met, False otherwise.
    """
    del application
    return True


def on_load(
    application: BaseApplicationProtocol,
) -> None:
    """Actions to perform on load for the OpenTelemetry plugin.

    Args:
        application (BaseApplicationProtocol): The application.
    """
    otel_config: OpenTelemetryConfig = OpenTelemetryPluginModule().provider_open_telemetry_config(application)
    resource: Resource = OpenTelemetryPluginModule().resource_factory(application)
    tracer_provider: TracerProvider = OpenTelemetryPluginModule().tracer_provider_factory(
        resource=resource, opentelemetry_config=otel_config
    )
    meter_provider: MeterProvider = OpenTelemetryPluginModule().meter_provider_factory(
        resource=resource, opentelemetry_config=otel_config
    )

    application.get_asgi_app().state.tracer_provider = tracer_provider
    application.get_asgi_app().state.meter_provider = meter_provider
    application.get_asgi_app().state.otel_config = otel_config
    FastAPIInstrumentor.instrument_app(  # pyright: ignore[reportUnknownMemberType]
        app=application.get_asgi_app(),
        tracer_provider=tracer_provider,
        meter_provider=meter_provider,
        excluded_urls=otel_config.excluded_urls,
    )

    _logger.debug("OpenTelemetry plugin loaded.")


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
    tracer_provider: TracerProvider = application.get_asgi_app().state.tracer_provider
    meter_provider: MeterProvider = application.get_asgi_app().state.meter_provider
    otel_config: OpenTelemetryConfig = application.get_asgi_app().state.otel_config

    seconds_to_ms_multiplier: int = 1000

    async def close_tracer_provider() -> None:
        """Close the tracer provider."""
        tracer_provider.force_flush(timeout_millis=otel_config.closing_timeout * seconds_to_ms_multiplier)
        # No Delay for the shutdown of the tracer provider
        tracer_provider.shutdown()

    async def close_meter_provider() -> None:
        """Close the meter provider.

        Split the timeout in half for the flush and shutdown.
        """
        meter_provider.force_flush(timeout_millis=int(otel_config.closing_timeout / 2) * seconds_to_ms_multiplier)
        meter_provider.shutdown(timeout_millis=int(otel_config.closing_timeout / 2) * seconds_to_ms_multiplier)

    _logger.debug("OpenTelemetry plugin stop requested. Flushing and closing...")

    await asyncio.gather(
        close_tracer_provider(),
        close_meter_provider(),
    )

    _logger.debug("OpenTelemetry plugin closed.")
