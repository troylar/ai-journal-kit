"""
Unit tests for config persistence.

Tests that config files are saved and loaded correctly,
especially focusing on the macOS platform directory issue.
"""

from datetime import datetime
from pathlib import Path

import pytest

from ai_journal_kit.core.config import (
    JournalProfile,
    MultiJournalConfig,
    get_config_path,
    load_multi_journal_config,
    save_multi_journal_config,
)


@pytest.mark.unit
def test_get_config_path_uses_platformdirs():
    """Test get_config_path returns correct platform-specific path."""
    config_path = get_config_path()

    # Should be under platformdirs location
    assert config_path.name == "config.json"
    assert "ai-journal-kit" in str(config_path)


@pytest.mark.unit
def test_save_and_load_multi_journal_config_roundtrip(tmp_path, monkeypatch):
    """Test saving and loading multi-journal config preserves all data."""
    # Mock config path to use tmp directory
    config_path = tmp_path / "config.json"
    monkeypatch.setattr("ai_journal_kit.core.config.get_config_path", lambda: config_path)

    # Create test profile
    profile = JournalProfile(
        name="test",
        location=Path("/test/journal"),
        ide="cursor",
        framework="gtd",
        version="1.0.0",
        created_at=datetime(2025, 1, 1, 10, 0, 0),
        last_updated=datetime(2025, 1, 2, 10, 0, 0),
        use_symlink=False,
        symlink_source=None,
    )

    # Create multi-journal config
    multi_config = MultiJournalConfig(
        active_journal="test",
        journals={"test": profile},
    )

    # Save config
    save_multi_journal_config(multi_config)

    # Verify file was created
    assert config_path.exists()

    # Load config
    loaded_config = load_multi_journal_config()

    # Verify loaded config matches original
    assert loaded_config is not None
    assert loaded_config.active_journal == "test"
    assert "test" in loaded_config.journals

    loaded_profile = loaded_config.journals["test"]
    assert loaded_profile.name == "test"
    assert loaded_profile.location == Path("/test/journal")
    assert loaded_profile.ide == "cursor"
    assert loaded_profile.framework == "gtd"


@pytest.mark.unit
def test_save_config_creates_parent_directory(tmp_path, monkeypatch):
    """Test save_config creates parent directory if it doesn't exist."""
    # Mock config path to use non-existent directory
    config_path = tmp_path / "nonexistent" / "config.json"
    monkeypatch.setattr("ai_journal_kit.core.config.get_config_path", lambda: config_path)

    assert not config_path.parent.exists()

    # Create and save config
    profile = JournalProfile(
        name="test",
        location=Path("/test/journal"),
        ide="cursor",
        framework="default",
    )
    multi_config = MultiJournalConfig(
        active_journal="test",
        journals={"test": profile},
    )

    save_multi_journal_config(multi_config)

    # Verify directory was created
    assert config_path.parent.exists()
    assert config_path.exists()


@pytest.mark.unit
def test_load_config_returns_none_if_not_exists(tmp_path, monkeypatch):
    """Test load_config returns None if config file doesn't exist."""
    # Mock config path to non-existent file
    config_path = tmp_path / "nonexistent.json"
    monkeypatch.setattr("ai_journal_kit.core.config.get_config_path", lambda: config_path)

    config = load_multi_journal_config()

    assert config is None


@pytest.mark.unit
def test_load_config_handles_corrupted_json(tmp_path, monkeypatch):
    """Test load_config returns None for corrupted JSON."""
    # Mock config path
    config_path = tmp_path / "config.json"
    monkeypatch.setattr("ai_journal_kit.core.config.get_config_path", lambda: config_path)

    # Write corrupted JSON
    config_path.write_text("{ invalid json")

    config = load_multi_journal_config()

    assert config is None


