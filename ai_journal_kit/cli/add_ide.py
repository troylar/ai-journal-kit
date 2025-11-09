"""Add IDE command for installing additional IDE configurations."""

import typer

from ai_journal_kit.core.config import load_config
from ai_journal_kit.core.templates import copy_ide_configs
from ai_journal_kit.core.validation import validate_ide
from ai_journal_kit.utils.ui import ask_ide, console, show_error, show_success


def add_ide(
    ide: str = typer.Argument(
        None,
        help="AI editor to add: cursor/windsurf/claude-code/copilot/all",
    ),
):
    """Add IDE configuration to your existing journal.

    Install AI coach configurations for additional editors without
    recreating your entire journal setup.

    Examples:
        ai-journal-kit add-ide cursor
        ai-journal-kit add-ide --help
    """
    # Check if journal is set up
    config = load_config()
    if not config:
        show_error(
            "Journal not set up yet",
            "Run 'ai-journal-kit setup' first to create your journal",
        )
        raise typer.Exit(1)

    # Interactive prompt if IDE not provided
    if ide is None:
        ide = ask_ide("Which AI editor would you like to add?")

    # Validate IDE selection
    try:
        ide = validate_ide(ide)
    except ValueError:
        show_error(
            f"Invalid IDE: {ide}",
            "Choose from: cursor, windsurf, claude-code, copilot, all",
        )
        raise typer.Exit(1)

    # Show what will be installed
    if ide == "all":
        console.print("\n[cyan]Installing configs for:[/cyan]")
        console.print("  • Cursor")
        console.print("  • Windsurf")
        console.print("  • Claude Code (Cline)")
        console.print("  • GitHub Copilot\n")
    else:
        ide_names = {
            "cursor": "Cursor",
            "windsurf": "Windsurf",
            "claude-code": "Claude Code (Cline)",
            "copilot": "GitHub Copilot",
        }
        console.print(f"\n[cyan]Installing {ide_names.get(ide, ide)} configuration...[/cyan]\n")

    # Install IDE configs
    try:
        copy_ide_configs(ide, config.journal_location, framework=config.framework)
    except Exception as e:
        show_error("Failed to install IDE configuration", str(e))
        raise typer.Exit(1)

    # Success message
    success_msg = (
        f"IDE configuration installed at [cyan]{config.journal_location}[/cyan]\n\n"
        "[bold]What was added:[/bold]\n"
    )

    if ide == "all" or ide == "cursor":
        success_msg += "• Cursor: .cursor/rules/*.mdc\n"
    if ide == "all" or ide == "windsurf":
        success_msg += "• Windsurf: .windsurf/rules/*.md\n"
    if ide == "all" or ide == "claude-code":
        success_msg += "• Claude Code: CLAUDE.md, SYSTEM-PROTECTION.md\n"
    if ide == "all" or ide == "copilot":
        success_msg += "• GitHub Copilot: .github/instructions/*.md\n"

    success_msg += "\n[dim]Your journal content and settings remain untouched.[/dim]"

    show_success(success_msg)
