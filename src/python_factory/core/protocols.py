"""Protocols for the base application."""

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from fastapi import FastAPI

if TYPE_CHECKING:
    from python_factory.core.app.base.config_abstract import AppConfigAbstract


class BaseApplicationProtocol(Protocol):
    """Protocol for the base application."""

    PACKAGE_NAME: str

    def get_config(self) -> "AppConfigAbstract":
        """Get the application configuration."""
        raise NotImplementedError

    def get_asgi_app(self) -> FastAPI:
        """Get the ASGI application."""
        raise NotImplementedError


@runtime_checkable
class PluginProtocol(Protocol):
    """Defines the protocol for the plugin.

    Attributes:
        INJECTOR_MODULE (type[Module]): The module for the plugin.

    """

    def pre_conditions_check(self, application: BaseApplicationProtocol) -> bool:
        """Check the pre-conditions for the plugin.

        Args:
            application (BaseApplicationProtocol): The application.

        Returns:
            bool: True if the pre-conditions are met, False otherwise.
        """
        raise NotImplementedError

    def on_load(self, application: BaseApplicationProtocol) -> None:
        """The actions to perform on load for the plugin.

        Args:
            application (BaseApplicationProtocol): The application.

        Returns:
            None
        """
        raise NotImplementedError

    async def on_startup(self, application: BaseApplicationProtocol) -> None:
        """The actions to perform on startup for the plugin.

        Args:
            application (BaseApplicationProtocol): The application.

        Returns:
            None
        """
        raise NotImplementedError

    async def on_shutdown(self, application: BaseApplicationProtocol) -> None:
        """The actions to perform on shutdown for the plugin.

        Args:
            application (BaseApplicationProtocol): The application.

        Returns:
            None
        """
        raise NotImplementedError
