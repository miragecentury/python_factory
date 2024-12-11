"""Provides the module for the ODM plugin."""

from typing import Any, Self

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from python_factory.core.protocols import BaseApplicationProtocol
from python_factory.core.utils.importlib import get_path_file_in_package
from python_factory.core.utils.yaml_reader import (
    UnableToReadYamlFileError,
    YamlFileReader,
)

from .configs import ODMConfig
from .exceptions import ODMPluginConfigError


class ODMBuilder:
    """Factory to create the resources for the ODM plugin.

    The factory is responsible for creating the resources for the ODM plugin.
    - The ODM configuration.
    - The ODM client.
    - The ODM database.

    ```python
    # Example of using the ODMFactory
    odm_factory: ODMFactory = ODMFactory(application=application)
    odm_factory.build_odm_config()
    odm_factory.build_client()
    odm_factory.build_database()
    # Access the ODM database created
    database: AsyncIOMotorDatabase[Any] = odm_factory.database
    ```

    """

    def __init__(self, application: BaseApplicationProtocol) -> None:
        """Initialize the ODMFactory."""
        self._application: BaseApplicationProtocol = application
        self._config: ODMConfig | None = None
        self._odm_client: AsyncIOMotorClient[Any] | None = None
        self._odm_database: AsyncIOMotorDatabase[Any] | None = None

    @property
    def config(self) -> ODMConfig | None:
        """Provide the ODM configuration object.

        Returns:
            ODMConfig: The ODM configuration object.
        """
        return self._config

    @property
    def odm_client(self) -> AsyncIOMotorClient[Any] | None:
        """Provide the ODM client.

        Returns:
            AsyncIOMotorClient | None: The ODM client.
        """
        return self._odm_client

    @property
    def odm_database(self) -> AsyncIOMotorDatabase[Any] | None:
        """Provide the ODM database.

        Returns:
            AsyncIOMotorDatabase | None: The ODM database.
        """
        return self._odm_database

    def build_odm_config(
        self,
    ) -> Self:
        """Build the ODM configuration object.

        Returns:
            Self: The ODM factory.

        Raises:
            ODMPluginConfigError: If the package name is not set or the configuration file is not found.
        """
        if self._application.PACKAGE_NAME == "":
            raise ODMPluginConfigError("The package name must be set in the concrete application class.")
        # Read the application configuration file
        try:
            yaml_file_content: dict[str, Any] = YamlFileReader(
                file_path=get_path_file_in_package(
                    filename="application.yaml",
                    package=self._application.PACKAGE_NAME,
                ),
                yaml_base_key="odm",
                use_environment_injection=True,
            ).read()
        except (FileNotFoundError, ImportError, UnableToReadYamlFileError) as exception:
            raise ODMPluginConfigError("Unable to read the application configuration file.") from exception

        # Create the application configuration model
        try:
            self._config = ODMConfig(**yaml_file_content)
        except ValueError as exception:
            raise ODMPluginConfigError("Unable to create the application configuration model.") from exception
        return self

    def build_client(
        self,
        odm_config: ODMConfig | None = None,
    ) -> Self:
        """Build the ODM client.

        Args:
            odm_config (ODMConfig): The ODM configuration.

        Returns:
            Self: The ODM factory.

        Raises:
            ODMPluginConfigError: If the ODM configuration is not build or provided.
        """
        if odm_config is None:
            odm_config = self._config
        if odm_config is None:
            raise ODMPluginConfigError(
                "ODM configuration is not set. Provide the ODM configuration using "
                "build_odm_config method or through parameter."
            )

        self._odm_client = AsyncIOMotorClient(
            host=odm_config.uri,
            connect=True,
            connectTimeoutMS=odm_config.connection_timeout_ms,
            serverSelectionTimeoutMS=odm_config.connection_timeout_ms,
        )

        return self

    def build_database(
        self,
        odm_client: AsyncIOMotorClient[Any] | None = None,
        odm_config: ODMConfig | None = None,
        database_name: str | None = None,
    ) -> Self:
        """Build the ODM database.

        The ODM client and ODM configuration are recommended to be provided through call to the build_client and
        build_odm_config methods.

        Args:
            odm_config (ODMConfig): The ODM configuration. (Default is None)
            odm_client (AsyncIOMotorClient): The ODM client. (Default is None)
            database_name (str): The database name. (Default is None)

        Returns:
            Any: The ODM database.

        Raises:
            ODMPluginConfigError: If the ODM configuration is not build or provided.
        """
        if database_name is None:
            if odm_config is None:
                odm_config = self._config

            if odm_config is None:
                raise ODMPluginConfigError(
                    "ODM configuration is not set. Provide the ODM configuration using "
                    "build_odm_config method or through parameter."
                )

            database_name = odm_config.database

        if odm_client is None:
            odm_client = self._odm_client

        if odm_client is None:
            raise ODMPluginConfigError(
                "ODM client is not set. Provide the ODM client using " "build_client method or through parameter."
            )

        self._odm_database = odm_client.get_database(name=database_name)

        return self
