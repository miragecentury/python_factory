"""Test cases for the health endpoint."""

from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response
from units.python_factory.example import TestExampleClassParent


class TestApiV1SysHealth(TestExampleClassParent):
    """Test the health endpoint."""

    def test_get_api_v1_sys_health(self) -> None:
        """Test the get_api_v1_sys_health function."""
        with TestClient(app=self.application_factory_for_test()) as client:
            response: Response = client.get(url="/api/v1/sys/health")

            assert response.status_code == HTTPStatus.OK.value
            assert response.json() == {"status": "healthy"}
            assert response.json() == {"status": "healthy"}
