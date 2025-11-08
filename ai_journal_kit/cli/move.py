"""Move command for relocating journal to a new location."""

import shutil
from pathlib import Path

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_journal_kit.core.config import get_config_path, load_config, save_config
from ai_journal_kit.core.symlinks import update_link_target
from ai_journal_kit.core.validation import validate_path
from ai_journal_kit.utils.ui import (
    ask_path,
    confirm,
    console,
    show_error,
    show_success,
)


def move(
    new_location: str = typer.Argument(None, help="New journal location"),
    no_confirm: bool = typer.Option(False, "--no-confirm", help="Skip confirmation"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes"),
):
    """Move your journal to a new location.

    This command:
    - Moves all journal files to the new location
    - Updates configuration
    - Updates symlinks (if applicable)
    - Preserves all your content and customizations
    """
    config = load_config()
    if not config:
        show_error("Journal not set up", "Run 'ai-journal-kit setup' first")
        raise typer.Exit(1)

    current_location = config.journal_location

    # Check if current location exists
    if not current_location.exists():
        show_error(
            f"Current journal location doesn't exist: {current_location}",
            "The location was deleted or moved. Delete config and run 'ai-journal-kit setup' to start fresh.",
        )
        console.print("\nTo delete config and start over:\n")
        console.print(f"  rm {get_config_path()}")
        console.print("  ai-journal-kit setup\n")
        raise typer.Exit(1)

    # Interactive prompt if location not provided
    if new_location is None:
        console.print(f"\nCurrent location: [cyan]{current_location}[/cyan]\n")
        new_location = ask_path("New location:")

    # Validate new location
    try:
        new_path = Path(new_location).expanduser().resolve()

        # Check if same location
        if new_path == current_location:
            show_error("New location is the same as current location")
            raise typer.Exit(1)

        # Check if parent exists
        if not new_path.parent.exists():
            if dry_run:
                console.print(f"[dim][DRY RUN] Would create parent: {new_path.parent}[/dim]")
            elif no_confirm:
                # Auto-create parent when no-confirm is set
                new_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                create_parent = confirm(
                    f"Parent directory doesn't exist. Create {new_path.parent}?"
                )
                if not create_parent:
                    show_error("Move cancelled")
                    raise typer.Exit(1)
                new_path.parent.mkdir(parents=True, exist_ok=True)

        validate_path(new_path)

    except ValueError as e:
        show_error(str(e))
        raise typer.Exit(1)

    # Check if destination already has files
    if new_path.exists() and any(new_path.iterdir()):
        console.print(f"\n[yellow]Warning: {new_path} already contains files.[/yellow]\n")
        console.print("Options:")
        console.print("  1. Cancel (recommended)")
        console.print("  2. Merge with existing files")
        console.print("  3. Replace existing files\n")

        if dry_run:
            console.print("[dim][DRY RUN] Would prompt for action[/dim]")
        else:
            choice = typer.prompt("Choose", default="1")
            if choice == "1":
                console.print("[yellow]Move cancelled.[/yellow]")
                raise typer.Exit(0)
            elif choice == "3":
                if confirm("Are you sure? This will delete existing files."):
                    shutil.rmtree(new_path)
                else:
                    console.print("[yellow]Move cancelled.[/yellow]")
                    raise typer.Exit(0)
            # If 2, we'll merge (do nothing special)

    # Show summary
    console.print("\n[bold]Move Summary:[/bold]")
    console.print(f"  From: [yellow]{current_location}[/yellow]")
    console.print(f"  To:   [yellow]{new_path}[/yellow]\n")

    if dry_run:
        console.print("[dim][DRY RUN] Would move all files and update configuration[/dim]")
        console.print("[dim][DRY RUN] No changes made.[/dim]\n")
        return

    # Confirmation
    if not no_confirm:
        if not confirm("Proceed with move?"):
            console.print("[yellow]Move cancelled.[/yellow]")
            raise typer.Exit(0)

    # Execute move
    try:
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console
        ) as progress:
            # Move files
            task1 = progress.add_task("Moving files...", total=None)
            if not new_path.exists():
                new_path.mkdir(parents=True, exist_ok=True)
            shutil.copytree(current_location, new_path, dirs_exist_ok=True)
            progress.update(task1, completed=True)

            # Update config
            task2 = progress.add_task("Updating configuration...", total=None)
            config.journal_location = new_path
            save_config(config)
            progress.update(task2, completed=True)

            # Update symlink if applicable
            if config.use_symlink and config.symlink_source:
                task3 = progress.add_task("Updating symlinks...", total=None)
                update_link_target(config.symlink_source, new_path)
                progress.update(task3, completed=True)

            # Clean up old location
            task4 = progress.add_task("Cleaning up old location...", total=None)
            shutil.rmtree(current_location)
            progress.update(task4, completed=True)

        show_success("Journal moved successfully!")
        console.print(f"\nNew location: [cyan]{new_path}[/cyan]\n")

    except Exception as e:
        show_error(f"Move failed: {e}", "Your journal is still at the original location.")
        raise typer.Exit(1)
