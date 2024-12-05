"""Cong Test."""

from collections.abc import AsyncGenerator
from typing import Any
from uuid import uuid4

import pytest
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient


@pytest.fixture(scope="function")  # pyright: ignore
async def async_motor_database(mongodb: MongoClient[Any]) -> AsyncGenerator[AsyncIOMotorDatabase[Any], None]:
    """Create an async motor database.

    Args:
        mongodb (MongoClient): The MongoDB client.

    Yields:
        Generator[AsyncIOMotorDatabase, None, None]: The async motor database.

    """
    client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(
        host=f"mongodb://{mongodb.HOST}:{mongodb.PORT}",
        serverMonitoringMode="stream",  # prevent error on teardown of the client
    )
    database_name = str(uuid4())
    database: AsyncIOMotorDatabase[Any] = client.get_database(name=database_name)

    try:
        yield database
    finally:
        await client.drop_database(name_or_database=database_name)
        client.close()
