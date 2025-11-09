"""
Journal factory fixture for creating configured test journals.

Provides a factory function to create journals with specific configurations
for testing purposes.
"""

from dataclasses import dataclass
from pathlib import Path

from ai_journal_kit.core.config import Config, save_config
from ai_journal_kit.core.journal import create_structure
from ai_journal_kit.core.templates import copy_ide_configs


@dataclass
class JournalFixture:
    """
    Represents a configured journal installation for testing.

    Attributes:
        path: Path to journal directory
        ide: IDE configuration installed
        config_path: Path to config file
        daily_notes_count: Number of daily notes created
    """

    path: Path
    ide: str
    config_path: Path
    daily_notes_count: int = 0

    @property
    def daily_dir(self) -> Path:
        """Get daily notes directory."""
        return self.path / "daily"

    @property
    def projects_dir(self) -> Path:
        """Get projects directory."""
        return self.path / "projects"

    @property
    def ide_config_dir(self) -> Path:
        """Get IDE config directory."""
        ide_paths = {
            "cursor": self.path / ".cursor" / "rules",
            "windsurf": self.path / ".windsurf" / "rules",
            "claude-code": self.path,  # CLAUDE.md is at root
            "copilot": self.path / ".github" / "instructions",
        }
        return ide_paths.get(self.ide, self.path)


def create_journal_fixture(
    path: Path,
    ide: str = "cursor",
    has_content: bool = False,
    config_dir: Path = None,
    framework: str = "default",
) -> JournalFixture:
    """
    Factory for creating configured journal installations.

    Args:
        path: Path where journal should be created
        ide: IDE to configure (cursor, windsurf, claude-code, copilot, all)
        has_content: Whether to add sample daily notes
        config_dir: Optional config directory path for config file
        framework: Journaling framework (default, gtd, para, bullet-journal, zettelkasten)

    Returns:
        JournalFixture: Configured journal for testing
    """
    # Create journal structure with framework
    create_structure(path, framework=framework)

    # Install IDE configs
    copy_ide_configs(ide, path)

    # Create config file
    config = Config(journal_location=path, ide=ide, framework=framework, version="1.0.0")

    if config_dir:
        # save_config() uses get_config_path() internally which reads AI_JOURNAL_CONFIG_DIR
        save_config(config)
        config_path = config_dir / "config.json"
    else:
        config_path = None

    # Optionally add sample content
    daily_notes_count = 0
    if has_content:
        daily_dir = path / "daily"
        for i in range(1, 4):  # Create 3 sample notes
            note_file = daily_dir / f"2025-01-{i:02d}.md"
            note_file.write_text(f"# Daily Note {i}\n\nSample content for testing.")
            daily_notes_count += 1

    return JournalFixture(
        path=path, ide=ide, config_path=config_path, daily_notes_count=daily_notes_count
    )
