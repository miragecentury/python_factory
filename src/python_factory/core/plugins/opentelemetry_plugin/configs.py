"""Provides the configuration model for the OpenTelemetry plugin."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, UrlConstraints
from pydantic_core import Url


class OpenTelemetryMeterConfig(BaseModel):
    """Provides the configuration model for the OpenTelemetry meter as sub-model."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    reader_interval_millis: float = Field(
        default=60000,
        description="The interval in miliseconds to read and export metrics.",
    )

    reader_timeout_millis: float = Field(
        default=1000,
        description="The timeout in miliseconds for the reader.",
    )


class OpenTelemetryTracerConfig(BaseModel):
    """Provides the configuration model for the OpenTelemetry tracer as sub-model."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    max_queue_size: int = Field(
        default=2048,
        description="The maximum queue size for the tracer.",
    )
    max_export_batch_size: int = Field(
        default=512,
        description="The maximum export batch size for the tracer.",
    )
    schedule_delay_millis: int = Field(
        default=5000,
        description="The schedule delay in miliseconds for the tracer.",
    )
    export_timeout_millis: int = Field(
        default=30000,
        description="The export timeout in miliseconds for the tracer.",
    )


class OpenTelemetryConfig(BaseModel):
    """Provides the configuration model for the OpenTelemetry plugin."""

    COLLECTOR_ENDPOINT_DEFAULT: str = "http://localhost:4317"

    model_config = ConfigDict(frozen=True, extra="forbid")

    activate: bool = Field(
        default=False,
        description="Whether to activate the OpenTelemetry collector export.",
    )
    endpoint: Annotated[Url, UrlConstraints(allowed_schemes=["http", "https"])] = Field(
        default=Url(url=COLLECTOR_ENDPOINT_DEFAULT),
        description="The collector endpoint.",
    )

    timeout: int = Field(
        default=10,
        description="The timeout in seconds for the collector.",
    )

    closing_timeout: int = Field(
        default=10,
        description="The closing timeout in seconds for the collector.",
    )

    meter_config: OpenTelemetryMeterConfig | None = Field(
        default_factory=OpenTelemetryMeterConfig,
        description="The meter configuration.",
    )

    tracer_config: OpenTelemetryTracerConfig | None = Field(
        default_factory=OpenTelemetryTracerConfig,
        description="The tracer configuration.",
    )

    excluded_urls: list[str] = Field(
        default_factory=list,
        description="The excluded URLs for both the metrics and traces.",
    )
