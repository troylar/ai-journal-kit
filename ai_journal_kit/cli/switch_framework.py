"""Switch framework command for changing journaling methodology."""

import shutil
from datetime import datetime
from pathlib import Path

import questionary
import typer
from rich.table import Table

from ai_journal_kit.core.config import load_config, update_config
from ai_journal_kit.core.journal import copy_framework_templates
from ai_journal_kit.core.manifest import Manifest
from ai_journal_kit.core.migration import ensure_manifest_exists
from ai_journal_kit.core.validation import validate_framework
from ai_journal_kit.utils.ui import ask_framework, console, show_error, show_success


def switch_framework(
    framework: str = typer.Argument(
        None,
        help="Framework to switch to: default/gtd/para/bullet-journal/zettelkasten",
    ),
    no_confirm: bool = typer.Option(False, "--no-confirm", help="Skip confirmation prompt"),
):
    """Switch to a different journaling framework.

    This command allows you to change your journaling framework after setup.
    Customized templates are detected and you'll be offered options to preserve them.

    Examples:
        ai-journal-kit switch-framework gtd
        ai-journal-kit switch-framework para
        ai-journal-kit switch-framework  # Interactive selection
    """
    # Check if journal is set up
    config = load_config()
    if not config:
        show_error(
            "Journal not set up yet",
            "Run 'ai-journal-kit setup' first to create your journal",
        )
        raise typer.Exit(1)

    # Ensure manifest exists (auto-migrate old journals)
    ensure_manifest_exists()

    journal_path = config.journal_location
    current_framework = config.framework

    # Interactive framework selection if not provided
    if framework is None:
        framework = ask_framework()

    # Validate framework
    try:
        framework = validate_framework(framework)
    except ValueError as e:
        show_error(str(e))
        raise typer.Exit(1)

    # Check if already using this framework
    if framework == current_framework:
        console.print(f"\n[yellow]You're already using the {framework} framework.[/yellow]")
        console.print("No changes needed.\n")
        raise typer.Exit(0)

    # Load manifest
    manifest_path = journal_path / ".system-manifest.json"
    manifest = Manifest.load(manifest_path)

    # Detect customized templates
    template_files = list(journal_path.glob("*-template.md"))
    customized_templates = []

    for template_file in template_files:
        if manifest.is_customized(template_file, relative_to=journal_path):
            customized_templates.append(template_file)

    # Show framework switch summary
    framework_names = {
        "default": "Default (flexible)",
        "gtd": "GTD (Getting Things Done)",
        "para": "PARA (Projects, Areas, Resources, Archive)",
        "bullet-journal": "Bullet Journal",
        "zettelkasten": "Zettelkasten",
    }

    console.print(
        f"\n[bold cyan]Framework Switch: {framework_names.get(current_framework, current_framework)} → {framework_names.get(framework, framework)}[/bold cyan]\n"
    )

    # Show interactive checklist
    if not no_confirm:
        show_interactive_checklist(
            framework=framework,
            framework_name=framework_names.get(framework, framework),
            customized_count=len(customized_templates),
        )

        # If customized templates exist, offer resolution options
        if customized_templates:
            action = ask_customization_resolution(
                customized_templates, framework_names.get(framework, framework)
            )
            if action == "cancel":
                console.print("[yellow]Framework switch cancelled.[/yellow]")
                raise typer.Exit(0)
        else:
            # No customizations - simple confirmation
            if not questionary.confirm("Proceed with framework switch?", default=True).ask():
                console.print("[yellow]Framework switch cancelled.[/yellow]")
                raise typer.Exit(0)
            action = "replace"  # No customizations, so just replace

    else:
        # Non-interactive mode: backup and replace
        action = "replace"

    # Create timestamped backup directory
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup_dir = journal_path / ".framework-backups" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Execute the switch based on chosen action
    execute_framework_switch(
        journal_path=journal_path,
        framework=framework,
        action=action,
        customized_templates=customized_templates,
        backup_dir=backup_dir,
        manifest=manifest,
    )

    # Update config
    update_config(framework=framework)

    # Save manifest
    manifest.framework = framework
    manifest.save(manifest_path)

    # Success message
    show_success("Framework switched successfully!")
    console.print(
        f"\n[bold]New framework:[/bold] [green]{framework_names.get(framework, framework)}[/green]"
    )
    console.print("\n[dim]Your journal notes (daily/, projects/, etc.) are untouched.[/dim]\n")


