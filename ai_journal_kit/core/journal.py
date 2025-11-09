"""Journal structure creation and validation."""

import shutil
from importlib.resources import files
from pathlib import Path

from ai_journal_kit.core.templates import copy_template

REQUIRED_FOLDERS = [
    "daily",
    "projects",
    "areas",
    "resources",
    "people",
    "memories",
    "archive",
]


def create_structure(journal_path: Path, framework: str = "default"):
    """Create all required journal folders with framework-specific templates.

    Args:
        journal_path: Root journal directory
        framework: Journaling framework (default, gtd, para, bullet-journal, zettelkasten)
    """
    journal_path.mkdir(parents=True, exist_ok=True)

    for folder in REQUIRED_FOLDERS:
        folder_path = journal_path / folder
        folder_path.mkdir(exist_ok=True)

    # Create .ai-instructions directory for custom preferences
    (journal_path / ".ai-instructions").mkdir(exist_ok=True)

    # Copy WELCOME.md to journal root to guide new users
    copy_template("WELCOME.md", journal_path / "WELCOME.md")

    # Copy framework-specific templates if not using default
    if framework != "default":
        copy_framework_templates(framework, journal_path)


def copy_framework_templates(framework: str, journal_path: Path):
    """Copy framework-specific templates to journal.

    Args:
        framework: Framework name (gtd, para, bullet-journal, zettelkasten)
        journal_path: Root journal directory
    """
    template_base = files("ai_journal_kit.templates").joinpath("frameworks").joinpath(framework)
    template_dir = Path(str(template_base))

    if not template_dir.exists():
        # Framework templates don't exist yet - skip silently
        return

    # Copy all templates from framework directory to journal root
    for template_file in template_dir.glob("*.md"):
        dest_file = journal_path / template_file.name
        shutil.copy2(template_file, dest_file)


def validate_structure(journal_path: Path) -> tuple[bool, list[str]]:
    """Verify all required folders exist.

    Args:
        journal_path: Root journal directory

    Returns:
        Tuple of (all_present, missing_folders)
    """
    if not journal_path.exists():
        return False, REQUIRED_FOLDERS.copy()

    missing = []
    for folder in REQUIRED_FOLDERS:
        folder_path = journal_path / folder
        if not folder_path.exists():
            missing.append(folder)

    return len(missing) == 0, missing


def get_folder_stats(journal_path: Path) -> dict[str, int]:
    """Get file counts for each journal folder.

    Args:
        journal_path: Root journal directory

    Returns:
        Dictionary of folder_name: file_count
    """
    stats = {}
    for folder in REQUIRED_FOLDERS:
        folder_path = journal_path / folder
        if folder_path.exists():
            # Count markdown files only
            stats[folder] = len(list(folder_path.glob("*.md")))
        else:
            stats[folder] = 0
    return stats
