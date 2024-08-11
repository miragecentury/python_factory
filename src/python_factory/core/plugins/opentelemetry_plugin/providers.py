"""
Provides a factory function to build a objets for OpenTelemetry.
"""

from typing import Any

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
from python_factory.core.plugins.opentelemetry_plugin.configs import (
    OpenTelemetryMeterConfig,
    OpenTelemetryTracerConfig,
)
from python_factory.core.utils.importlib import get_path_file_in_package
from python_factory.core.utils.yaml_reader import (
    UnableToReadYamlFileError,
    YamlFileReader,
)

from .configs import OpenTelemetryConfig
from .exceptions import OpenTelemetryPluginConfigError


class OpenTelemetryPluginModule(injector.Module):
    """
    Configure the injection bindings for OpenTelemetryPlugin.
    """

    @injector.singleton
    @injector.provider
    def resource_factory(
        self, application: injector.Inject[BaseApplication]
    ) -> Resource:
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

    @injector.singleton
    @injector.provider
    def meter_provider_factory(
        self,
        resource: injector.Inject[Resource],
        opentelemetry_config: injector.Inject[OpenTelemetryConfig],
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
        meter_config: OpenTelemetryMeterConfig = opentelemetry_config.meter_config
        reader = PeriodicExportingMetricReader(
            exporter=exporter,
            export_interval_millis=meter_config.reader_interval_millis,
            export_timeout_millis=meter_config.reader_timeout_millis,
        )

        # Setup the Meter Provider
        return MeterProvider(
            resource=resource,
            metric_readers=[reader],
            shutdown_on_exit=True,
            views=[],
        )

    @injector.singleton
    @injector.provider
    def tracer_provider_factory(
        self,
        resource: injector.Inject[Resource],
        opentelemetry_config: injector.Inject[OpenTelemetryConfig],
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
        tracer_config: OpenTelemetryTracerConfig = opentelemetry_config.tracer_config
        span_processor = BatchSpanProcessor(
            span_exporter=exporter,
            max_queue_size=tracer_config.max_queue_size,
            max_export_batch_size=tracer_config.max_export_batch_size,
            schedule_delay_millis=tracer_config.schedule_delay_millis,
            export_timeout_millis=tracer_config.export_timeout_millis,
        )

        # Setup the Multi Span Processor
        synchronous_multi_span_processor = SynchronousMultiSpanProcessor()
        synchronous_multi_span_processor.add_span_processor(
            span_processor=span_processor
        )

        # Setup the Tracer Provider
        return TracerProvider(
            sampler=None,
            resource=resource,
            active_span_processor=synchronous_multi_span_processor,
            id_generator=None,
            span_limits=None,
            shutdown_on_exit=True,
        )

    @injector.singleton
    @injector.provider
    def provider_open_telemetry_config(
        self,
        base_application: injector.Inject["BaseApplication"],
    ) -> OpenTelemetryConfig:

        if base_application.PACKAGE_NAME == "":
            raise OpenTelemetryPluginConfigError(
                "The package name must be set in the concrete application class."
            )

        # Read the application configuration file
        try:
            yaml_file_content: dict[str, Any] = YamlFileReader(
                file_path=get_path_file_in_package(
                    filename="application.yaml",
                    package=base_application.PACKAGE_NAME,
                ),
                yaml_base_key="opentelemetry",
                use_environment_injection=True,
            ).read()
        except (FileNotFoundError, ImportError, UnableToReadYamlFileError) as exception:
            raise OpenTelemetryPluginConfigError(
                "Unable to read the application configuration file."
            ) from exception

        # Create the application configuration model
        try:
            config = OpenTelemetryConfig(**yaml_file_content)
        except ValueError as exception:
            raise OpenTelemetryPluginConfigError(
                "Unable to create the application configuration model."
            ) from exception

        return config
