"""Provides the App and AppConfig classes."""

from .app import App, AppModule, factory_for_app
from .config import AppConfig

__all__: list[str] = ["App", "AppConfig", "factory_for_app", "AppModule"]
