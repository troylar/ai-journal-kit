"""
End-to-end integration tests for config persistence.

These tests verify that config files are created, saved, and loaded
correctly through the actual CLI commands.
"""

import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from ai_journal_kit.core.config import load_multi_journal_config


@pytest.mark.integration
def test_setup_creates_persistent_config(temp_journal_dir, isolated_config):
    """Test that setup command creates a config that persists."""
    runner = CliRunner()

    # Run setup
    result = runner.invoke(
        app,
        [
            "setup",
            "--location", str(temp_journal_dir),
            "--ide", "cursor",
            "--no-confirm"
        ]
    )

    assert result.exit_code == 0, f"Setup failed: {result.output}"

    # Verify config file was created
    config = load_multi_journal_config()
    assert config is not None, "Config should exist after setup"
    assert config.active_journal == "default"
    assert "default" in config.journals

    # Verify config persists across multiple loads
    config2 = load_multi_journal_config()
    assert config2 is not None
    assert config2.active_journal == config.active_journal
    assert len(config2.journals) == len(config.journals)


@pytest.mark.integration
def test_config_survives_multiple_commands(temp_journal_dir, isolated_config):
    """Test that config persists across multiple CLI commands."""
    runner = CliRunner()

    # Setup journal
    result1 = runner.invoke(
        app,
        [
            "setup",
            "--location", str(temp_journal_dir),
            "--ide", "cursor",
            "--no-confirm"
        ]
    )
    assert result1.exit_code == 0

    # Run status command
    result2 = runner.invoke(app, ["status"])
    assert result2.exit_code == 0
    assert "cursor" in result2.output.lower()

    # Verify config still exists and is correct
    config = load_multi_journal_config()
    assert config is not None
    assert config.active_journal == "default"
    assert config.journals["default"].ide == "cursor"

    # Run list command
    result3 = runner.invoke(app, ["list"])
    assert result3.exit_code == 0

    # Verify config still exists after list
    config2 = load_multi_journal_config()
    assert config2 is not None
    assert config2.active_journal == "default"


@pytest.mark.integration
def test_config_location_is_platform_specific(temp_journal_dir, isolated_config):
    """Test that config is created in correct platform-specific location."""
    from ai_journal_kit.core.config import get_config_path

    runner = CliRunner()

    # Run setup
    result = runner.invoke(
        app,
        [
            "setup",
            "--location", str(temp_journal_dir),
            "--ide", "cursor",
            "--no-confirm"
        ]
    )
    assert result.exit_code == 0

    # Get expected config path
    config_path = get_config_path()

    # Verify file exists at expected location
    assert config_path.exists(), f"Config file should exist at {config_path}"

    # Just verify the path ends with config.json (platform dirs are mocked in tests)
    assert config_path.name == "config.json"


@pytest.mark.integration
def test_multiple_setup_with_different_names(tmp_path, isolated_config):
    """Test creating multiple journals maintains config correctly."""
    runner = CliRunner()

    journal1 = tmp_path / "journal1"
    journal2 = tmp_path / "journal2"

    # Create first journal (default name)
    result1 = runner.invoke(
        app,
        [
            "setup",
            "--location", str(journal1),
            "--ide", "cursor",
            "--no-confirm"
        ]
    )
    assert result1.exit_code == 0

    # Verify first journal exists in config
    config = load_multi_journal_config()
    assert config is not None
    assert "default" in config.journals

    # Create second journal with explicit name
    result2 = runner.invoke(
        app,
        [
            "setup",
            "--location", str(journal2),
            "--name", "work",
            "--ide", "windsurf",
            "--no-confirm"
        ]
    )
    assert result2.exit_code == 0

    # Verify both journals exist in config
    config2 = load_multi_journal_config()
    assert config2 is not None
    assert "default" in config2.journals
    assert "work" in config2.journals
    assert len(config2.journals) == 2


@pytest.mark.integration
def test_use_journal_persists_active_journal(tmp_path, isolated_config):
    """Test that use command persists active journal selection."""
    runner = CliRunner()

    journal1 = tmp_path / "journal1"
    journal2 = tmp_path / "journal2"

    # Create two journals
    runner.invoke(app, ["setup", "--location", str(journal1), "--ide", "cursor", "--no-confirm"])
    runner.invoke(app, ["setup", "--location", str(journal2), "--name", "work", "--ide", "windsurf", "--no-confirm"])

    # Switch to work journal
    result = runner.invoke(app, ["use", "work"])
    assert result.exit_code == 0

    # Verify active journal was persisted
    config = load_multi_journal_config()
    assert config is not None
    assert config.active_journal == "work"

    # Verify it persists across loads
    config2 = load_multi_journal_config()
    assert config2 is not None
    assert config2.active_journal == "work"
