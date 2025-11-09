"""Setup command for first-time journal installation."""

from pathlib import Path

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_journal_kit.core.config import (
    JournalProfile,
    load_multi_journal_config,
    save_multi_journal_config,
)
from ai_journal_kit.core.journal import create_structure
from ai_journal_kit.core.manifest import Manifest
from ai_journal_kit.core.templates import copy_ide_configs
from ai_journal_kit.core.validation import validate_framework, validate_ide, validate_path
from ai_journal_kit.utils.ui import (
    ask_framework,
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
    framework: str = typer.Option(
        None,
        "--framework",
        "-f",
        help="Journaling framework: default/gtd/para/bullet-journal/zettelkasten",
    ),
    name: str = typer.Option(
        None,
        "--name",
        "-n",
        help="Name for this journal (for multiple journals). Defaults to 'default'",
    ),
    no_confirm: bool = typer.Option(False, "--no-confirm", help="Skip confirmation prompt"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be done without doing it"
    ),
):
    """Set up your AI journal for the first time.

    Interactive setup that guides you through:
    - Choosing journal location (local or cloud)
    - Selecting journaling framework
    - Selecting your AI editor
    - Creating journal structure
    - Installing AI coach configurations
    """
    # Load existing multi-journal config
    multi_config = load_multi_journal_config()
    if multi_config is None:
        # First journal setup - create new multi-config
        from ai_journal_kit.core.config import MultiJournalConfig

        multi_config = MultiJournalConfig()

    # Determine journal name
    if name is None:
        # Default to "default" for first journal, otherwise prompt
        if not multi_config.journals:
            name = "default"
        else:
            # Multiple journals exist - require name
            if not no_confirm and not dry_run:
                name = typer.prompt("Journal name")
            else:
                show_error(
                    "Journal name required",
                    "Use --name to specify a name for additional journals",
                )
                raise typer.Exit(1)

    # Check if journal with this name already exists
    if multi_config.has_journal(name) and not dry_run:
        profile = multi_config.journals[name]
        show_error(
            f"Journal '{name}' already exists at {profile.location}",
            f"Choose a different name or use: ai-journal-kit use {name}",
        )
        raise typer.Exit(1)

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
            elif no_confirm:
                # Auto-create parent when no-confirm is set
                journal_path.parent.mkdir(parents=True, exist_ok=True)
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

    # Framework selection - default to "default" if not provided
    if framework is None:
        # Only prompt in interactive mode (no --no-confirm)
        if not no_confirm and not dry_run:
            framework = ask_framework()
        else:
            # Use default framework for non-interactive setups
            framework = "default"

    # Validate framework
    try:
        framework = validate_framework(framework)
    except ValueError as e:
        show_error(str(e))
        raise typer.Exit(1)

    # Show summary
    from ai_journal_kit.core.config import get_config_path

    # Get framework display name
    framework_names = {
        "default": "Default (flexible)",
        "gtd": "GTD (Getting Things Done)",
        "para": "PARA (Projects, Areas, Resources, Archive)",
        "bullet-journal": "Bullet Journal",
        "zettelkasten": "Zettelkasten",
    }

    summary = f"""[bold cyan]Setup Configuration[/bold cyan]

• Journal Location: [yellow]{journal_path}[/yellow]
• Framework: [yellow]{framework_names.get(framework, framework)}[/yellow]
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
            create_structure(journal_path, framework=framework)
            progress.update(task1, completed=True)

            # Install IDE configs
            task2 = progress.add_task(f"Installing {ide} configuration...", total=None)
            copy_ide_configs(ide, journal_path)
            progress.update(task2, completed=True)

            # Create journal profile
            task3 = progress.add_task("Saving configuration...", total=None)
            profile = JournalProfile(
                name=name,
                location=journal_path,
                ide=ide,
                framework=framework,
                version="1.0.0",
            )
            multi_config.add_journal(profile)

            # Set as active if it's the first/only journal
            if len(multi_config.journals) == 1:
                multi_config.set_active(name)

            save_multi_journal_config(multi_config)
            progress.update(task3, completed=True)

            # Create initial manifest to track installed files
            task4 = progress.add_task("Creating system manifest...", total=None)
            manifest = Manifest(version="1.0.0", framework=framework)

            # Track all installed templates
            for template_file in journal_path.glob("*-template.md"):
                manifest.add_file(
                    template_file,
                    source=f"framework:{framework}",
                    customized=False,
                    relative_to=journal_path,
                )

            # Save manifest
            manifest_path = journal_path / ".system-manifest.json"
            manifest.save(manifest_path)
            progress.update(task4, completed=True)

        # Success message
        show_success("Setup complete!")
        console.print("\n[bold]Next steps:[/bold]")
        console.print(f"1. Open [cyan]{journal_path}[/cyan] in your IDE")
        console.print("2. Start journaling with your AI coach")
        console.print("3. Check status anytime: [cyan]ai-journal-kit status[/cyan]\n")

    except Exception as e:
        show_error(f"Setup failed: {e}")
        raise typer.Exit(1)
