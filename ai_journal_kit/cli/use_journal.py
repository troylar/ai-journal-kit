"""Use command to switch active journal."""

import typer

from ai_journal_kit.core.config import (
    load_multi_journal_config,
    save_multi_journal_config,
)
from ai_journal_kit.utils.ui import console, show_error, show_success


def use_journal(
    name: str = typer.Argument(..., help="Name of journal to make active"),
):
    """Switch to a different journal.

    Sets the specified journal as the active journal. All subsequent commands
    will operate on this journal until you switch again.

    The AI_JOURNAL environment variable can override this setting for single commands.

    Examples:
        ai-journal-kit use business
        ai-journal-kit use personal
        AI_JOURNAL=test ai-journal-kit status  # Temporary override
    """
    multi_config = load_multi_journal_config()
    if not multi_config:
        show_error("No journals configured", "Run 'ai-journal-kit setup' first")
        raise typer.Exit(1)

    if not multi_config.has_journal(name):
        show_error(
            f"Journal '{name}' not found",
            f"Available journals: {', '.join(multi_config.journals.keys())}",
        )
        raise typer.Exit(1)

    # Set active journal
    multi_config.set_active(name)
    save_multi_journal_config(multi_config)

    # Show success
    profile = multi_config.journals[name]
    show_success(f"Switched to journal '{name}'")
    console.print("\n[bold]Active Journal:[/bold]")
    console.print(f"  Name:      [cyan]{name}[/cyan]")
    console.print(f"  Location:  {profile.location}")
    console.print(f"  Framework: {profile.framework}")
    console.print(f"  IDE:       {profile.ide}\n")
