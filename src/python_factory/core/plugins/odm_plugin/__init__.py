"""Oriented Data Model (ODM) plugin package."""

from typing import Any

from beanie import init_beanie  # type: ignore
from injector import Module, inject
from motor.motor_asyncio import AsyncIOMotorClient
from structlog.stdlib import BoundLogger, get_logger

from python_factory.core.protocols import BaseApplicationProtocol

from .configs import ODMConfig
from .providers import ODMPluginModule

_logger: BoundLogger = get_logger()

INJECTOR_MODULE: type[Module] = ODMPluginModule


def pre_conditions_check(application: BaseApplicationProtocol) -> bool:
    """Check the pre-conditions for the OpenTelemetry plugin.

    Args:
        application (BaseApplicationProtocol): The application.

    Returns:
        bool: True if the pre-conditions are met, False otherwise.
    """
    del application
    return True


@inject
def on_load(
    application: BaseApplicationProtocol,
) -> None:
    """Actions to perform on load for the OpenTelemetry plugin.

    Args:
        application (BaseApplicationProtocol): The application.
    """
    del application
    _logger.debug("ODM plugin loaded.")


@inject
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
    odm_config: ODMConfig = application.get_injector().get(ODMConfig)
    odm_client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(
        host=odm_config.mongo_uri,
    )

    application.get_injector().binder.bind(AsyncIOMotorClient, to=odm_client)

    await init_beanie(database=odm_client, document_models=[])  # type: ignore

    _logger.debug("ODM plugin started.")


async def on_shutdown(application: BaseApplicationProtocol) -> None:
    """Actions to perform on shutdown for the ODM plugin.

    Args:
        application (BaseApplicationProtocol): The application.

    Returns:
        None
    """
    database: AsyncIOMotorClient[Any] = application.get_injector().get(AsyncIOMotorClient)
    database.close()
    _logger.debug("ODM plugin shutdown.")
