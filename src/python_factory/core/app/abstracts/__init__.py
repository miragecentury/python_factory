"""
Provides the abstract class for the application.
"""

from abc import ABC
from typing import cast

from .config import AppConfigAbstract
from .fastapi_abstract import FastAPIAbstract


class AppBase(FastAPIAbstract):
    """
    Application abstract class.
    """

    def __init__(self, config: AppConfigAbstract) -> None:
        self._config: AppConfigAbstract = config
        FastAPIAbstract.__init__(self=cast(FastAPIAbstract, self), config=self._config)

    def get_config(self) -> AppConfigAbstract:
        """
        Get the application configuration.
        """
        return self._config
