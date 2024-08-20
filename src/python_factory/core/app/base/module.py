"""Provide a generic module for injection bindings for the application."""

from typing import Generic, TypeVar, get_args

import injector

from python_factory.core.plugins.opentelemetry_plugin import OpenTelemetryPluginModule
from python_factory.core.utils.configs import (
    UnableToReadConfigFileError,
    ValueErrorConfigError,
    build_config_from_file_in_package,
)

from .application import BaseApplication
from .config_abstract import AppConfigAbstract
from .exceptions import ApplicationConfigFactoryException

APP_T = TypeVar("APP_T", bound=BaseApplication)  # pylint: disable=invalid-name
CONFIG_T = TypeVar("CONFIG_T", bound=AppConfigAbstract)  # pylint: disable=invalid-name


class GenericBaseApplicationModule(Generic[APP_T, CONFIG_T], injector.Module):
    """Generic application module."""

    def configure(self, binder: injector.Binder) -> None:
        """Configure injection bindings for the application in a generic way.

        Args:
            binder (injector.Binder): The injector binder.

        Returns:
            None

        """
        # Retrieve the concrete application class and configuration class
        app_concrete_class, app_config_concrete_class = get_args(
            self.__orig_bases__[0]  # type: ignore[attr-defined]
        )

        # Bind the concreate application type and the base application type
        # to the same provider.
        application_class_provider = injector.ClassProvider(app_concrete_class)
        binder.bind(
            interface=app_concrete_class,
            to=application_class_provider,
            scope=injector.SingletonScope,
        )
        binder.bind(
            interface=BaseApplication,
            to=application_class_provider,
            scope=injector.SingletonScope,
        )

        # Like the application class, bind the concrete application configuration
        # and the application configuration abstract class to the same provider.
        application_config_callable_provider = injector.CallableProvider(
            callable=self._build_generic_application_config
        )
        binder.bind(
            interface=app_config_concrete_class,
            to=application_config_callable_provider,
            scope=injector.SingletonScope,
        )
        binder.bind(
            interface=AppConfigAbstract,
            to=application_config_callable_provider,
            scope=injector.SingletonScope,
        )

        binder.install(module=OpenTelemetryPluginModule)

    def _build_generic_application_config(self) -> CONFIG_T | None:
        """Generic Builder for the application configuration.

        Use the concrete application class to build the concrete application
        configuration class.

        Raises:
            ApplicationFactoryException: If the package name is not set
            in the concrete application class.
            ApplicationFactoryException: If the application configuration file
            cannot be read.
            ApplicationFactoryException: If the application configuration model
            cannot be created.

        Returns:
            The application configuration

        """
        # Retrieve the concrete application class
        # and the concrete application configuration class
        app_concrete_class, app_config_concrete_class = get_args(
            self.__orig_bases__[0]  # type: ignore[attr-defined]
        )

        # Ensure that the package name is set in the concrete application class
        if app_concrete_class.PACKAGE_NAME == "":
            raise ApplicationConfigFactoryException(
                "The package name must be set in the concrete application class."
            )

        try:
            config: CONFIG_T = build_config_from_file_in_package(
                package_name=app_concrete_class.PACKAGE_NAME,
                config_class=app_config_concrete_class,
                filename="application.yaml",
                yaml_base_key="application",
            )
        except UnableToReadConfigFileError as exception:
            raise ApplicationConfigFactoryException(
                "Unable to read the application configuration file."
            ) from exception
        except ValueErrorConfigError as exception:
            raise ApplicationConfigFactoryException(
                "Unable to create the application configuration model."
            ) from exception

        return config
