"""
Provides the abstract class for the application.
"""

from typing import cast

from .config_abstract import AppConfigAbstract
from .fastapi_application_abstract import FastAPIAbstract


class BaseApplication(FastAPIAbstract):
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
        FastAPIAbstract.__init__(self=cast(FastAPIAbstract, self), config=self._config)

    def get_config(self) -> AppConfigAbstract:
        """
        Get the application configuration.
        """
        return self._config
