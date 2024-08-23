"""Tests for the routes of the books API."""

from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response
from units.python_factory.example import TestExampleClassParent

from python_factory.example.app.app import App


class TestBooksRoutes(TestExampleClassParent):
    """Tests for the routes of the books API."""

    def test_get_books(self) -> None:
        """Test get_books."""
        application: App = self.application_factory_for_test()

        with TestClient(application) as client:
            response: Response = client.get("/api/v1/books")
            assert response.status_code == HTTPStatus.OK
