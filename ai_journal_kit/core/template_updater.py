"""Template update utilities for safely updating journal templates."""

import shutil
from datetime import datetime
from pathlib import Path

from rich.table import Table

from ai_journal_kit.utils.ui import console


def backup_template(template_path: Path) -> Path:
    """Create a timestamped backup of a template.

    Args:
        template_path: Path to template file

    Returns:
        Path to backup file
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{template_path.stem}.backup_{timestamp}{template_path.suffix}"
    backup_path = template_path.parent / backup_name

    shutil.copy2(template_path, backup_path)
    return backup_path


def get_template_changes(journal_path: Path) -> dict[str, dict]:
    """Check which templates have updates available.

    Args:
        journal_path: Path to journal root

    Returns:
        Dict mapping template names to change info
    """
    from ai_journal_kit.core.templates import get_template

    templates = [
        "daily-template.md",
        "project-template.md",
        "people-template.md",
        "memory-template.md",
        "WELCOME.md",
    ]

    changes = {}
    for template_name in templates:
        user_template = journal_path / template_name
        if not user_template.exists():
            continue

        try:
            package_template = get_template(template_name)
            if not package_template.exists():
                continue

            # Read both versions
            user_content = user_template.read_text()
            package_content = package_template.read_text()

            if user_content != package_content:
                changes[template_name] = {
                    "user_path": user_template,
                    "package_path": package_template,
                    "size_old": len(user_content),
                    "size_new": len(package_content),
                    "modified": user_template.stat().st_mtime,
                }
        except Exception:
            continue

    return changes


def show_template_changes(changes: dict[str, dict]) -> None:
    """Display a table of template changes.

    Args:
        changes: Dict of template changes from get_template_changes()
    """
    if not changes:
        console.print("✓ [green]All templates are up to date![/green]")
        return

    table = Table(title="📝 Available Template Updates", show_header=True)
    table.add_column("Template", style="cyan")
    table.add_column("Current Size", justify="right")
    table.add_column("New Size", justify="right")
    table.add_column("Last Modified")

    for name, info in changes.items():
        modified_date = datetime.fromtimestamp(info["modified"]).strftime("%Y-%m-%d")
        table.add_row(
            name,
            f"{info['size_old']} bytes",
            f"{info['size_new']} bytes",
            modified_date,
        )

    console.print(table)
    console.print()


def update_templates(journal_path: Path, backup: bool = True) -> list[str]:
    """Update all templates to latest versions.

    Args:
        journal_path: Path to journal root
        backup: Whether to backup existing templates

    Returns:
        List of updated template names
    """
    from ai_journal_kit.core.templates import copy_template

    changes = get_template_changes(journal_path)
    if not changes:
        return []

    updated = []
    for template_name, info in changes.items():
        user_path = info["user_path"]

        # Backup if requested
        if backup:
            backup_path = backup_template(user_path)
            console.print(f"  Backed up: [dim]{backup_path.name}[/dim]")

        # Update template
        copy_template(template_name, user_path)
        updated.append(template_name)
        console.print(f"  ✓ Updated: [green]{template_name}[/green]")

    return updated


def list_backups(journal_path: Path) -> list[Path]:
    """List all template backups in the journal.

    Args:
        journal_path: Path to journal root

    Returns:
        List of backup file paths
    """
    backups = []
    for file in journal_path.glob("*.backup_*"):
        if file.is_file() and file.suffix == ".md":
            backups.append(file)

    return sorted(backups, key=lambda p: p.stat().st_mtime, reverse=True)


def restore_template_backup(backup_path: Path) -> Path:
    """Restore a template from a backup.

    Args:
        backup_path: Path to backup file

    Returns:
        Path to restored template
    """
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup not found: {backup_path}")

    # Extract original name from backup name
    # Format: template-name.backup_20231107_123456.md
    name_part = backup_path.name.split(".backup_")[0]
    original_path = backup_path.parent / f"{name_part}.md"

    shutil.copy2(backup_path, original_path)
    return original_path
