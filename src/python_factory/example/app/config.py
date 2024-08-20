"""Provides the application configuration."""

from python_factory.core.app import AppConfigAbstract


class AppConfig(AppConfigAbstract):
    """The application configuration."""

    title: str = "Python Factory Example"
    description: str = "An example application for Python Factory."
