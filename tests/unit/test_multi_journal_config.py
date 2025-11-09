"""Unit tests for multi-journal configuration."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from ai_journal_kit.core.config import (
    JournalProfile,
    MultiJournalConfig,
    get_active_journal_name,
    load_multi_journal_config,
    migrate_legacy_config,
    save_multi_journal_config,
)


def test_journal_profile_creation():
    """Test creating a journal profile."""
    profile = JournalProfile(
        name="test",
        location=Path("/tmp/test"),
        ide="cursor",
        framework="gtd",
    )

    assert profile.name == "test"
    # Paths are resolved, so compare resolved versions
    assert profile.location == Path("/tmp/test").resolve()
    assert profile.ide == "cursor"
    assert profile.framework == "gtd"
    assert profile.version  # Just check it exists, don't hardcode version


def test_journal_profile_path_expansion():
    """Test that paths are expanded and resolved."""
    profile = JournalProfile(
        name="test",
        location="~/test-journal",
        ide="cursor",
    )

    # Should expand ~ to home directory
    assert not str(profile.location).startswith("~")
    assert profile.location.is_absolute()


def test_multi_journal_config_add_journal():
    """Test adding journals to config."""
    config = MultiJournalConfig()

    profile1 = JournalProfile(name="personal", location=Path("/tmp/personal"), ide="cursor")
    profile2 = JournalProfile(name="business", location=Path("/tmp/business"), ide="windsurf")

    config.add_journal(profile1)
    config.add_journal(profile2)

    assert len(config.journals) == 2
    assert "personal" in config.journals
    assert "business" in config.journals


def test_multi_journal_config_get_active_profile():
    """Test getting the active journal profile."""
    config = MultiJournalConfig(active_journal="personal")

    profile = JournalProfile(name="personal", location=Path("/tmp/personal"), ide="cursor")
    config.add_journal(profile)

    active = config.get_active_profile()
    assert active is not None
    assert active.name == "personal"


def test_multi_journal_config_set_active():
    """Test setting the active journal."""
    config = MultiJournalConfig()

    profile1 = JournalProfile(name="personal", location=Path("/tmp/personal"), ide="cursor")
    profile2 = JournalProfile(name="business", location=Path("/tmp/business"), ide="cursor")

    config.add_journal(profile1)
    config.add_journal(profile2)

    config.set_active("business")
    assert config.active_journal == "business"


def test_multi_journal_config_set_active_nonexistent():
    """Test setting active journal to non-existent name raises error."""
    config = MultiJournalConfig()

    with pytest.raises(ValueError, match="not found"):
        config.set_active("nonexistent")


def test_multi_journal_config_remove_journal():
    """Test removing a journal."""
    config = MultiJournalConfig(active_journal="personal")

    profile1 = JournalProfile(name="personal", location=Path("/tmp/personal"), ide="cursor")
    profile2 = JournalProfile(name="business", location=Path("/tmp/business"), ide="cursor")

    config.add_journal(profile1)
    config.add_journal(profile2)

    config.remove_journal("business")

    assert len(config.journals) == 1
    assert "business" not in config.journals
    assert "personal" in config.journals


def test_multi_journal_config_remove_active_switches_to_another():
    """Test that removing active journal switches to another one."""
    config = MultiJournalConfig(active_journal="personal")

    profile1 = JournalProfile(name="personal", location=Path("/tmp/personal"), ide="cursor")
    profile2 = JournalProfile(name="business", location=Path("/tmp/business"), ide="cursor")

    config.add_journal(profile1)
    config.add_journal(profile2)

    config.remove_journal("personal")

    # Should switch to the other journal
    assert config.active_journal == "business"


def test_migrate_legacy_config():
    """Test migrating old single-journal config to multi-journal format."""

    legacy_data = {
        "journal_location": "/tmp/test-journal",
        "ide": "cursor",
        "framework": "gtd",
        "version": "1.0.0",
        "created_at": datetime(2025, 1, 9, 10, 0, 0),
        "last_updated": datetime(2025, 1, 9, 10, 0, 0),
        "use_symlink": False,
        "symlink_source": None,
    }

    multi_config = migrate_legacy_config(legacy_data)

    # Check type name instead of isinstance for Python 3.10 compatibility
    assert type(multi_config).__name__ == "MultiJournalConfig"
    assert len(multi_config.journals) == 1
    assert "default" in multi_config.journals
    assert multi_config.active_journal == "default"

    profile = multi_config.journals["default"]
    assert profile.location == Path("/tmp/test-journal").resolve()
    assert profile.ide == "cursor"
    assert profile.framework == "gtd"


def test_save_and_load_multi_journal_config(tmp_path, monkeypatch):
    """Test saving and loading multi-journal config."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(config_dir))

    # Create config
    config = MultiJournalConfig(active_journal="personal")
    profile = JournalProfile(
        name="personal",
        location=Path("/tmp/test"),
        ide="cursor",
        framework="gtd",
    )
    config.add_journal(profile)

    # Save
    save_multi_journal_config(config)

    # Load
    loaded_config = load_multi_journal_config()

    assert loaded_config is not None
    assert loaded_config.active_journal == "personal"
    assert len(loaded_config.journals) == 1
    assert "personal" in loaded_config.journals

    loaded_profile = loaded_config.journals["personal"]
    assert loaded_profile.location == Path("/tmp/test").resolve()
    assert loaded_profile.ide == "cursor"
    assert loaded_profile.framework == "gtd"


def test_load_multi_journal_config_migrates_legacy(tmp_path, monkeypatch):
    """Test that loading legacy config auto-migrates to multi-journal format."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = config_dir / "config.json"
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(config_dir))

    # Write legacy config
    legacy_config = {
        "journal_location": str(tmp_path / "journal"),
        "ide": "cursor",
        "framework": "default",
        "version": "1.0.0",
        "created_at": "2025-01-09T10:00:00",
        "last_updated": "2025-01-09T10:00:00",
        "use_symlink": False,
    }
    config_path.write_text(json.dumps(legacy_config))

    # Load - should auto-migrate
    multi_config = load_multi_journal_config()

    assert multi_config is not None
    assert len(multi_config.journals) == 1
    assert "default" in multi_config.journals
    assert multi_config.active_journal == "default"

    # Verify migrated config was saved
    loaded_data = json.loads(config_path.read_text())
    assert "journals" in loaded_data
    assert "active_journal" in loaded_data


def test_get_active_journal_name_env_override(tmp_path, monkeypatch):
    """Test that AI_JOURNAL env var overrides active journal."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(config_dir))

    # Create config with personal as active
    config = MultiJournalConfig(active_journal="personal")
    profile1 = JournalProfile(name="personal", location=Path("/tmp/personal"), ide="cursor")
    profile2 = JournalProfile(name="business", location=Path("/tmp/business"), ide="cursor")
    config.add_journal(profile1)
    config.add_journal(profile2)
    save_multi_journal_config(config)

    # Without env var
    active_name = get_active_journal_name()
    assert active_name == "personal"

    # With env var override
    monkeypatch.setenv("AI_JOURNAL", "business")
    active_name = get_active_journal_name()
    assert active_name == "business"


def test_multi_journal_config_has_journal():
    """Test checking if journal exists."""
    config = MultiJournalConfig()
    profile = JournalProfile(name="test", location=Path("/tmp/test"), ide="cursor")
    config.add_journal(profile)

    assert config.has_journal("test")
    assert not config.has_journal("nonexistent")
