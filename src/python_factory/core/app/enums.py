"""
Provides enums for the app module.
"""

from enum import StrEnum


class EnvironmentEnum(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
