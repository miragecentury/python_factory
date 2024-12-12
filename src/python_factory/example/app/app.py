"""Provides the concrete application class."""

from typing import ClassVar

from beanie import Document

from python_factory.core.app import BaseApplication
from python_factory.example.models.books.document import BookDocument

from .config import AppConfig


class App(BaseApplication):
    """Concrete application class."""

    PACKAGE_NAME: str = "python_factory.example"

    CONFIG_CLASS = AppConfig

    ODM_DOCUMENT_MODELS: ClassVar[list[type[Document]]] = [BookDocument]

    def __init__(self, config: AppConfig) -> None:
        """Instantiate the application with the configuration and the API router.

        Args:
            config (AppConfig): The application configuration.
        """
        super().__init__(config=config)

        # Prevent circular imports
        from ..api import api_router  # pylint: disable=import-outside-toplevel

        self.get_asgi_app().include_router(router=api_router)
