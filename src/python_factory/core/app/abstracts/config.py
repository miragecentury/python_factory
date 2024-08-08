"""
Provide the configuration for the app server.
"""

from ..enums import EnvironmentEnum
from .fastapi_abstract import FastAPIConfigAbstract


class AppConfigAbstract(FastAPIConfigAbstract):
    environment: EnvironmentEnum
