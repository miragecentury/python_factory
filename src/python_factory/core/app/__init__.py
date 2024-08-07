"""
Package that contains the abstract classes
for the application and application configuration.
"""

from .abstracts import AppBase, AppConfigAbstract
from .enums import EnvironmentEnum

__all__: list[str] = [
    "AppBase",
    "AppConfigAbstract",
    "EnvironmentEnum",
]
