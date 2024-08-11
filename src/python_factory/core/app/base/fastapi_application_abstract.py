"""
Provide
"""

from abc import ABC
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel


class FastAPIConfigAbstract(ABC, BaseModel):
    """
    Partial configuration for FastAPI.
    """

    # Application metadata
    title: str
    description: str
    version: str = "0.0.0"

    # Host configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # Root configuration
    root_path: str = ""

    # Debug mode
    debug: bool = False

    # Uvicorn configuration
    reload: bool = False
    workers: int = 1


class FastAPIAbstract(ABC):
    """
    Application integration with FastAPI.
    """

    def __init__(self, config: FastAPIConfigAbstract) -> None:
        self._fastapi_app: FastAPI = FastAPI(
            title=config.title,
            description=config.description,
            version=config.version,
            root_path=config.root_path,
            debug=config.debug,
        )

    def get_asgi_app(self) -> FastAPI:
        """
        Get the ASGI application.
        """
        return self._fastapi_app

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        Forward the call to the FastAPI app.
        """
        return self._fastapi_app.__call__(*args, **kwds)
