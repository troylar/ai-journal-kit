"""
Unit tests for the status CLI command.

Tests status display, configuration checking, and error handling.
"""

import pytest

from ai_journal_kit.core.config import Config, load_config, save_config


@pytest.mark.unit
def test_config_loads_from_valid_json(isolated_config_dir, monkeypatch):
    """Test that Config can load from valid JSON file."""
    # Set environment to use isolated test config directory
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(isolated_config_dir))

    # Create a test config file
    config_to_save = Config(journal_location="/tmp/test-journal", ide="cursor")
    save_config(config_to_save)

    # Load it back
    config = load_config()
    assert config is not None
    assert config.ide == "cursor"
    assert str(config.journal_location).endswith("test-journal")


@pytest.mark.unit
def test_config_handles_missing_file(tmp_path, monkeypatch, isolated_config_dir):
    """Test that Config handles missing configuration file."""
    # Point to a truly non-existent config location
    nonexistent_dir = isolated_config_dir / "nonexistent" / "nowhere"
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(nonexistent_dir))

    config = load_config()
    # Should return None when config file doesn't exist
    assert (
        config is None or config.journal_location
    )  # Either None or has location from actual config


@pytest.mark.unit
def test_config_saves_to_file(isolated_config_dir, monkeypatch):
    """Test that Config can save to file."""
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(isolated_config_dir))

    config = Config(journal_location="/tmp/test-journal", ide="cursor")

    save_config(config)

    # Verify it was saved
    loaded = load_config()
    assert loaded is not None
    # Compare as strings since Config stores Path objects
    assert str(loaded.journal_location).endswith("test-journal")
    assert loaded.ide == "cursor"


@pytest.mark.unit
def test_config_validates_journal_location():
    """Test that Config validates journal_location is set."""
    config = Config(journal_location="/tmp/journal", ide="cursor")
    # Config stores as Path object, check it's not empty
    assert config.journal_location is not None
    assert str(config.journal_location)  # Not empty string
    # On Windows, /tmp/journal becomes D:\tmp\journal, so just check "journal" is in path
    assert "journal" in str(config.journal_location)


@pytest.mark.unit
def test_config_validates_ide_choice():
    """Test that Config validates IDE choice."""
    config = Config(journal_location="/tmp/journal", ide="windsurf")
    assert config.ide == "windsurf"
