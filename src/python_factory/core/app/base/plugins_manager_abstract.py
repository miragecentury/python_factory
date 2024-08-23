"""Plugins manager abstract module."""

from abc import ABC
from importlib import import_module
from types import ModuleType
from typing import cast

from pydantic import BaseModel, ConfigDict, Field

from python_factory.core.plugins import PluginsEnum
from python_factory.core.protocols import BaseApplicationProtocol, PluginProtocol
from python_factory.core.utils.configs import (
    UnableToReadConfigFileError,
    ValueErrorConfigError,
    build_config_from_file_in_package,
)

from .exceptions import ApplicationPluginManagerException


class PluginsActivationList(BaseModel):
    """Model for the plugins activation list."""

    model_config = ConfigDict(extra="forbid")

    activate: list[PluginsEnum] = Field(default=list())


class ApplicationPluginManagerAbstract(ABC):
    """Abstract class for the application plugin manager.

    Responsibilities:
    - Retrieve the plugins for the application.
    - Check the pre-conditions for the plugins.
    - Perform actions on startup for the plugins.
    - Perform actions on shutdown for the plugins.
    """

    PACKAGE_NAME: str = ""

    PLUGIN_PACKAGE_NAME: str = "python_factory.core.plugins"

    def __init__(self) -> None:
        """Instanciate the application plugin manager."""
        if self.PACKAGE_NAME == "":
            raise ValueError(
                "The package name must be set in the concrete plugin manager class."
            )

        self._plugins: list[PluginProtocol] = []

        self._plugins_activation_list: PluginsActivationList = (
            self._build_plugins_activation_list()
        )

        self._check_pre_conditions()

    def _check_pre_conditions(self) -> None:
        """Check the pre-conditions for the plugins.

        Raises:
            ApplicationPluginManagerException: If a plugin is not
            activated.

        """
        for plugin in self._plugins_activation_list.activate:
            try:
                plugin_module: ModuleType = import_module(
                    name=f"{self.PLUGIN_PACKAGE_NAME}.{plugin.value}"
                )
            except ImportError as exception:
                raise ApplicationPluginManagerException(
                    f"Unable to import the plugin {plugin.value}"
                ) from exception

            if not isinstance(plugin_module, PluginProtocol):
                raise ApplicationPluginManagerException(
                    f"The plugin {plugin.value} does not implement the PluginProtocol"
                )

            if not plugin_module.pre_conditions_check(
                application=cast(BaseApplicationProtocol, self)
            ):
                raise ApplicationPluginManagerException(
                    f"The plugin {plugin.value} does not meet the pre-conditions"
                )

            self._plugins.append(plugin_module)

    def _on_load(self) -> None:
        """Actions to perform on load for the plugins."""
        for plugin in self._plugins:
            plugin.on_load(application=cast(BaseApplicationProtocol, self))

    def _build_plugins_activation_list(self) -> PluginsActivationList:
        """Build the plugins activation list.

        Returns:
            PluginsActivationList: The plugins activation list.

        Raises:
            ApplicationPluginManagerException: If there is an error
            reading the configuration file.
            ApplicationPluginManagerException: If there is an error
            creating the configuration model.

        """
        try:
            config: PluginsActivationList = build_config_from_file_in_package(
                package_name=self.PACKAGE_NAME,
                filename="application.yaml",
                config_class=PluginsActivationList,
                yaml_base_key="plugins",
            )
        except UnableToReadConfigFileError as exception:
            raise ApplicationPluginManagerException(
                "Unable to read the application configuration file"
            ) from exception
        except ValueErrorConfigError as exception:
            raise ApplicationPluginManagerException(
                "Unable to create the application configuration model"
            ) from exception

        return config

    async def _on_startup(self) -> None:
        """Actions to perform on startup for the plugins."""
        for plugin in self._plugins:
            await plugin.on_startup(application=cast(BaseApplicationProtocol, self))
