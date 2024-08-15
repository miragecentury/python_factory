"""
Provides the abstract class for the application.
"""

from typing import cast

from python_factory.core.api import api

from .config_abstract import AppConfigAbstract
from .fastapi_application_abstract import FastAPIAbstract
from .plugins_manager_abstract import ApplicationPluginManagerAbstract


class BaseApplication(FastAPIAbstract, ApplicationPluginManagerAbstract):
    """
    Application abstract class.
    """

    PACKAGE_NAME: str = ""

    def __init__(self, config: AppConfigAbstract) -> None:

        if self.PACKAGE_NAME == "":
            raise ValueError(
                "The package name must be set in the concrete application class."
            )

        self._config: AppConfigAbstract = config
        FastAPIAbstract.__init__(
            self=cast(FastAPIAbstract, self), config=self._config, api_router=api
        )
        ApplicationPluginManagerAbstract.__init__(
            self=cast(ApplicationPluginManagerAbstract, self)
        )

    def get_config(self) -> AppConfigAbstract:
        """
        Get the application configuration.
        """
        return self._config
