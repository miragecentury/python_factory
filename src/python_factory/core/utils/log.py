"""Provides a function to setup the logging configuration."""

import logging
from enum import StrEnum, auto
from typing import Any

import structlog
from structlog.types import EventDict

_logger = structlog.getLogger(__package__)


class LogModeEnum(StrEnum):
    """Defines the possible logging modes."""

    CONSOLE = auto()
    JSON = auto()


# https://github.com/hynek/structlog/issues/35#issuecomment-591321744
def _rename_event_key(
    _: Any, __: Any, event_dict: EventDict  # pylint: disable=invalid-name
) -> EventDict:
    """Renames the `event` key to `message` in the event dictionary.

    Log entries keep the text message in the `event` field, but Datadog
    uses the `message` field. This processor moves the value from one field to
    the other.
    See https://github.com/hynek/structlog/issues/35#issuecomment-591321744
    """
    event_dict["message"] = event_dict.pop("event")
    return event_dict


def clean_uvicorn_logger() -> None:
    """Cleans the uvicorn loggers."""
    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        # Clear the log handlers for uvicorn loggers, and enable propagation
        # so the messages are caught by our root logger and formatted correctly
        # by structlog
        logging.getLogger(logger_name).handlers.clear()
        logging.getLogger(logger_name).propagate = True


def _drop_color_message_key(
    _: Any, __: Any, event_dict: EventDict  # pylint: disable=invalid-name
) -> EventDict:
    """Cleans the `color_message` key from the event dictionary.

    Uvicorn logs the message a second time in the extra `color_message`, but we don't
    need it. This processor drops the key from the event dict if it exists.
    """
    event_dict.pop("color_message", None)
    return event_dict


def setup_log(
    mode: LogModeEnum = LogModeEnum.CONSOLE, log_level: str = "DEBUG"
) -> None:
    """Prepares the logging configuration.

    Args:
        mode (LogMode): The logging mode to use.
        log_level (str): The log level to use.

    Returns:
        None
    """
    processors: list[structlog.typing.Processor] = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.CallsiteParameterAdder(
            parameters={
                structlog.processors.CallsiteParameter.MODULE: True,
                structlog.processors.CallsiteParameter.FUNC_NAME: True,
                structlog.processors.CallsiteParameter.LINENO: True,
            }
        ),
        _drop_color_message_key,
    ]

    log_renderer: structlog.dev.ConsoleRenderer | structlog.processors.JSONRenderer
    match mode:
        case LogModeEnum.CONSOLE:
            processors.append(structlog.processors.ExceptionPrettyPrinter())
            log_renderer = structlog.dev.ConsoleRenderer()
        case LogModeEnum.JSON:
            # We rename the `event` key to `message` only in JSON logs,
            # as Datadog looks for the
            # `message` key but the pretty ConsoleRenderer looks for `event`
            processors.append(_rename_event_key)
            # Format the exception only for JSON logs, as we want
            # to pretty-print them when
            # using the ConsoleRenderer
            processors.append(structlog.processors.format_exc_info)
            log_renderer = structlog.processors.JSONRenderer()

    # Remove all existing loggers
    structlog.reset_defaults()
    structlog_processors = processors.copy()
    structlog_processors.append(structlog.stdlib.ProcessorFormatter.wrap_for_formatter)
    structlog.configure(
        processors=structlog_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run ONLY on `logging` entries that do NOT originate within
        # structlog.
        foreign_pre_chain=processors,
        # These run on ALL entries after the pre_chain is done.
        processors=[
            # Remove _record & _from_structlog.
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            log_renderer,
        ],
    )

    handler = logging.StreamHandler()
    # Use OUR `ProcessorFormatter` to format all `logging` entries.
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level.upper())
