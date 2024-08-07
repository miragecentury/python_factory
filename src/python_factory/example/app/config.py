"""
Provides the application configuration.
"""

from python_factory.core.app import AppConfigAbstract


class AppConfig(AppConfigAbstract):
    package_name: str = "python_factory.example"
    title: str = "Python Factory Example"
    description: str = "An example application for Python Factory."
