"""
Provides the abstract class for the application.
"""

from typing import Generic, TypeVar, cast, get_args

import injector

from .config import AppConfigAbstract
from .fastapi_abstract import FastAPIAbstract

APP_T = TypeVar("APP_T", bound="AppBase")  # pylint: disable=invalid-name
CONFIG_T = TypeVar("CONFIG_T", bound=AppConfigAbstract)  # pylint: disable=invalid-name


class AppBase(FastAPIAbstract):
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


class GenericAppModule(Generic[APP_T, CONFIG_T], injector.Module):

    def configure(self, binder: injector.Binder) -> None:
        app_concrete_class, _ = get_args(
            self.__orig_bases__[0]  # type: ignore[attr-defined]
        )
        binder.bind(interface=app_concrete_class, to=app_concrete_class)
