"""Provides an utility to inject a class using FastAPI's Depends with Injector."""

from typing import TypeVar

import injector
from fastapi import Depends, Request

T = TypeVar("T")


def inject_depends(
    interface: type[T],
) -> T:  # pylint: disable=redefined-outer-name
    """Inject the class using FastAPI's Depends.

    Args:
        interface (Type[T]): The interface to inject.

    Returns:
        T: The injected instance.
    """

    def _inject(request: Request) -> T:
        injector_instance: injector.Injector = request.app.state.injector
        return injector_instance.get(interface=interface)

    return Depends(dependency=_inject)
