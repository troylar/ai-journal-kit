"""Migration utilities for upgrading existing journals to new versions."""

from ai_journal_kit.core.config import load_config
from ai_journal_kit.core.manifest import Manifest


def migrate_to_manifest_system() -> bool:
    """Migrate existing journal to use manifest tracking system.

    This runs automatically when a journal is detected without a manifest.
    Safe to run multiple times (idempotent).

    Returns:
        True if migration was performed, False if not needed
    """
    config = load_config()
    if not config:
        return False  # No journal setup yet

    journal_path = config.journal_location
    manifest_path = journal_path / ".system-manifest.json"

    # Check if manifest already exists
    if manifest_path.exists():
        return False  # Already migrated

    # Check if journal actually exists
    if not journal_path.exists():
        return False  # Journal doesn't exist

    # Create manifest for existing journal
    manifest = Manifest(version="1.0.0", framework=config.framework)

    # Track all existing templates
    for template_file in journal_path.glob("*-template.md"):
        manifest.add_file(
            template_file,
            source=f"framework:{config.framework}",
            customized=False,  # Assume not customized initially
            relative_to=journal_path,
        )

    # Save manifest
    manifest.save(manifest_path)

    return True  # Migration performed


def ensure_manifest_exists() -> None:
    """Ensure manifest exists for current journal, migrating if necessary.

    Call this from any command that needs manifest support.
    Silent no-op if not needed.
    """
    migrate_to_manifest_system()
