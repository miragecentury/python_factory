"""Protocols for the base application."""

from typing import Protocol


class BaseApplicationProtocol(Protocol):
    """Protocol for the base application."""

    PACKAGE_NAME: str
