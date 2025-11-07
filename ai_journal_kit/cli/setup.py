"""Setup command for first-time journal installation."""

from pathlib import Path

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_journal_kit.core.config import Config, load_config, save_config
from ai_journal_kit.core.journal import create_structure
from ai_journal_kit.core.templates import copy_ide_configs
from ai_journal_kit.core.validation import validate_ide, validate_path
from ai_journal_kit.utils.ui import (
    ask_ide,
    ask_path,
    confirm,
    console,
    show_error,
    show_panel,
    show_success,
)


def setup(
    location: str = typer.Option(None, "--location", "-l", help="Journal location path"),
    ide: str = typer.Option(
        None, "--ide", "-i", help="AI editor: cursor/windsurf/claude-code/copilot/all"
    ),
    no_confirm: bool = typer.Option(False, "--no-confirm", help="Skip confirmation prompt"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without doing it"
    ),
):
    """Set up your AI journal for the first time.

    Interactive setup that guides you through:
    - Choosing journal location (local or cloud)
    - Selecting your AI editor
    - Creating journal structure
    - Installing AI coach configurations
    """
    # Check if already set up
    existing_config = load_config()
    if existing_config and not dry_run:
        # Check if the journal location actually exists
        if existing_config.journal_location.exists():
            show_error(
                f"Journal already set up at {existing_config.journal_location}",
                "To reconfigure, run: ai-journal-kit move",
            )
            raise typer.Exit(1)
        else:
            # Journal was deleted - warn but allow setup
            console.print(
                f"[yellow]Note: Previous journal at {existing_config.journal_location} no longer exists.[/yellow]"
            )
            console.print("[yellow]Creating new journal configuration...[/yellow]\n")

    # Interactive prompts if options not provided
    if location is None:
        location = ask_path("Where would you like to store your journal?", default="~/journal")

    # Validate and normalize path
    try:
        journal_path = Path(location).expanduser().resolve()

        # Check if parent exists, offer to create
        if not journal_path.parent.exists():
            if dry_run:
                console.print(f"[dim][DRY RUN] Would create parent: {journal_path.parent}[/dim]")
            else:
                create_parent = confirm(
                    f"Parent directory doesn't exist. Create {journal_path.parent}?"
                )
                if create_parent:
                    journal_path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    show_error("Setup cancelled")
                    raise typer.Exit(1)

        # Validate path
        validate_path(journal_path)

    except ValueError as e:
        show_error(str(e), "Please provide a valid filesystem path.")
        raise typer.Exit(1)

    # IDE selection
    if ide is None:
        ide = ask_ide()

    # Validate IDE
    try:
        ide = validate_ide(ide)
    except ValueError as e:
        show_error(str(e))
        raise typer.Exit(1)

    # Show summary
    from ai_journal_kit.core.config import get_config_path

    summary = f"""[bold cyan]Setup Configuration[/bold cyan]

• Journal Location: [yellow]{journal_path}[/yellow]
• AI Editor: [yellow]{ide}[/yellow]
• Config File: [yellow]{get_config_path()}[/yellow]

This will create your journal structure and install AI coaching configurations.
"""

    if dry_run:
        console.print("[bold yellow]DRY RUN MODE[/bold yellow]\n")

    show_panel(summary.strip(), border_style="blue")

    if dry_run:
        console.print("\n[dim][DRY RUN] Would create:")
        for folder in ["daily", "projects", "areas", "resources", "people", "memories", "archive"]:
            console.print(f"[dim]  {journal_path / folder}/[/dim]")
        console.print(f"[dim]  {journal_path / '.ai-instructions'}/[/dim]")
        console.print(f"\n[dim][DRY RUN] Would install {ide} configuration[/dim]")
        console.print(f"[dim][DRY RUN] Would create config at: {get_config_path()}[/dim]\n")
        console.print("[yellow]No changes made.[/yellow]")
        return

    # Confirmation
    if not no_confirm:
        proceed = confirm("Proceed?")
        if not proceed:
            console.print("[yellow]Setup cancelled.[/yellow]")
            raise typer.Exit(0)

    # Execute setup with progress
    try:
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console
        ) as progress:
            # Create journal structure
            task1 = progress.add_task("Creating journal structure...", total=None)
            create_structure(journal_path)
            progress.update(task1, completed=True)

            # Install IDE configs
            task2 = progress.add_task(f"Installing {ide} configuration...", total=None)
            copy_ide_configs(ide, journal_path)
            progress.update(task2, completed=True)

            # Create config
            task3 = progress.add_task("Saving configuration...", total=None)
            config = Config(journal_location=journal_path, ide=ide)
            save_config(config)
            progress.update(task3, completed=True)

        # Success message
        show_success("Setup complete!")
        console.print("\n[bold]Next steps:[/bold]")
        console.print(f"1. Open [cyan]{journal_path}[/cyan] in your IDE")
        console.print("2. Start journaling with your AI coach")
        console.print("3. Check status anytime: [cyan]ai-journal-kit status[/cyan]\n")

    except Exception as e:
        show_error(f"Setup failed: {e}")
        raise typer.Exit(1)
