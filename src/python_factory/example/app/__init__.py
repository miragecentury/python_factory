"""
Provides the App and AppConfig classes.
"""

from .app import App, app_factory
from .config import AppConfig

__all__: list[str] = ["App", "AppConfig", "app_factory"]
