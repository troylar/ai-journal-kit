"""Setup command for first-time journal installation."""

from pathlib import Path

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_journal_kit import __version__
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


def _detect_existing_journal(path: Path) -> dict[str, bool]:
    """Detect existing journal content at the specified path.

    Args:
        path: Path to check for existing journal content

    Returns:
        Dictionary with detected content types (empty if nothing found)
    """
    detected = {}

    # Check for journal structure folders
    journal_folders = ["daily", "projects", "people", "memories", "areas", "resources", "archive"]
    for folder in journal_folders:
        if (path / folder).exists():
            detected[f"folder_{folder}"] = True

    # Check for IDE configurations
    if (path / ".cursor").exists():
        detected["ide_cursor"] = True
    if (path / ".windsurf").exists():
        detected["ide_windsurf"] = True
    if (path / "CLAUDE.md").exists() or (path / "SYSTEM-PROTECTION.md").exists():
        detected["ide_claude_code"] = True
    if (path / ".github" / "instructions").exists():
        detected["ide_copilot"] = True

    # Check for templates
    if list(path.glob("*-template.md")):
        detected["templates"] = True

    # Check for .ai-instructions (user customizations)
    if (path / ".ai-instructions").exists():
        detected["customizations"] = True

    return detected


def _handle_existing_journal(
    path: Path,
    detected: dict[str, bool],
    no_confirm: bool,
    location: str,
    name: str,
) -> dict[str, str | None]:
    """Handle setup when existing journal content is detected.

    Args:
        path: Journal path
        detected: Dictionary of detected content
        no_confirm: Whether running in no-confirm mode
        location: Original location string (for messaging)
        name: Journal name

    Returns:
        Dictionary with detected IDE and framework (or None if not detected)

    Raises:
        typer.Exit: If user cancels
    """
    # Build message describing what was found
    found_items = []

    # Journal folders
    folder_count = sum(1 for k in detected if k.startswith("folder_"))
    if folder_count > 0:
        found_items.append(f"{folder_count} journal folder(s)")

    # IDE configs
    ide_configs = [
        k.replace("ide_", "").replace("_", " ") for k in detected if k.startswith("ide_")
    ]
    if ide_configs:
        found_items.append(f"IDE config(s): {', '.join(ide_configs)}")

    # Templates
    if detected.get("templates"):
        found_items.append("template files")

    # Customizations
    if detected.get("customizations"):
        found_items.append("user customizations (.ai-instructions/)")

    message = f"""[bold yellow]⚠️  Existing Journal Detected[/bold yellow]

The path [cyan]{path}[/cyan] already contains:
"""

    for item in found_items:
        message += f"\n• {item}"

    message += """

[bold]What will happen if you proceed:[/bold]
• Journal folders will be preserved (your content is safe)
• IDE configurations will be reinstalled (any customizations should be in .ai-instructions/)
• Templates will be overwritten with selected framework templates
• User customizations in .ai-instructions/ will be preserved

[bold]Options:[/bold]
1. Proceed with re-installation (update this journal)
2. Cancel and change the path to create a new journal elsewhere
"""

    if detected.get("customizations"):
        message += "\n[dim]Note: Your .ai-instructions/ customizations will be preserved[/dim]"

    show_panel(message, title="Existing Journal", border_style="yellow")

    # Handle confirmation based on mode
    if no_confirm:
        # In no-confirm mode, show warning but proceed
        console.print(
            "[yellow]⚠️  Running in --no-confirm mode. Proceeding with setup...[/yellow]\n"
        )
    else:
        # Interactive mode - ask user
        proceed = confirm("Proceed with re-installation at this location?")
        if not proceed:
            console.print(
                "\n[yellow]Setup cancelled.[/yellow]\n\n"
                "[bold]To create a new journal:[/bold]\n"
                f"  1. Choose a different path: [cyan]ai-journal-kit setup --location ~/new-journal[/cyan]\n"
                f"  2. Or use a different name: [cyan]ai-journal-kit setup --name {name}-new[/cyan]\n"
            )
            raise typer.Exit(0)

    # Detect existing IDE (if any) and return it
    detected_ide = None
    if detected.get("ide_cursor"):
        detected_ide = "cursor"
    elif detected.get("ide_windsurf"):
        detected_ide = "windsurf"
    elif detected.get("ide_claude_code"):
        detected_ide = "claude-code"
    elif detected.get("ide_copilot"):
        detected_ide = "copilot"

    return {"detected_ide": detected_ide, "is_reinstall": True}


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

        # Check for existing journal content
        existing_info = {"detected_ide": None, "is_reinstall": False}
        if journal_path.exists():
            existing_content = _detect_existing_journal(journal_path)
            if existing_content and not dry_run:
                existing_info = _handle_existing_journal(
                    journal_path, existing_content, no_confirm, location, name
                )

    except ValueError as e:
        show_error(str(e), "Please provide a valid filesystem path.")
        raise typer.Exit(1)

    # IDE selection - use detected IDE if available
    if ide is None:
        if existing_info["detected_ide"] and not no_confirm:
            # Ask if they want to keep existing IDE or change it
            keep_ide = confirm(
                f"Keep existing IDE configuration ({existing_info['detected_ide']})?"
            )
            if keep_ide:
                ide = existing_info["detected_ide"]
            else:
                ide = ask_ide("Which AI editor would you like to use instead?")
        else:
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

    # Determine action message based on whether it's a reinstall
    action_message = (
        "This will update your journal structure and reinstall AI coaching configurations."
        if existing_info["is_reinstall"]
        else "This will create your journal structure and install AI coaching configurations."
    )

    summary = f"""[bold cyan]Setup Configuration[/bold cyan]

• Journal Location: [yellow]{journal_path}[/yellow]
• Framework: [yellow]{framework_names.get(framework, framework)}[/yellow]
• AI Editor: [yellow]{ide}[/yellow]
• Config File: [yellow]{get_config_path()}[/yellow]

{action_message}
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
            copy_ide_configs(ide, journal_path, framework=framework)
            progress.update(task2, completed=True)

            # Create journal profile
            task3 = progress.add_task("Saving configuration...", total=None)
            profile = JournalProfile(
                name=name,
                location=journal_path,
                ide=ide,
                framework=framework,
                version=__version__,
            )
            multi_config.add_journal(profile)

            # Set as active if it's the first/only journal
            if len(multi_config.journals) == 1:
                multi_config.set_active(name)

            save_multi_journal_config(multi_config)
            progress.update(task3, completed=True)

            # Create initial manifest to track installed files
            task4 = progress.add_task("Creating system manifest...", total=None)
            manifest = Manifest(version=__version__, framework=framework)

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
