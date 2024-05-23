"""
Entry point for the module.
"""

import logging

import structlog

from .cli import cli
from .setup.log import LogModeEnum, setup_log

_logger: logging.Logger = structlog.get_logger(__package__)


def main() -> None:
    """
    Main entry point for the module.
    """
    setup_log(mode=LogModeEnum.CONSOLE)
    cli()


if __name__ == "__main__":
    main()