def show_interactive_checklist(framework: str, framework_name: str, customized_count: int):
    """Show interactive checklist of what will happen during framework switch."""
    # Create checklist table
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Status", style="green")
    table.add_column("Description")

    # What WILL happen
    console.print("\n[bold]What will happen:[/bold]")
    table.add_row("✓", f"Templates will be replaced with {framework_name} templates")
    table.add_row("✓", "Your journal notes (daily/, projects/, people/) stay untouched")
    table.add_row("✓", "Old templates backed up to .framework-backups/")

    if customized_count > 0:
        table.add_row(
            "✓", f"{customized_count} customized template(s) detected - you'll choose what to do"
        )

    console.print(table)

    # What will NOT happen
    console.print("\n[bold]What will NOT happen:[/bold]")
    table_not = Table(show_header=False, box=None, padding=(0, 2))
    table_not.add_column("Status", style="red")
    table_not.add_column("Description")

    table_not.add_row("✗", "Your journal content will NOT be reorganized")
    table_not.add_row("✗", "Your existing notes will NOT be modified")
    table_not.add_row("✗", "Your .ai-instructions/ customizations will NOT be touched")

    console.print(table_not)
    console.print()


def ask_customization_resolution(customized_templates: list[Path], new_framework: str) -> str:
    """Ask user how to handle customized templates.

    Returns:
        Action to take: 'move', 'replace', or 'cancel'
    """
    console.print("[bold yellow]⚠ Customized templates detected:[/bold yellow]")
    for template in customized_templates:
        console.print(f"  • {template.name}")
    console.print()

    choices = [
        questionary.Choice(
            title="Move to .ai-instructions/templates/ (RECOMMENDED) - Keep customizations forever",
            value="move",
        ),
        questionary.Choice(
            title=f"Backup and replace - Start fresh with {new_framework} templates",
            value="replace",
        ),
        questionary.Choice(title="Cancel - Don't switch frameworks", value="cancel"),
    ]

    console.print("[bold]Choose what to do with your customizations:[/bold]\n")
    console.print("  [green]1. Move to .ai-instructions/templates/[/green]")
    console.print("     → Your templates will override new framework templates")
    console.print("     → Safe from all future framework switches")
    console.print("     → You keep your customizations forever")
    console.print()
    console.print("  [yellow]2. Backup and replace[/yellow]")
    console.print("     → Backed up to .framework-backups/")
    console.print(f"     → Start fresh with {new_framework} templates")
    console.print("     → You can restore from backup later")
    console.print()
    console.print("  [red]3. Cancel[/red]")
    console.print("     → No changes made")
    console.print()

    action = questionary.select(
        "Your choice:",
        choices=choices,
        default="move",
    ).ask()

    return action or "cancel"


def execute_framework_switch(
    journal_path: Path,
    framework: str,
    action: str,
    customized_templates: list[Path],
    backup_dir: Path,
    manifest: Manifest,
):
    """Execute the framework switch with chosen customization handling.

    Args:
        journal_path: Journal root directory
        framework: New framework to switch to
        action: 'move' or 'replace'
        customized_templates: List of customized template files
        backup_dir: Backup directory for old templates
        manifest: Manifest to update
    """
    all_templates = list(journal_path.glob("*-template.md"))

    # Backup all existing templates
    if all_templates:
        console.print(f"\n[cyan]Backing up {len(all_templates)} templates...[/cyan]")
        for template_file in all_templates:
            backup_path = backup_dir / template_file.name
            shutil.copy2(template_file, backup_path)

    # Handle customized templates based on action
    if action == "move" and customized_templates:
        # Move customized templates to .ai-instructions/templates/
        safe_dir = journal_path / ".ai-instructions" / "templates"
        safe_dir.mkdir(parents=True, exist_ok=True)

        console.print(
            f"\n[cyan]Moving {len(customized_templates)} customized templates to safe zone...[/cyan]"
        )
        for template_file in customized_templates:
            safe_path = safe_dir / template_file.name
            shutil.copy2(template_file, safe_path)
            console.print(f"  → {template_file.name} → .ai-instructions/templates/")

        console.print(
            "\n[green]✓[/green] Your customizations are now in [cyan].ai-instructions/templates/[/cyan]"
        )
        console.print("[dim]They will override framework templates when creating notes.[/dim]\n")

    # Install new framework templates
    console.print(f"[cyan]Installing {framework} templates...[/cyan]")
    copy_framework_templates(framework, journal_path)

    # Update manifest for all templates
    new_templates = list(journal_path.glob("*-template.md"))
    for template_file in new_templates:
        manifest.add_file(
            template_file,
            source=f"framework:{framework}",
            customized=False,
            relative_to=journal_path,
        )
