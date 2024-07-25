"""
Provide "commands" definition for cli
"""

import structlog

_logger = structlog.get_logger(__package__)


def execute():
    """
    Execute the command
    """
    _logger.info("Executing command")
