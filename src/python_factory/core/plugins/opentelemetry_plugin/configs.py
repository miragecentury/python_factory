"""
Provides the configuration model for the OpenTelemetry plugin.
"""

from typing import Annotated

from pydantic import BaseModel
from pydantic.networks import Url, UrlConstraints


class OpenTelemetryConfig(BaseModel):

    COLLECTOR_ENDPOINT_DEFAULT = "http://localhost:4317"

    collector_endpoint: Annotated[
        Url, UrlConstraints(allowed_schemes=["http", "https"])
    ] = Url(COLLECTOR_ENDPOINT_DEFAULT)
