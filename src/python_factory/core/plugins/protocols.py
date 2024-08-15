"""
Defines the protocols for the plugins.
"""

from typing import Protocol, runtime_checkable

from injector import Module

from python_factory.core.app.base.protocols import BaseApplicationProtocol


@runtime_checkable
class PluginProtocol(Protocol):
    """
    Defines the protocol for the plugin.
    """

    INJECTOR_MODULE: type[Module]

    def pre_conditions_check(self, application: BaseApplicationProtocol) -> bool:
        """
        Check the pre-conditions for the plugin.
        """
        raise NotImplementedError

    async def on_startup(self, application: BaseApplicationProtocol) -> None:
        """
        The actions to perform on startup for the plugin.
        """
        raise NotImplementedError

    async def on_shutdown(self, application: BaseApplicationProtocol) -> None:
        """
        The actions to perform on shutdown for the plugin.
        """
        raise NotImplementedError
