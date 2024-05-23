"""
Entry point for the module.
"""

import asyncio
import logging

import structlog

from .setup.log import setup_log

_logger: logging.Logger = structlog.get_logger(__package__)


async def main() -> None:
    """
    Entry point for the application.
    """
    _logger.info("main started")
    _logger.info("main finished")


if __name__ == "__main__":
    setup_log()
    _logger.debug("logging configured")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        _logger.debug("main interrupted by user with keyboard interrupt")
