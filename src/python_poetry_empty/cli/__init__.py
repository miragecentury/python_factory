"""
Cli Package definitions
"""

import typer

from .commands import execute

# Create Typer Application
cli = typer.Typer()

# Add command
cli.command(name="execute")(execute)
