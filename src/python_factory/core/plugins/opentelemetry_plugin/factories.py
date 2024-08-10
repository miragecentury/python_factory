"""
Provides a factory function to build a objets for OpenTelemetry.
"""

import injector
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
