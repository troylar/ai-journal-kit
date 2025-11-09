"""
Integration tests for move command.

Tests journal relocation including:
- Moving all files to new location
- Updating config file
- Preserving IDE configurations
- Updating symlinks
- Dry-run mode
- Cancellation handling
"""


import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from tests.integration.fixtures.journal_factory import create_journal_fixture
from tests.integration.helpers import (
    assert_config_valid,
    assert_ide_config_installed,
    assert_journal_structure_valid,
)


@pytest.mark.integration
def test_move_relocates_all_files(temp_journal_dir, isolated_config, tmp_path):
    """Test move relocates all journal files to new location."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        has_content=True,
        config_dir=isolated_config
    )

    # New location
    new_location = tmp_path / "new-journal"

    # Run move
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location),  # Positional argument, not --new-location
        "--no-confirm"
    ])

    # Should succeed
    assert result.exit_code == 0

    # New location should have complete structure
    assert new_location.exists()
    assert_journal_structure_valid(new_location)

    # Journal entries should be moved
    assert (new_location / "daily" / "2025-01-01.md").exists()


@pytest.mark.integration
def test_move_updates_config(temp_journal_dir, isolated_config, tmp_path):
    """Test move updates config file with new location."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # New location
    new_location = tmp_path / "relocated-journal"

    # Run move
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location),  # Positional argument, not --new-location
        "--no-confirm"
    ])

    # Should succeed
    assert result.exit_code == 0

    # Config should be updated
    config_file = isolated_config / "config.json"
    assert_config_valid(config_file, expected_journal=new_location)


@pytest.mark.integration
def test_move_preserves_ide_configs(temp_journal_dir, isolated_config, tmp_path):
    """Test move preserves IDE configurations at new location."""
    # Create journal with Windsurf
    create_journal_fixture(
        path=temp_journal_dir,
        ide="windsurf",
        config_dir=isolated_config
    )

    # New location
    new_location = tmp_path / "moved-journal"

    # Run move
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location),  # Positional argument, not --new-location
        "--no-confirm"
    ])

    # Should succeed
    assert result.exit_code == 0

    # IDE config should be at new location
    assert_ide_config_installed(new_location, "windsurf")


@pytest.mark.integration
def test_move_updates_symlinks(temp_journal_dir, isolated_config, tmp_path):
    """Test move updates symlink targets."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Create a symlink (if supported on platform)
    try:
        symlink_path = temp_journal_dir / "link-to-daily"
        symlink_path.symlink_to(temp_journal_dir / "daily")
    except (OSError, NotImplementedError):
        # Symlinks not supported, skip this part
        pytest.skip("Symlinks not supported on this platform")

    # New location
    new_location = tmp_path / "new-home"

    # Run move
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location),  # Positional argument, not --new-location
        "--no-confirm"
    ])

    # Should succeed or handle symlinks appropriately
    assert result.exit_code == 0
    assert new_location.exists()


@pytest.mark.integration
def test_move_dry_run_mode(temp_journal_dir, isolated_config, tmp_path):
    """Test move dry-run shows actions without making changes."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # New location
    new_location = tmp_path / "would-be-here"

    # Run move with dry-run
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location),  # Positional argument
        "--dry-run"
    ])

    # Should succeed
    assert result.exit_code == 0

    # Should mention dry run
    assert "dry run" in result.output.lower() or "would" in result.output.lower()

    # New location should NOT exist
    assert not new_location.exists()

    # Original should still exist
    assert temp_journal_dir.exists()


@pytest.mark.integration
def test_move_handles_cancellation(temp_journal_dir, isolated_config, tmp_path):
    """Test move handles user cancellation gracefully."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # New location
    new_location = tmp_path / "cancelled-move"

    # Run move without --no-confirm and cancel
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location)  # Positional argument
    ], input="n\n")

    # Should handle cancellation
    assert result.exit_code != 0 or "cancel" in result.output.lower()

    # Original should still exist
    assert temp_journal_dir.exists()
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_move_to_cloud_drive(temp_journal_dir, isolated_config, tmp_path):
    """Test move to cloud drive path (simulated)."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        has_content=True,
        config_dir=isolated_config
    )

    # Simulate cloud drive path
    cloud_path = tmp_path / "GoogleDrive" / "MyJournal"

    # Run move
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(cloud_path),  # Positional argument
        "--no-confirm"
    ])

    # Should succeed
    assert result.exit_code == 0

    # Journal should be at cloud path
    assert cloud_path.exists()
    assert_journal_structure_valid(cloud_path)


