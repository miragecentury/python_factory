"""Oriented Data Model (ODM) plugin package."""

from typing import Any

from beanie import init_beanie  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from structlog.stdlib import BoundLogger, get_logger

from python_factory.core.protocols import BaseApplicationProtocol

from .configs import ODMConfig
from .providers import ODMPluginModule

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
    odm_config: ODMConfig = ODMPluginModule().odm_config(application)
    odm_client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(
        host=odm_config.mongo_uri,
    )
    odm_database: AsyncIOMotorDatabase[Any] = odm_client.get_database(name=odm_config.mongo_database)

    application.get_asgi_app().state.odm_client = odm_client
    application.get_asgi_app().state.odm_database = odm_database

    await init_beanie(database=odm_database, document_models=[])  # type: ignore

    _logger.debug("ODM plugin started.")


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
