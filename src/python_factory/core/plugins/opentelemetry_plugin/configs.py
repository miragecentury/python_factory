"""
Provides the configuration model for the OpenTelemetry plugin.
"""

from typing import Annotated

from pydantic import BaseModel, Field, UrlConstraints
from pydantic_core import Url


class OpenTelemetryConfig(BaseModel):

    COLLECTOR_ENDPOINT_DEFAULT: str = "http://localhost:4317"

    collector_export_activate: bool = Field(
        default=False,
        description="Whether to activate the OpenTelemetry collector export.",
    )
    collector_export_endpoint: Annotated[
        Url, UrlConstraints(allowed_schemes=["http", "https"])
    ] = Field(
        default=Url(url=COLLECTOR_ENDPOINT_DEFAULT),
        description="The collector endpoint.",
    )
