"""Customize template command for safely overriding framework templates."""

import shutil

import typer

from ai_journal_kit.core.config import load_config
from ai_journal_kit.core.migration import ensure_manifest_exists
from ai_journal_kit.core.templates import resolve_template
from ai_journal_kit.utils.ui import console, show_error, show_success


def customize_template(
    template_name: str = typer.Argument(
        ...,
        help="Template to customize (e.g., 'daily-template.md', 'project-template.md')",
    ),
):
    """Copy a template to .ai-instructions/templates/ for safe customization.

    This command copies a framework template to your .ai-instructions/templates/
    folder, where you can customize it without fear of losing changes during
    framework switches or updates.

    Your customized template will always override the framework template.

    Examples:
        ai-journal-kit customize-template daily-template.md
        ai-journal-kit customize-template project-template.md
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

    # Ensure template name ends with .md
    if not template_name.endswith(".md"):
        template_name = f"{template_name}.md"

    # Ensure template name ends with -template.md
    if not template_name.endswith("-template.md"):
        template_name = template_name.replace(".md", "-template.md")

    # Resolve the template (find it in journal, framework, or package)
    source_template = resolve_template(template_name, journal_path)

    if not source_template or not source_template.exists():
        show_error(
            f"Template not found: {template_name}",
            "Available templates: daily-template.md, project-template.md, etc.",
        )
        raise typer.Exit(1)

    # Create .ai-instructions/templates/ directory
    custom_dir = journal_path / ".ai-instructions" / "templates"
    custom_dir.mkdir(parents=True, exist_ok=True)

    # Destination path
    dest_template = custom_dir / template_name

    # Check if already customized
    if dest_template.exists():
        console.print(f"\n[yellow]⚠ Template already customized:[/yellow] {template_name}")
        console.print(f"Location: [cyan]{dest_template}[/cyan]")
        console.print("\nYour existing customization is safe. No changes made.\n")
        raise typer.Exit(0)

    # Copy template to safe zone
    shutil.copy2(source_template, dest_template)

    # Success message
    show_success("Template ready for customization!")

    console.print("\n[bold]Template copied:[/bold]")
    console.print(f"  From: [dim]{source_template}[/dim]")
    console.print(f"  To:   [cyan]{dest_template}[/cyan]")

    console.print("\n[bold]What this means:[/bold]")
    console.print("  ✓ Your customization is now in a safe zone (.ai-instructions/templates/)")
    console.print("  ✓ This template will override framework templates when creating notes")
    console.print("  ✓ Safe from ALL framework switches and updates")
    console.print("  ✓ Edit freely without fear of losing changes")

    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  1. Open [cyan]{dest_template}[/cyan] in your editor")
    console.print("  2. Customize the template to your liking")
    console.print("  3. Save and start using your customized template\n")
