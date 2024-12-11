"""Test cases for the health endpoint."""

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

_logger = get_logger(__package__)


class TestApiV1SysHealth(TestExampleClassParent):
    """Test the health endpoint."""

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_api_v1_sys_health(self, async_motor_database: AsyncIOMotorDatabase[Any]) -> None:
        """Test the get_api_v1_sys_health function."""
        await async_motor_database.client.server_info()
        hostname, port = async_motor_database.client.address

        with patch.dict(
            os.environ,
            {"MONGO_URI": f"mongodb://{hostname}:{port!s}"},
        ):
            with TestClient(app=self.application_factory_for_test()) as client:
                response: Response = client.get(url="/api/v1/sys/health")
                assert response.status_code == HTTPStatus.OK.value
                assert response.json() == {"status": "healthy"}
                assert response.json() == {"status": "healthy"}
