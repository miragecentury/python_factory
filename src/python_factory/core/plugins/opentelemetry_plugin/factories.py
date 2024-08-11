"""
Provides a factory function to build a objets for OpenTelemetry.
"""

import injector
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import (
    DEPLOYMENT_ENVIRONMENT,
    SERVICE_NAME,
    SERVICE_NAMESPACE,
    SERVICE_VERSION,
    Resource,
)
from opentelemetry.sdk.trace import SynchronousMultiSpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from python_factory.core.app.base.application import BaseApplication

from .configs import OpenTelemetryConfig
from .exceptions import OpenTelemetryPluginConfigError


def resource_factory(application: injector.Inject[BaseApplication]) -> Resource:
    """
    Build a resource object for OpenTelemetry
    from the application and it's configuration.

    Args:
        application (BaseApplication): The application object.

    Returns:
        Resource: The resource object for OpenTelemetry.
    """

    return Resource(
        attributes={
            DEPLOYMENT_ENVIRONMENT: application.get_config().environment.value,
            SERVICE_NAME: application.get_config().service_name,
            SERVICE_NAMESPACE: application.get_config().service_namespace,
            SERVICE_VERSION: application.get_config().version,
        }
    )


def meter_provider_factory(
    resource: Resource,
    opentelemetry_config: OpenTelemetryConfig,
) -> MeterProvider:
    """
    Build a meter provider object for OpenTelemetry

    Args:
        resource (Resource): The resource object for OpenTelemetry.
        opentelemetry_config (OpenTelemetryConfig): The configuration object
        for OpenTelemetry.

    Returns:
        MeterProvider: The meter provider object for OpenTelemetry.
    """

    # Exit with a void MeterProvider if the export is not activated
    if opentelemetry_config.activate is False:
        return MeterProvider(
            resource=resource,
            metric_readers=[],
            shutdown_on_exit=True,
            views=[],
        )

    if opentelemetry_config.meter_config is None:
        # TODO: switch to a custom exception
        raise OpenTelemetryPluginConfigError("The meter configuration is missing.")

    # Setup the Exporter
    exporter = OTLPMetricExporter(
        endpoint=opentelemetry_config.endpoint.unicode_string(),
        timeout=opentelemetry_config.timeout,
    )

    # Setup the Metric Reader
    reader = PeriodicExportingMetricReader(
        exporter=exporter,
        export_interval_millis=opentelemetry_config.meter_config.reader_interval_millis,
        export_timeout_millis=opentelemetry_config.meter_config.reader_timeout_millis,
    )

    # Setup the Meter Provider
    return MeterProvider(
        resource=resource,
        metric_readers=[reader],
        shutdown_on_exit=True,
        views=[],
    )


def tracer_provider_factory(
    resource: Resource,
    opentelemetry_config: OpenTelemetryConfig,
) -> TracerProvider:
    """
    Provides a tracer provider for OpenTelemetry.

    Args:
        resource (Resource): The resource object for OpenTelemetry.
        opentelemetry_config (OpenTelemetryConfig): The configuration object
        for OpenTelemetry.

    Returns:
        TracerProvider: The tracer provider object for OpenTelemetry.
    """

    # Exit with a void TracerProvider if the export is not activated
    if opentelemetry_config.activate is False:
        return TracerProvider(
            resource=resource,
            sampler=None,
            id_generator=None,
            active_span_processor=None,
            shutdown_on_exit=True,
            span_limits=None,
        )

    if opentelemetry_config.tracer_config is None:
        raise OpenTelemetryPluginConfigError("The tracer configuration is missing.")

    # Setup the Exporter
    exporter = OTLPSpanExporter(
        endpoint=opentelemetry_config.endpoint.unicode_string(),
        timeout=opentelemetry_config.timeout,
    )

    # Setup the Span Processor
    span_processor = BatchSpanProcessor(
        span_exporter=exporter,
        max_queue_size=opentelemetry_config.tracer_config.max_queue_size,
        max_export_batch_size=opentelemetry_config.tracer_config.max_export_batch_size,
        schedule_delay_millis=opentelemetry_config.tracer_config.schedule_delay_millis,
        export_timeout_millis=opentelemetry_config.tracer_config.export_timeout_millis,
    )

    # Setup the Multi Span Processor
    synchronous_multi_span_processor = SynchronousMultiSpanProcessor()
    synchronous_multi_span_processor.add_span_processor(span_processor=span_processor)

    # Setup the Tracer Provider
    return TracerProvider(
        sampler=None,
        resource=resource,
        active_span_processor=synchronous_multi_span_processor,
        id_generator=None,
        span_limits=None,
        shutdown_on_exit=True,
    )
