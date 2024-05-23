"""
Provides a function to setup the logging configuration.
"""

from enum import StrEnum, auto

import structlog

_logger = structlog.getLogger(__package__)


class LogModeEnum(StrEnum):
    """
    Defines the possible logging modes.
    """

    CONSOLE = auto()
    JSON = auto()


def setup_log(mode: LogModeEnum = LogModeEnum.CONSOLE) -> None:
    """
    Prepares the logging configuration.

    Args:
        mode (LogMode): The logging mode to use.

    Returns:
        None
    """

    _processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.CallsiteParameterAdder(
            parameters={
                structlog.processors.CallsiteParameter.MODULE: True,
                structlog.processors.CallsiteParameter.FUNC_NAME: True,
                structlog.processors.CallsiteParameter.LINENO: True,
            }
        ),
    ]

    match mode:
        case LogModeEnum.CONSOLE:
            _processors.append(structlog.processors.ExceptionPrettyPrinter())
            _processors.append(structlog.dev.ConsoleRenderer())
        case LogModeEnum.JSON:
            _processors.append(structlog.processors.ExceptionRenderer())
            _processors.append(structlog.processors.JSONRenderer())

    structlog.configure(processors=_processors, cache_logger_on_first_use=True)
