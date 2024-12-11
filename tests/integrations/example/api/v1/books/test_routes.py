"""Tests for the routes of the books API."""

import os
from http import HTTPStatus
from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from httpx import Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from structlog.stdlib import get_logger
from units.python_factory.example import TestExampleClassParent

from python_factory.example.app.app import App

_logger = get_logger(__package__)


class TestBooksRoutes(TestExampleClassParent):
    """Tests for the routes of the books API."""

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_books(self, async_motor_database: AsyncIOMotorDatabase[Any]) -> None:
        """Test get_books."""
        await async_motor_database.client.server_info()
        hostname, port = async_motor_database.client.address

        with patch.dict(
            os.environ,
            {"MONGO_URI": f"mongodb://{hostname}:{port!s}"},
        ):
            _logger.debug(f"MONGO_URI={os.getenv('MONGO_URI')}")
            application: App = self.application_factory_for_test()

            with TestClient(application) as client:
                response: Response = client.get("/api/v1/books")
                assert response.status_code == HTTPStatus.OK
