"""Journal structure creation and validation."""

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


def create_structure(journal_path: Path):
    """Create all required journal folders.

    Args:
        journal_path: Root journal directory
    """
    journal_path.mkdir(parents=True, exist_ok=True)

    for folder in REQUIRED_FOLDERS:
        folder_path = journal_path / folder
        folder_path.mkdir(exist_ok=True)

    # Create .ai-instructions directory for custom preferences
    (journal_path / ".ai-instructions").mkdir(exist_ok=True)

    # Copy WELCOME.md to journal root to guide new users
    copy_template("WELCOME.md", journal_path / "WELCOME.md")


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