@pytest.mark.unit
def test_save_config_handles_datetime_serialization(tmp_path, monkeypatch):
    """Test save_config correctly serializes datetime objects."""
    config_path = tmp_path / "config.json"
    monkeypatch.setattr("ai_journal_kit.core.config.get_config_path", lambda: config_path)

    # Create profile with specific datetimes
    profile = JournalProfile(
        name="test",
        location=Path("/test/journal"),
        ide="cursor",
        framework="default",
        created_at=datetime(2025, 1, 1, 12, 30, 45),
        last_updated=datetime(2025, 1, 2, 14, 20, 30),
    )

    multi_config = MultiJournalConfig(
        active_journal="test",
        journals={"test": profile},
    )

    save_multi_journal_config(multi_config)

    # Verify datetimes are ISO format strings in JSON
    import json

    data = json.loads(config_path.read_text())

    assert data["journals"]["test"]["created_at"] == "2025-01-01T12:30:45"
    assert data["journals"]["test"]["last_updated"] == "2025-01-02T14:20:30"


@pytest.mark.unit
def test_load_config_parses_datetime_strings(tmp_path, monkeypatch):
    """Test load_config correctly parses ISO datetime strings."""
    config_path = tmp_path / "config.json"
    monkeypatch.setattr("ai_journal_kit.core.config.get_config_path", lambda: config_path)

    # Create JSON with datetime strings
    import json

    data = {
        "active_journal": "test",
        "journals": {
            "test": {
                "name": "test",
                "location": "/test/journal",
                "ide": "cursor",
                "framework": "default",
                "version": "1.0.0",
                "created_at": "2025-01-01T12:30:45",
                "last_updated": "2025-01-02T14:20:30",
                "use_symlink": False,
            }
        },
    }
    config_path.write_text(json.dumps(data))

    # Load config
    config = load_multi_journal_config()

    assert config is not None
    profile = config.journals["test"]
    assert profile.created_at == datetime(2025, 1, 1, 12, 30, 45)
    assert profile.last_updated == datetime(2025, 1, 2, 14, 20, 30)


@pytest.mark.unit
def test_config_persists_across_multiple_operations(tmp_path, monkeypatch):
    """Test config survives multiple save/load cycles."""
    config_path = tmp_path / "config.json"
    monkeypatch.setattr("ai_journal_kit.core.config.get_config_path", lambda: config_path)

    # Create initial config
    profile1 = JournalProfile(
        name="journal1",
        location=Path("/test/journal1"),
        ide="cursor",
        framework="gtd",
    )

    multi_config = MultiJournalConfig(
        active_journal="journal1",
        journals={"journal1": profile1},
    )

    # Save
    save_multi_journal_config(multi_config)

    # Load and add another journal
    loaded = load_multi_journal_config()
    assert loaded is not None

    profile2 = JournalProfile(
        name="journal2",
        location=Path("/test/journal2"),
        ide="windsurf",
        framework="para",
    )
    loaded.journals["journal2"] = profile2

    # Save again
    save_multi_journal_config(loaded)

    # Load again and verify both journals exist
    final = load_multi_journal_config()
    assert final is not None
    assert len(final.journals) == 2
    assert "journal1" in final.journals
    assert "journal2" in final.journals


@pytest.mark.unit
def test_config_path_expansion(tmp_path, monkeypatch):
    """Test that ~ in paths gets expanded correctly."""
    config_path = tmp_path / "config.json"
    monkeypatch.setattr("ai_journal_kit.core.config.get_config_path", lambda: config_path)

    # Create profile with ~ in path
    import json

    data = {
        "active_journal": "test",
        "journals": {
            "test": {
                "name": "test",
                "location": "~/test/journal",  # Using ~ which should be expanded
                "ide": "cursor",
                "framework": "default",
                "version": "1.0.0",
                "created_at": "2025-01-01T12:00:00",
                "last_updated": "2025-01-01T12:00:00",
                "use_symlink": False,
            }
        },
    }
    config_path.write_text(json.dumps(data))

    # Load config
    config = load_multi_journal_config()

    assert config is not None
    profile = config.journals["test"]

    # Path should be absolute, not contain ~
    assert profile.location.is_absolute()
    assert "~" not in str(profile.location)
