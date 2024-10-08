"""Provides utilities for the application."""

import uvicorn
import uvicorn.server

from python_factory.core.utils.log import clean_uvicorn_logger

from .base import AppConfigAbstract, BaseApplication


class UvicornUtils:
    """Provides utilities for Uvicorn."""

    def __init__(self, app: BaseApplication, config: AppConfigAbstract) -> None:
        """Instanticate the factory.

        Args:
            app (BaseApplication): The application.
            config (AppConfigAbstract): The application configuration.

        Returns:
            None
        """
        self._app: BaseApplication = app
        self._config: AppConfigAbstract = config

    def build_uvicorn_config(self) -> uvicorn.Config:
        """Build the Uvicorn configuration.

        Returns:
            uvicorn.Config: The Uvicorn configuration.
        """
        config = uvicorn.Config(
            app=self._app.get_asgi_app(),
            host=self._config.host,
            port=self._config.port,
            reload=self._config.reload,
            workers=self._config.workers,
        )
        clean_uvicorn_logger()
        return config

    def serve(self) -> None:
        """Serve the application."""
        config: uvicorn.Config = self.build_uvicorn_config()
        server: uvicorn.Server = uvicorn.Server(config=config)
        server.run()
