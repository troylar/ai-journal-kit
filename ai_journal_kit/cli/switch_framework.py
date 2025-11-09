"""Switch framework command for changing journaling methodology."""

from datetime import datetime

import typer

from ai_journal_kit.core.config import load_config, update_config
from ai_journal_kit.core.journal import copy_framework_templates
from ai_journal_kit.core.validation import validate_framework
from ai_journal_kit.utils.ui import ask_framework, confirm, console, show_error, show_success


def switch_framework(
    framework: str = typer.Argument(
        None,
        help="Framework to switch to: default/gtd/para/bullet-journal/zettelkasten",
    ),
    no_confirm: bool = typer.Option(False, "--no-confirm", help="Skip confirmation prompt"),
):
    """Switch to a different journaling framework.

    This command allows you to change your journaling framework after setup.
    All existing templates will be backed up with a timestamp before switching.

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

    # Show summary
    framework_names = {
        "default": "Default (flexible)",
        "gtd": "GTD (Getting Things Done)",
        "para": "PARA (Projects, Areas, Resources, Archive)",
        "bullet-journal": "Bullet Journal",
        "zettelkasten": "Zettelkasten",
    }

    console.print("\n[bold cyan]Framework Switch[/bold cyan]\n")
    console.print(f"  Current:  [yellow]{framework_names.get(current_framework, current_framework)}[/yellow]")
    console.print(f"  New:      [green]{framework_names.get(framework, framework)}[/green]\n")
    console.print("[dim]Your templates will be backed up before switching.[/dim]\n")

    # Confirmation
    if not no_confirm:
        proceed = confirm("Proceed with framework switch?")
        if not proceed:
            console.print("[yellow]Framework switch cancelled.[/yellow]")
            raise typer.Exit(0)

    # Create timestamped backup directory with microseconds to ensure uniqueness
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup_dir = journal_path / ".framework-backups" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Backup existing templates
    backed_up_files = []
    template_files = list(journal_path.glob("*-template.md"))

    if template_files:
        console.print(f"\n[cyan]Backing up {len(template_files)} existing templates...[/cyan]")
        for template_file in template_files:
            backup_path = backup_dir / template_file.name
            backup_path.write_text(template_file.read_text(encoding="utf-8"), encoding="utf-8")
            backed_up_files.append(template_file.name)

    # Copy new framework templates
    console.print(f"[cyan]Installing {framework} templates...[/cyan]")
    try:
        copy_framework_templates(framework, journal_path)
    except Exception as e:
        show_error("Failed to install templates", str(e))
        raise typer.Exit(1)

    # Update config
    update_config(framework=framework)

    # Success message
    show_success("Framework switched successfully!")

    if backed_up_files:
        console.print("\n[bold]Backed up templates:[/bold]")
        console.print(f"  Location: [cyan]{backup_dir}[/cyan]")
        console.print(f"  Files: {len(backed_up_files)}")
        for filename in backed_up_files:
            console.print(f"    • {filename}")

    console.print(f"\n[bold]New framework:[/bold] [green]{framework_names.get(framework, framework)}[/green]")
    console.print("\n[dim]Your journal notes (daily/, projects/, etc.) are untouched.[/dim]\n")
