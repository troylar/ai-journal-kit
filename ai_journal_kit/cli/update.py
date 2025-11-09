"""Update command for safely updating the core system."""

import subprocess

import typer
from packaging.version import parse as parse_version
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_journal_kit.core.config import load_config
from ai_journal_kit.core.migration import ensure_manifest_exists
from ai_journal_kit.core.templates import copy_ide_configs
from ai_journal_kit.utils.ui import confirm, console, show_error, show_panel, show_success


def detect_pip_command() -> list[str]:
    """Detect which pip command works on this system.

    Returns:
        Command list that works (e.g., ['pip', 'install'] or ['python3', '-m', 'pip', 'install'])
    """
    # Try different pip commands in order of preference
    commands = [
        ["pip"],
        ["pip3"],
        ["python", "-m", "pip"],
        ["python3", "-m", "pip"],
    ]

    for cmd in commands:
        try:
            # Test if command exists by checking version
            result = subprocess.run(
                cmd + ["--version"],
                check=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return cmd
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            continue

    # Fallback to pip (will fail with clear error if nothing works)
    return ["pip"]


def get_latest_version() -> str | None:
    """Query PyPI for the latest version of ai-journal-kit.

    Returns:
        Latest version string or None if unable to check.
    """
    try:
        import json
        import urllib.request

        with urllib.request.urlopen(
            "https://pypi.org/pypi/ai-journal-kit/json", timeout=5
        ) as response:
            data = json.loads(response.read().decode())
            return data["info"]["version"]
    except Exception:
        return None


def get_changelog(from_version: str, to_version: str) -> str | None:
    """Fetch changelog between versions from GitHub.

    Returns:
        Markdown changelog or None if unavailable.
    """
    try:
        import json
        import urllib.request

        # Fetch release notes from GitHub
        url = f"https://api.github.com/repos/troylar/ai-journal-kit/releases/tags/v{to_version}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            body = data.get("body", "")
            if body:
                return f"# What's New in {to_version}\n\n{body}"
    except Exception:
        pass

    # Fallback to generic message if API fails
    return f"""
# What's New in {to_version}

Check the full changelog at:
https://github.com/troylar/ai-journal-kit/releases/tag/v{to_version}

## 📦 Updates
- Package updated to {to_version}
- IDE configs will be refreshed with latest rules
- See GitHub release for full details
"""


def update(
    check: bool = typer.Option(False, "--check", help="Check for updates without installing"),
    no_confirm: bool = typer.Option(False, "--no-confirm", help="Skip confirmation prompt"),
    force: bool = typer.Option(
        False, "--force", help="Force reinstall IDE configs even if up to date"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be updated"),
    templates: bool = typer.Option(
        False, "--templates", help="Update templates to latest versions (with backup)"
    ),
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

    # Ensure manifest exists (auto-migrate old journals)
    ensure_manifest_exists()

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

        # Compare versions properly to detect downgrades
        try:
            current_parsed = parse_version(current_version)
            latest_parsed = parse_version(latest_version)

            if current_parsed > latest_parsed:
                console.print(
                    "[yellow]⚠️  Your version is newer than PyPI![/yellow]\n"
                    f"  Current: [cyan]{current_version}[/cyan]\n"
                    f"  PyPI:    [dim]{latest_version}[/dim]\n\n"
                    "[dim]This usually means you're running a development version.[/dim]\n"
                )
                if not force:
                    console.print("[yellow]Use --force to reinstall IDE configs anyway.[/yellow]\n")
                    raise typer.Exit(0)
                else:
                    console.print("[yellow]Forcing IDE config refresh...[/yellow]\n")
                    latest_version = current_version  # Don't downgrade
            elif current_parsed == latest_parsed and not force:
                console.print("[green]✓ You're already on the latest version![/green]\n")
                if check:
                    raise typer.Exit(0)
                console.print("No updates needed. Use --force to reinstall IDE configs.\n")
                raise typer.Exit(0)
        except (ValueError, TypeError, AttributeError):
            # Fallback to string comparison if version parsing fails
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
        console.print(
            Panel(
                Markdown(changelog), title="[bold cyan]Changelog[/bold cyan]", border_style="cyan"
            )
        )
        console.print()

    # Check for template updates if requested
    template_changes = {}
    if templates:
        from ai_journal_kit.core.template_updater import get_template_changes, show_template_changes

        template_changes = get_template_changes(config.journal_location)

        if template_changes:
            console.print()
            show_template_changes(template_changes)
            console.print(
                "[yellow]⚠️  Templates will be backed up before updating[/yellow]\n"
                "[dim]Backups are saved with timestamp: template.backup_YYYYMMDD_HHMMSS.md[/dim]\n"
            )

    # Summary of what will happen
    update_details = (
        f"• Package: [yellow]{current_version}[/yellow] → [green]{latest_version}[/green]\n"
        f"• IDE Configs: Refresh [cyan]{config.ide}[/cyan] configurations\n"
    )

    if templates:
        if template_changes:
            update_details += (
                f"• Templates: Update [yellow]{len(template_changes)}[/yellow] template(s)\n"
            )
        else:
            update_details += "• Templates: [green]All up to date[/green]\n"

    update_details += (
        f"• Journal: [green]{config.journal_location}[/green]\n\n"
        "[bold]What's Protected:[/bold]\n"
        "✓ All journal content (daily, projects, people, memories, etc.)\n"
        "✓ Your custom preferences (.ai-instructions/)\n"
    )

    if templates and template_changes:
        update_details += "✓ Original templates (backed up with timestamp)\n"

    update_details += "✓ Your data remains untouched\n\n[bold]What's Updated:[/bold]\n"
    update_details += "→ IDE configuration files with new features\n"
    update_details += "→ System rules and protections\n"
    update_details += "→ WELCOME.md (if it exists, will be replaced)\n"

    if templates and template_changes:
        update_details += (
            f"→ [yellow]{len(template_changes)}[/yellow] template(s) to latest versions\n"
        )

    show_panel("Update Plan", update_details)

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
        # Step 1: Upgrade package (always, even with --force)
        task_upgrade = progress.add_task("[cyan]Upgrading package...", total=1)
        try:
            # Detect which pip command works on this system
            pip_cmd = detect_pip_command()
            upgrade_cmd = pip_cmd + ["install", "--upgrade", "ai-journal-kit"]

            subprocess.run(
                upgrade_cmd,
                check=True,
                capture_output=True,
                text=True,
            )
            progress.update(
                task_upgrade, completed=1, description="[green]Package upgraded![/green]"
            )
        except subprocess.CalledProcessError as e:
            progress.update(task_upgrade, completed=1, description="[red]Upgrade failed.[/red]")
            pip_cmd_str = " ".join(detect_pip_command())
            show_error(
                "Package upgrade failed",
                f"{e.stderr if e.stderr else str(e)}\n\nTry: {pip_cmd_str} install --upgrade --no-cache-dir ai-journal-kit",
            )
            raise typer.Exit(1)

        # Step 2: Refresh IDE configs
        task_configs = progress.add_task(
            f"[cyan]Refreshing {config.ide} configurations...", total=1
        )
        try:
            copy_ide_configs(config.ide, config.journal_location, framework=config.framework)
            progress.update(
                task_configs,
                completed=1,
                description=f"[green]{config.ide.capitalize()} configs refreshed.[/green]",
            )
        except Exception as e:
            progress.update(
                task_configs, completed=1, description="[red]Config refresh failed.[/red]"
            )
            show_error("Failed to refresh IDE configs", str(e))
            raise typer.Exit(1)

        # Step 3: Update templates if requested
        if templates and template_changes:
            from ai_journal_kit.core.template_updater import update_templates

            task_templates = progress.add_task(
                f"[cyan]Updating {len(template_changes)} template(s)...", total=1
            )
            try:
                updated = update_templates(config.journal_location, backup=True)
                progress.update(
                    task_templates,
                    completed=1,
                    description=f"[green]{len(updated)} template(s) updated![/green]",
                )
            except Exception as e:
                progress.update(
                    task_templates, completed=1, description="[red]Template update failed.[/red]"
                )
                show_error("Failed to update templates", str(e))
                raise typer.Exit(1)

        # Step 4: Update WELCOME.md if it exists (and not already updated by templates)
        if not (templates and "WELCOME.md" in template_changes):
            welcome_path = config.journal_location / "WELCOME.md"
            if welcome_path.exists():
                task_welcome = progress.add_task("[cyan]Updating WELCOME.md...", total=1)
                from ai_journal_kit.core.templates import copy_template

                copy_template("WELCOME.md", welcome_path)
                progress.update(
                    task_welcome, completed=1, description="[green]WELCOME.md updated.[/green]"
                )

    # Build success message
    success_msg = (
        f"✨ AI Journal Kit updated to [green]{latest_version}[/green]!\n\n"
        f"Your journal at [cyan]{config.journal_location}[/cyan] is ready.\n\n"
        "[bold]What Changed:[/bold]\n"
        "• IDE configs refreshed with latest features\n"
    )

    if templates and template_changes:
        success_msg += (
            f"• [green]{len(template_changes)}[/green] template(s) updated (originals backed up)\n"
        )

    success_msg += (
        "• Your content and customizations untouched\n\nOpen your journal to see what's new!"
    )

    show_success(success_msg)
