"""Test cases for the health endpoint."""

from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from python_factory.example import application_factory


class TestApiV1SysHealth:
    """Test the health endpoint."""

    def test_get_api_v1_sys_health(self) -> None:
        """Test the get_api_v1_sys_health function."""
        with TestClient(app=application_factory()) as client:
            response: Response = client.get(url="/api/v1/sys/health")

            assert response.status_code == HTTPStatus.OK.value
            assert response.json() == {"status": "healthy"}
            assert response.json() == {"status": "healthy"}