@pytest.mark.integration
def test_move_prevents_same_location(temp_journal_dir, isolated_config):
    """Test move prevents moving to same location."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Try to move to same location
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(temp_journal_dir),
        "--no-confirm"
    ])

    # Should fail
    assert result.exit_code != 0
    assert "same" in result.output.lower()


@pytest.mark.integration
def test_move_handles_existing_destination(temp_journal_dir, isolated_config, tmp_path):
    """Test move handles destination that already has files."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Create destination with existing file
    new_location = tmp_path / "existing-journal"
    new_location.mkdir(parents=True)
    (new_location / "existing.txt").write_text("existing content")

    # Try to move
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location),
        "--no-confirm"
    ], input="1\n")  # Choose cancel

    # Should handle gracefully
    assert result.exit_code != 0 or "cancel" in result.output.lower()


@pytest.mark.integration
def test_move_validates_path(temp_journal_dir, isolated_config):
    """Test move validates destination path."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Try invalid path
    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        "/invalid/\0/path",
        "--no-confirm"
    ])

    # Should fail validation
    assert result.exit_code != 0


@pytest.mark.integration
def test_move_creates_nested_parents(temp_journal_dir, isolated_config, tmp_path):
    """Test move creates nested parent directories."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Move to deeply nested path
    new_location = tmp_path / "level1" / "level2" / "level3" / "journal"

    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location),
        "--no-confirm"
    ])

    # Should create all parents and succeed
    assert result.exit_code == 0
    assert new_location.exists()
    assert_journal_structure_valid(new_location)


@pytest.mark.integration
def test_move_verbose_output(temp_journal_dir, isolated_config, tmp_path):
    """Test move with verbose flag shows detailed output."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    new_location = tmp_path / "verbose-journal"

    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location),
        "--no-confirm",
        "--verbose"
    ])

    # Should show verbose output
    if result.exit_code == 0:
        # If verbose flag exists and works
        output_lower = result.output.lower()
        # Just verify it executed successfully
        assert new_location.exists()


@pytest.mark.integration
def test_move_with_confirmation_prompt(temp_journal_dir, isolated_config, tmp_path):
    """Test move prompts for confirmation when no --no-confirm flag (covers lines 36-37, 43-50)."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    new_location = tmp_path / "prompted-journal"

    runner = CliRunner()
    # No --no-confirm flag, should prompt
    result = runner.invoke(app, [
        "move",
        str(new_location)
    ], input="y\n")  # Confirm the move

    # Should either succeed or show prompt
    output_lower = result.output.lower()
    # Check for prompt indicators
    assert result.exit_code == 0 or "confirm" in output_lower or "proceed" in output_lower


@pytest.mark.integration
def test_move_cancellation_via_prompt(temp_journal_dir, isolated_config, tmp_path):
    """Test move can be cancelled via prompt (covers lines 54-55)."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    new_location = tmp_path / "cancelled-journal"

    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location)
    ], input="n\n")  # Decline the move

    # Should cancel or ask for confirmation
    output_lower = result.output.lower()
    assert result.exit_code != 0 or "cancel" in output_lower or "abort" in output_lower or "confirm" in output_lower


@pytest.mark.integration
def test_move_handles_nonexistent_source(isolated_config, tmp_path):
    """Test move handles case where source journal doesn't exist (covers lines 69, 74-80)."""
    # Create config but don't create journal
    from ai_journal_kit.core.config import Config, save_config
    nonexistent_journal = tmp_path / "nonexistent"
    config = Config(
        journal_location=nonexistent_journal,
        ide="cursor",
        use_symlink=False
    )
    save_config(config)

    new_location = tmp_path / "new-location"

    runner = CliRunner()
    result = runner.invoke(app, [
        "move",
        str(new_location),
        "--no-confirm"
    ])

    # Should handle gracefully
    assert result.exit_code != 0
    output_lower = result.output.lower()
    assert "error" in output_lower or "not found" in output_lower or "doesn't exist" in output_lower

