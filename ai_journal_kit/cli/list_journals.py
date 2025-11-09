"""List command to show all configured journals."""

import json

import typer
from rich.table import Table

from ai_journal_kit.core.config import get_active_journal_name, load_multi_journal_config
from ai_journal_kit.utils.ui import console, show_error


def list_journals(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """List all configured journals.

    Shows all journals with their locations, frameworks, and active status.

    Examples:
        ai-journal-kit list
        ai-journal-kit list --json
    """
    multi_config = load_multi_journal_config()
    if not multi_config or not multi_config.journals:
        show_error(
            "No journals configured", "Run 'ai-journal-kit setup' to create your first journal"
        )
        raise typer.Exit(1)

    active_name = get_active_journal_name()

    if json_output:
        # JSON output
        output = {
            "active_journal": active_name,
            "journals": {},
        }

        for name, profile in multi_config.journals.items():
            output["journals"][name] = {
                "name": name,
                "location": str(profile.location),
                "framework": profile.framework,
                "ide": profile.ide,
                "version": profile.version,
                "created_at": profile.created_at.isoformat(),
                "last_updated": profile.last_updated.isoformat(),
                "is_active": name == active_name,
            }

        print(json.dumps(output, indent=2))
    else:
        # Rich table output
        table = Table(title="Configured Journals", show_header=True)
        table.add_column("Name", style="cyan")
        table.add_column("Location")
        table.add_column("Framework")
        table.add_column("IDE")
        table.add_column("Status", justify="center")

        for name, profile in multi_config.journals.items():
            status = "✓ Active" if name == active_name else ""
            status_style = "green bold" if name == active_name else "dim"

            table.add_row(
                name,
                str(profile.location),
                profile.framework,
                profile.ide,
                f"[{status_style}]{status}[/{status_style}]",
            )

        console.print()
        console.print(table)
        console.print()
        console.print("[dim]Switch journals with: [cyan]ai-journal-kit use <name>[/cyan][/dim]")
        console.print(
            "[dim]Override for single command: [cyan]AI_JOURNAL=<name> ai-journal-kit <command>[/cyan][/dim]\n"
        )
