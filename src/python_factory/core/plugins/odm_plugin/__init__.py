"""Oriented Data Model (ODM) plugin package."""

from typing import Any

from beanie import init_beanie  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient
from structlog.stdlib import BoundLogger, get_logger

from python_factory.core.protocols import BaseApplicationProtocol

from .builder import ODMBuilder

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
    del application
    _logger.debug("ODM plugin loaded.")


async def on_startup(
    application: BaseApplicationProtocol,
) -> None:
    """Actions to perform on startup for the ODM plugin.

    Args:
        application (BaseApplicationProtocol): The application.
        odm_config (ODMConfig): The ODM configuration.

    Returns:
        None
    """
    odm_factory: ODMBuilder = ODMBuilder(application=application)
    odm_factory.build_odm_config()
    odm_factory.build_client()
    odm_factory.build_database()
    # TODO: Find a way to add type to the state
    application.get_asgi_app().state.odm_client = odm_factory.odm_client
    application.get_asgi_app().state.odm_database = odm_factory.odm_database

    # TODO: Find a better way to initialize beanie with the document models of the concrete application
    # through an hook in the application ?
    await init_beanie(
        database=odm_factory.odm_database,
        document_models=application.odm_document_models,  # type: ignore
    )

    _logger.debug(
        f"ODM plugin started. Database: {odm_factory.odm_database.name} - "  # type: ignore
        f"Client: {odm_factory.odm_client.address} - "  # type: ignore
        f"Document models: {application.odm_document_models}"
    )  # type: ignore


async def on_shutdown(application: BaseApplicationProtocol) -> None:
    """Actions to perform on shutdown for the ODM plugin.

    Args:
        application (BaseApplicationProtocol): The application.

    Returns:
        None
    """
    client: AsyncIOMotorClient[Any] = application.get_asgi_app().state.odm_client
    client.close()
    _logger.debug("ODM plugin shutdown.")
