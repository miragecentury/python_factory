"""
Provides utilities to handle configurations.
"""

from typing import Any, TypeVar

from pydantic import BaseModel

from python_factory.core.utils.importlib import get_path_file_in_package
from python_factory.core.utils.yaml_reader import (
    UnableToReadYamlFileError,
    YamlFileReader,
)

GENERIC_CONFIG = TypeVar(  # pylint: disable=invalid-name
    "GENERIC_CONFIG", bound=BaseModel
)


class ConfigBaseException(BaseException):
    """
    Base exception for all the configuration exceptions.
    """

    pass


class UnableToReadConfigFileError(ConfigBaseException):
    """
    Exception raised when the configuration file cannot be read.
    """

    pass


class ValueErrorConfigError(ConfigBaseException):
    """
    Exception raised when the configuration file cannot be read.
    """

    pass


def build_config_from_file_in_package(
    package_name: str,
    filename: str,
    config_class: type[GENERIC_CONFIG],
    yaml_base_key: str,
) -> GENERIC_CONFIG:
    """
    Build a configuration object from a file in a package.

    Args:
        package_name (str): The package name.
        filename (str): The filename.
        config_class (type[GENERIC_CONFIG]): The configuration class.

    Returns:
        GENERIC_CONFIG: The configuration object.

    Raises:
        UnableToReadConfigFileError: If the configuration file cannot be read.
        ValueErrorConfigError: If the configuration file is invalid.
    """

    # Read the application configuration file
    try:
        yaml_file_content: dict[str, Any] = YamlFileReader(
            file_path=get_path_file_in_package(
                filename=filename,
                package=package_name,
            ),
            yaml_base_key=yaml_base_key,
            use_environment_injection=True,
        ).read()
    except (FileNotFoundError, ImportError, UnableToReadYamlFileError) as exception:
        raise UnableToReadConfigFileError(
            "Unable to read the application configuration file."
        ) from exception

    # Create the application configuration model
    try:
        config: GENERIC_CONFIG = config_class(**yaml_file_content)
    except ValueError as exception:
        raise ValueErrorConfigError(
            "Unable to create the configuration model."
        ) from exception

    return config
