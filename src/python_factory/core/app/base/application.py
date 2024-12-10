"""Provides the abstract class for the application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import ClassVar, cast

import starlette.types
from beanie import Document
from fastapi import FastAPI

from python_factory.core.api import api

from .config_abstract import AppConfigAbstract
from .fastapi_application_abstract import FastAPIAbstract
from .plugins_manager_abstract import ApplicationPluginManagerAbstract


class BaseApplication(FastAPIAbstract, ApplicationPluginManagerAbstract):
    """Application abstract class."""

    PACKAGE_NAME: str = ""

    odm_document_models: ClassVar[list[type[Document]]] = []

    def __init__(self, config: AppConfigAbstract) -> None:
        """Instanciate the application.

        Args:
            config (AppConfigAbstract): The application configuration.

        Returns:
            None

        Raises:
            ValueError: If the package name is not set.
        """
        if self.PACKAGE_NAME == "":
            raise ValueError("The package name must be set in the concrete application class.")

        self._config: AppConfigAbstract = config
        FastAPIAbstract.__init__(
            self=cast(FastAPIAbstract, self),
            config=self._config,
            api_router=api,
            lifespan=cast(starlette.types.StatelessLifespan[starlette.types.ASGIApp], self.fastapi_lifespan),
        )
        ApplicationPluginManagerAbstract.__init__(self=cast(ApplicationPluginManagerAbstract, self))
        self._on_load()

    @asynccontextmanager
    async def fastapi_lifespan(self, fastapi_application: FastAPI) -> AsyncGenerator[None, None]:
        """Provide the lifespan context manager for FastAPI.

        Args:
            fastapi_application (FastAPI): The FastAPI application.

        Returns:
            AsyncGenerator[None]: The lifespan context manager.
        """
        del fastapi_application
        await self.plugins_on_startup()
        yield
        await self.plugins_on_shutdown()

    def get_config(self) -> AppConfigAbstract:
        """Get the application configuration."""
        return self._config
