"""
Config factory fixture for creating test configurations.

Provides utilities for creating and manipulating Config objects for testing.
"""

from pathlib import Path

from ai_journal_kit.core.config import Config, save_config


def create_config_fixture(
    journal_location: Path, ide: str = "cursor", version: str = "1.0.0", config_dir: Path = None
) -> Config:
    """
    Factory for creating Config objects for testing.

    Args:
        journal_location: Path to journal directory
        ide: IDE configuration (cursor, windsurf, claude-code, copilot, all)
        version: Version string
        config_dir: Optional directory to save config file

    Returns:
        Config: Configured Config object
    """
    config = Config(journal_location=journal_location, ide=ide, version=version)

    if config_dir:
        # save_config() uses get_config_path() internally which reads AI_JOURNAL_CONFIG_DIR
        save_config(config)

    return config


def create_corrupted_config(config_dir: Path) -> Path:
    """
    Create a corrupted config file for testing error handling.

    Args:
        config_dir: Directory to create corrupted config

    Returns:
        Path: Path to corrupted config file
    """
    config_path = config_dir / "config.json"
    config_path.write_text("{invalid json content}")
    return config_path


def create_incomplete_config(config_dir: Path) -> Path:
    """
    Create an incomplete config file for testing validation.

    Args:
        config_dir: Directory to create incomplete config

    Returns:
        Path: Path to incomplete config file
    """
    config_path = config_dir / "config.json"
    config_path.write_text('{"journal_location": "/tmp/journal"}')  # Missing ide
    return config_path
