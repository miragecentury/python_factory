"""Provides the module for the ODM plugin."""

from typing import Any

from python_factory.core.protocols import BaseApplicationProtocol
from python_factory.core.utils.importlib import get_path_file_in_package
from python_factory.core.utils.yaml_reader import (
    UnableToReadYamlFileError,
    YamlFileReader,
)

from .configs import ODMConfig
from .exceptions import ODMPluginConfigError


class ODMPluginModule:
    """The module for the ODM plugin."""

    def odm_config(
        self,
        base_application: "BaseApplicationProtocol",
    ) -> ODMConfig:
        """Provide the ODM configuration object.

        Returns:
            ODMConfig: The ODM configuration object.
        """
        if base_application.PACKAGE_NAME == "":
            raise ODMPluginConfigError("The package name must be set in the concrete application class.")
        # Read the application configuration file
        try:
            yaml_file_content: dict[str, Any] = YamlFileReader(
                file_path=get_path_file_in_package(
                    filename="application.yaml",
                    package=base_application.PACKAGE_NAME,
                ),
                yaml_base_key="odm",
                use_environment_injection=True,
            ).read()
        except (FileNotFoundError, ImportError, UnableToReadYamlFileError) as exception:
            raise ODMPluginConfigError("Unable to read the application configuration file.") from exception

        # Create the application configuration model
        try:
            config = ODMConfig(**yaml_file_content)
        except ValueError as exception:
            raise ODMPluginConfigError("Unable to create the application configuration model.") from exception

        return config
