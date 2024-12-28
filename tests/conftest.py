"""Cong Test."""

import asyncio
import logging
import os
from collections.abc import AsyncGenerator, Generator
from typing import Any
from uuid import uuid4

import pytest
from mirakuru import TCPExecutor
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pytest_mongo import factories
from structlog.stdlib import get_logger

from python_factory.core.utils.log import LoggingConfig, LogModeEnum, setup_log

setup_log(mode=LogModeEnum.CONSOLE)

_logger = get_logger(__package__)

CONNECTION_TIMEOUT: int = 100
SOCKET_TIMEOUT: int = 300

mongodb_with_flexible_executable = factories.mongo_proc(
    executable=os.getenv("MONGO_EXECUTABLE", "/usr/bin/mongod"),
)

setup_log(
    mode=LogModeEnum.CONSOLE,
    log_level="DEBUG",
    logging_config=[
        LoggingConfig(
            name="pymongo",
            level=logging.INFO,
        )
    ],
)


@pytest.fixture(scope="session")
def database_for_function(
    mongodb_with_flexible_executable: TCPExecutor,  # pylint: disable=redefined-outer-name
) -> Generator[TCPExecutor, None, None]:
    """Cleanup the database.

    Args:
        mongodb_with_flexible_executable (TCPExecutor): The TCP executor for mongodb server.

    """
    yield mongodb_with_flexible_executable
    mongodb_with_flexible_executable.stop()


@pytest.fixture(scope="function")  # pyright: ignore
async def async_motor_database(
    database_for_function: TCPExecutor,  # pylint: disable=redefined-outer-name
) -> AsyncGenerator[AsyncIOMotorDatabase[Any], None]:
    """Create an async motor database.

    Args:
        database_for_function (TCPExecutor): The TCP executor for mongodb server.

    Yields:
        Generator[AsyncIOMotorDatabase, None, None]: The async motor database.

    """
    _logger.debug(
        f"Creating AsyncIOMotorDatabase with " f"{database_for_function.host=} and " f"{database_for_function.port=}"
    )
    client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(
        host=f"mongodb://{database_for_function.host}:{database_for_function.port}",
        serverMonitoringMode="stream",  # prevent error on teardown of the client
        connectTimeoutMS=CONNECTION_TIMEOUT,
        socketTimeoutMS=SOCKET_TIMEOUT,
        timeoutMS=SOCKET_TIMEOUT,
        serverSelectionTimeoutMS=CONNECTION_TIMEOUT,
    )
    database_name = str(uuid4())
    database: AsyncIOMotorDatabase[Any] = client.get_database(name=database_name)

    try:
        yield database
    finally:
        await client.drop_database(name_or_database=database_name)
        client.close()
        # Pymongo does not cleanely close the connection
        # the monitoring stream is still running
        # and need time to close nicely
        # so we wait a bit to prevent the exception and log message
        await asyncio.sleep(0.3)
