"""Provides the concrete application class."""

from typing import ClassVar

from beanie import Document

from python_factory.core.app import BaseApplication
from python_factory.core.app.base.exceptions import ApplicationConfigFactoryException
from python_factory.core.utils.configs import (
    UnableToReadConfigFileError,
    ValueErrorConfigError,
    build_config_from_file_in_package,
)
from python_factory.example.models.books.document import BookDocument

from .config import AppConfig


class App(BaseApplication):
    """Concrete application class."""

    PACKAGE_NAME: str = "python_factory.example"

    odm_document_models: ClassVar[list[type[Document]]] = [BookDocument]

    def __init__(self, config: AppConfig) -> None:
        """Instanciate the application with the configuration and the API router.

        Args:
            config (AppConfig): The application configuration.
        """
        super().__init__(config=config)

        # Prevent circular imports
        from ..api import api_router  # pylint: disable=import-outside-toplevel

        self.get_asgi_app().include_router(router=api_router)


def config_factory() -> AppConfig:
    """Provides the configuration factory."""
    try:
        config: AppConfig = build_config_from_file_in_package(
            package_name=App.PACKAGE_NAME,
            config_class=AppConfig,
            filename="application.yaml",
            yaml_base_key="application",
        )
    except UnableToReadConfigFileError as exception:
        raise ApplicationConfigFactoryException("Unable to read the application configuration file.") from exception
    except ValueErrorConfigError as exception:
        raise ApplicationConfigFactoryException("Unable to create the application configuration model.") from exception

    return config


def factory_for_app(app_config: AppConfig | None = None) -> App:
    """Provides the application factory.

    TODO: Move this to core and transform it into a generic factory.
    Args will be the application class and the module class.
    """
    if app_config is None:
        app_config = config_factory()
    application: App = App(config=app_config)

    return application
