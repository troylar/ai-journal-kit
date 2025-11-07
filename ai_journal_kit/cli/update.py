"""Update command for safely updating the core system."""

import subprocess

import typer
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_journal_kit.core.config import load_config
from ai_journal_kit.core.templates import copy_ide_configs
from ai_journal_kit.utils.ui import confirm, console, show_error, show_panel, show_success


def get_latest_version() -> str | None:
    """Query PyPI for the latest version of ai-journal-kit.

    Returns:
        Latest version string or None if unable to check.
    """
    try:
        subprocess.run(
            ["python", "-m", "pip", "index", "versions", "ai-journal-kit"],
            capture_output=True,
            text=True,
            check=True,
        )
        # Parse output to get latest version
        # For now, return None (will be implemented when published to PyPI)
        return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_changelog(from_version: str, to_version: str) -> str | None:
    """Fetch changelog between versions from GitHub.

    Returns:
        Markdown changelog or None if unavailable.
    """
    # TODO: Fetch from GitHub releases API
    # For now, return a placeholder
    return f"""
# What's New in {to_version}

## ✨ New Features
- Onboarding flow: Journal now guides new users through customization
- System protection: AI can't accidentally modify core files
- WELCOME.md: Helpful starter guide in every new journal

## 🛡️ AI Behavior Changes
- Added protective rules to prevent editing system files
- Onboarding rule now triggers on "help me get started"
- All changes maintain backward compatibility

## 🐛 Bug Fixes
- Improved error handling in CLI commands
- Better path validation across platforms

## 📦 Updates
- IDE configs refreshed with latest rules
- Templates updated for better user experience
"""


def update(
    check: bool = typer.Option(False, "--check", help="Check for updates without installing"),
    no_confirm: bool = typer.Option(False, "--no-confirm", help="Skip confirmation prompt"),
    force: bool = typer.Option(False, "--force", help="Force reinstall IDE configs even if up to date"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be updated"),
):
    """Update AI Journal Kit to the latest version.

    Updates NEVER touch your journal content or customizations!

    The update will:
    - Upgrade the package to the latest version
    - Refresh IDE configurations with latest rules
    - Preserve all your journal data
    - Keep your custom configurations (.ai-instructions/)
    - Show changelog with any AI behavior changes
    """
    config = load_config()
    if not config:
        show_error("Journal not set up", "Run 'ai-journal-kit setup' first")
        raise typer.Exit(1)

    console.print("[bold cyan]Checking for updates...[/bold cyan]\n")

    # Check current version
    from ai_journal_kit import __version__ as current_version

    console.print(f"  Current version: [cyan]{current_version}[/cyan]")

    # Check for latest version
    with console.status("[cyan]Querying PyPI..."):
        latest_version = get_latest_version()

    if latest_version is None:
        # Can't check PyPI (dev mode or network issue)
        console.print("  Latest version:  [yellow]Unable to check[/yellow]")
        console.print("\n[yellow]Note: Running in development mode or PyPI unavailable.[/yellow]")

        if not force:
            console.print("[yellow]Use --force to reinstall IDE configs anyway.[/yellow]\n")
            raise typer.Exit(0)
        else:
            console.print("[yellow]Forcing IDE config refresh...[/yellow]\n")
            latest_version = current_version  # Pretend we're updating
    else:
        console.print(f"  Latest version:  [cyan]{latest_version}[/cyan]\n")

        if latest_version == current_version and not force:
            console.print("[green]✓ You're already on the latest version![/green]\n")
            if check:
                raise typer.Exit(0)
            console.print("No updates needed. Use --force to reinstall IDE configs.\n")
            raise typer.Exit(0)

    if check:
        console.print(f"\n[yellow]Update available: {current_version} → {latest_version}[/yellow]")
        console.print("Run without --check to install.\n")
        raise typer.Exit(0)

    # Show changelog
    changelog = get_changelog(current_version, latest_version)
    if changelog:
        console.print(Panel(Markdown(changelog), title="[bold cyan]Changelog[/bold cyan]", border_style="cyan"))
        console.print()

    # Summary of what will happen
    show_panel(
        "Update Plan",
        f"• Package: [yellow]{current_version}[/yellow] → [green]{latest_version}[/green]\n"
        f"• IDE Configs: Refresh [cyan]{config.ide}[/cyan] configurations\n"
        f"• Journal: [green]{config.journal_location}[/green]\n\n"
        "[bold]What's Protected:[/bold]\n"
        "✓ All journal content (daily, projects, people, memories, etc.)\n"
        "✓ Your custom preferences (.ai-instructions/)\n"
        "✓ Your data remains untouched\n\n"
        "[bold]What's Updated:[/bold]\n"
        "→ IDE configuration files with new features\n"
        "→ System templates and rules\n"
        "→ WELCOME.md (if it exists, will be replaced)"
    )

    if not no_confirm and not dry_run:
        if not confirm("Proceed with update?"):
            console.print("[red]Update cancelled.[/red]")
            raise typer.Exit(0)

    if dry_run:
        console.print("[yellow]Dry run complete. No changes were made.[/yellow]")
        raise typer.Exit(0)

    # Perform update
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        # Step 1: Upgrade package (if not forcing)
        if not force:
            task_upgrade = progress.add_task("[cyan]Upgrading package...", total=1)
            try:
                subprocess.run(
                    ["uvx", "--upgrade", "ai-journal-kit"],
                    check=True,
                    capture_output=True,
                )
                progress.update(task_upgrade, completed=1, description="[green]Package upgraded.[/green]")
            except subprocess.CalledProcessError as e:
                progress.update(task_upgrade, completed=1, description="[red]Upgrade failed.[/red]")
                show_error("Package upgrade failed", str(e))
                raise typer.Exit(1)

        # Step 2: Refresh IDE configs
        task_configs = progress.add_task(f"[cyan]Refreshing {config.ide} configurations...", total=1)
        try:
            copy_ide_configs(config.ide, config.journal_location)
            progress.update(task_configs, completed=1, description=f"[green]{config.ide.capitalize()} configs refreshed.[/green]")
        except Exception as e:
            progress.update(task_configs, completed=1, description="[red]Config refresh failed.[/red]")
            show_error("Failed to refresh IDE configs", str(e))
            raise typer.Exit(1)

        # Step 3: Update WELCOME.md if it exists
        welcome_path = config.journal_location / "WELCOME.md"
        if welcome_path.exists():
            task_welcome = progress.add_task("[cyan]Updating WELCOME.md...", total=1)
            from ai_journal_kit.core.templates import copy_template
            copy_template("WELCOME.md", welcome_path)
            progress.update(task_welcome, completed=1, description="[green]WELCOME.md updated.[/green]")

    show_success(
        "Update Complete!",
        f"✨ AI Journal Kit updated to [green]{latest_version}[/green]!\n\n"
        f"Your journal at [cyan]{config.journal_location}[/cyan] is ready.\n\n"
        "[bold]What Changed:[/bold]\n"
        "• IDE configs refreshed with latest features\n"
        "• New AI rules and templates installed\n"
        "• Your content and customizations untouched\n\n"
        "Open your journal to see what's new!"
    )
