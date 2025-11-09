"""Typer application instance and CLI setup."""

import typer

from ai_journal_kit import __version__
from ai_journal_kit.cli.add_ide import add_ide as add_ide_command
from ai_journal_kit.cli.customize_template import customize_template as customize_template_command
from ai_journal_kit.cli.doctor import doctor as doctor_command
from ai_journal_kit.cli.list_journals import list_journals as list_journals_command
from ai_journal_kit.cli.move import move as move_command
from ai_journal_kit.cli.setup import setup as setup_command
from ai_journal_kit.cli.status import status as status_command
from ai_journal_kit.cli.switch_framework import switch_framework as switch_framework_command
from ai_journal_kit.cli.update import update as update_command
from ai_journal_kit.cli.use_journal import use_journal as use_journal_command

app = typer.Typer(
    name="ai-journal-kit",
    help="AI-powered journaling system with beautiful CLI",
    add_completion=False,
)


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        typer.echo(f"ai-journal-kit version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
):
    """AI Journal Kit - Setup, customize, and update your AI-powered journal."""
    pass


# Register commands
app.command(name="setup")(setup_command)
app.command(name="use")(use_journal_command)
app.command(name="list")(list_journals_command)
app.command(name="add-ide")(add_ide_command)
app.command(name="switch-framework")(switch_framework_command)
app.command(name="customize-template")(customize_template_command)
app.command(name="status")(status_command)
app.command(name="doctor")(doctor_command)
app.command(name="update")(update_command)
app.command(name="move")(move_command)
