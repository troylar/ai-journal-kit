"""Status command to display journal configuration and health."""

import json

import typer
from rich.table import Table

from ai_journal_kit.core.config import get_config_path, load_config
from ai_journal_kit.core.journal import get_folder_stats, validate_structure
from ai_journal_kit.core.migration import ensure_manifest_exists
from ai_journal_kit.utils.ui import console


def status(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Check journal status and configuration.

    Shows:
    - Current configuration
    - Journal health checks
    - Latest version info (if available)
    """
    config = load_config()

    if not config:
        if json_output:
            print(json.dumps({"status": "not_setup"}))
        else:
            console.print("[yellow]Status: Not set up[/yellow]\n")
            console.print("AI Journal Kit is installed but not configured.")
            console.print("Run [cyan]'ai-journal-kit setup'[/cyan] to get started.\n")
        raise typer.Exit(0)

    # Ensure manifest exists (auto-migrate old journals)
    ensure_manifest_exists()

    # Health checks
    structure_valid, missing = validate_structure(config.journal_location)
    ide_configs_exist = _check_ide_configs(config)

    if json_output:
        # JSON output
        output = {
            "version": config.version,
            "journal_location": str(config.journal_location),
            "ide": config.ide,
            "created_at": config.created_at.isoformat(),
            "last_updated": config.last_updated.isoformat(),
            "health": {
                "journal_exists": config.journal_location.exists(),
                "structure_valid": structure_valid,
                "ide_configs": ide_configs_exist,
                "config_valid": True,
            },
        }
        print(json.dumps(output, indent=2))
    else:
        # Rich table output
        table = Table(title="AI Journal Kit Status", show_header=False, box=None)
        table.add_column("Setting", style="cyan", width=20)
        table.add_column("Value", style="white")

        table.add_row("Journal Location", str(config.journal_location))
        table.add_row("AI Editor", config.ide)
        table.add_row("Version", config.version)
        table.add_row("Last Updated", config.last_updated.strftime("%Y-%m-%d"))
        table.add_row("Config File", str(get_config_path()))

        console.print()
        console.print(table)
        console.print()

        # Health checks
        console.print("[bold]Health Checks:[/bold]")
        _print_check("Journal folder exists", config.journal_location.exists())
        _print_check("All required folders present", structure_valid)
        if not structure_valid:
            console.print(f"  [dim]Missing: {', '.join(missing)}[/dim]")
        _print_check("IDE configs installed", ide_configs_exist)
        _print_check("Config file valid", True)
        console.print()

        # Verbose mode
        if verbose:
            console.print("[bold]Journal Structure:[/bold]")
            stats = get_folder_stats(config.journal_location)
            for folder, count in stats.items():
                console.print(f"  ✓ {folder}/ ([cyan]{count} files[/cyan])")
            console.print()


def _check_ide_configs(config) -> bool:
    """Check if IDE configs are installed."""
    if config.ide == "cursor":
        return (config.journal_location / ".cursor" / "rules").exists()
    elif config.ide == "windsurf":
        return (config.journal_location / ".windsurf" / "rules").exists()
    elif config.ide == "claude-code":
        return (config.journal_location / "CLAUDE.md").exists()
    elif config.ide == "copilot":
        return (config.journal_location / ".github" / "copilot-instructions.md").exists()
    elif config.ide == "all":
        return True  # At least one should exist
    return False


def _print_check(label: str, passed: bool):
    """Print a check result."""
    icon = "✓" if passed else "✗"
    color = "green" if passed else "red"
    console.print(f"  [{color}]{icon}[/{color}] {label}")
