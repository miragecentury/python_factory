import structlog
import typer

cli = typer.Typer()

_logger = structlog.get_logger(__package__)


@cli.command(name="execute")
def execute():
    """
    Execute the command
    """
    _logger.info("Executing command")
