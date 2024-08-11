"""
Package for the base application, abstract config classes and related exceptions.
"""

from .application import BaseApplication
from .config_abstract import AppConfigAbstract
from .exceptions import (
    ApplicationConfigFactoryException,
    ApplicationFactoryException,
    BaseApplicationException,
)
from .module import GenericBaseApplicationModule

__all__: list[str] = [
    "BaseApplication",
    "GenericBaseApplicationModule",
    "AppConfigAbstract",
    "ApplicationConfigFactoryException",
    "ApplicationFactoryException",
    "BaseApplicationException",
]
