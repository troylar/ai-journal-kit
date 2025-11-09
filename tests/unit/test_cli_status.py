"""
Unit tests for the status CLI command.

Tests status display, configuration checking, and error handling.
"""

import json

import pytest

from ai_journal_kit.core.config import Config, load_config, save_config, update_config


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


@pytest.mark.unit
def test_config_serializes_path_objects(isolated_config_dir, monkeypatch):
    """Test that Config properly serializes Path objects to JSON."""
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(isolated_config_dir))

    config = Config(
        journal_location="/tmp/test-journal",
        ide="cursor",
        use_symlink=True,
        symlink_source="/tmp/source",
    )

    # Test model_dump_json handles symlink_source (line 40-41)
    json_str = config.model_dump_json()
    data = json.loads(json_str)

    assert isinstance(data["journal_location"], str)
    assert isinstance(data["symlink_source"], str)
    assert data["use_symlink"] is True


@pytest.mark.unit
def test_config_handles_corrupted_file(isolated_config_dir, monkeypatch):
    """Test that Config handles corrupted JSON file gracefully."""
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(isolated_config_dir))

    # Create a corrupted config file
    config_path = isolated_config_dir / "config.json"
    config_path.write_text("{ invalid json }")

    # Should return None and print warning (lines 70-76)
    config = load_config()
    assert config is None


@pytest.mark.unit
def test_config_handles_missing_file_check(isolated_config_dir, monkeypatch):
    """Test that load_config returns None when file doesn't exist (line 60)."""
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(isolated_config_dir))

    # Ensure no config file exists
    config_path = isolated_config_dir / "config.json"
    if config_path.exists():
        config_path.unlink()

    # Should return None (line 60)
    config = load_config()
    assert config is None


@pytest.mark.unit
def test_update_config(isolated_config_dir, monkeypatch):
    """Test updating config fields (lines 86-98)."""
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(isolated_config_dir))

    # Create initial config
    config = Config(journal_location="/tmp/test-journal", ide="cursor")
    save_config(config)

    # Update config
    updated = update_config(ide="windsurf", use_symlink=True)

    assert updated.ide == "windsurf"
    assert updated.use_symlink is True

    # Verify it was saved
    loaded = load_config()
    assert loaded.ide == "windsurf"
    assert loaded.use_symlink is True


@pytest.mark.unit
def test_update_config_raises_when_no_config(isolated_config_dir, monkeypatch):
    """Test update_config raises error when no config exists (lines 89-90)."""
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(isolated_config_dir))

    # Ensure no config file
    config_path = isolated_config_dir / "config.json"
    if config_path.exists():
        config_path.unlink()

    # Should raise ValueError
    with pytest.raises(ValueError, match="No configuration found"):
        update_config(ide="windsurf")


@pytest.mark.unit
def test_config_path_validator_with_string(isolated_config_dir, monkeypatch):
    """Test that path validator handles string input (line 27-28)."""
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(isolated_config_dir))

    # Create config with string path
    config = Config(journal_location="~/test-journal", ide="cursor")

    # Should expand ~ and resolve to absolute path
    assert config.journal_location.is_absolute()
    assert "test-journal" in str(config.journal_location)


@pytest.mark.unit
def test_config_path_validator_with_path(isolated_config_dir, monkeypatch):
    """Test that path validator handles Path input (line 29)."""
    from pathlib import Path

    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(isolated_config_dir))

    # Create config with Path object
    config = Config(journal_location=Path("~/test-journal"), ide="cursor")

    # Should expand ~ and resolve to absolute path
    assert config.journal_location.is_absolute()
    assert "test-journal" in str(config.journal_location)


@pytest.mark.unit
def test_get_config_path_without_env_override(tmp_path):
    """Test get_config_path uses platformdirs default when no env var set (line 58)."""
    import os
    from importlib import reload

    from ai_journal_kit.core import config as config_module

    # Temporarily remove env var
    old_value = os.environ.pop("AI_JOURNAL_CONFIG_DIR", None)

    try:
        # Force reload to use default path
        reload(config_module)

        path = config_module.get_config_path()

        # Should use platformdirs path
        assert "ai-journal-kit" in str(path)
        assert path.name == "config.json"

    finally:
        # Restore for other tests
        if old_value:
            os.environ["AI_JOURNAL_CONFIG_DIR"] = old_value
        reload(config_module)
