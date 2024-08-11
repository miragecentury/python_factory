"""
Provides a factory function to build a objets for OpenTelemetry.
"""

import injector
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    MetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import (
    DEPLOYMENT_ENVIRONMENT,
    SERVICE_NAME,
    SERVICE_NAMESPACE,
    SERVICE_VERSION,
    Resource,
)

from python_factory.core.app.base.application import BaseApplication


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


def metric_exporter_factory() -> MetricExporter:
    """
    Build a metric exporter object for OpenTelemetry.

    Returns:
        MetricExporter: The metric exporter object for OpenTelemetry.
    """
    return OTLPMetricExporter()


def periodic_exporting_metric_reader_factory(
    metric_exporter: MetricExporter,
) -> PeriodicExportingMetricReader:
    """
    Build a periodic exporting metric reader object for OpenTelemetry.

    Returns:
        PeriodicExportingMetricReader: The periodic exporting metric reader object
        for OpenTelemetry.
    """
    return PeriodicExportingMetricReader(
        exporter=metric_exporter,
    )


def meter_provider_factory(
    resource: Resource,
    metric_reader: PeriodicExportingMetricReader,
) -> MeterProvider:
    """
    Build a meter provider object for OpenTelemetry.

    Args:
        resource (Resource): The resource object for OpenTelemetry.
        metric_reader (PeriodicExportingMetricReader): The periodic exporting
        metric reader object for OpenTelemetry.

    Returns:
        MeterProvider: The meter provider object for OpenTelemetry.
    """
    return MeterProvider(
        resource=resource,
        metric_readers=[metric_reader],
    )
