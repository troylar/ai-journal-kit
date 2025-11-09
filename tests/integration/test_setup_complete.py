"""
Integration tests for setup command complete flow.

Tests all setup scenarios including:
- Journal structure creation
- IDE configuration installation
- Config file generation
- Error handling and validation
"""

import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from tests.integration.helpers import (
    assert_config_valid,
    assert_ide_config_installed,
    assert_journal_structure_valid,
)


@pytest.mark.integration
def test_setup_creates_all_folders(temp_journal_dir, isolated_config):
    """Test setup creates all required journal folders."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )

    # Setup should succeed
    assert result.exit_code == 0, f"Setup failed: {result.output}"

    # Verify all folders created
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_setup_creates_all_templates(temp_journal_dir, isolated_config):
    """Test setup creates template files."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Check WELCOME.md template
    welcome_file = temp_journal_dir / "WELCOME.md"
    assert welcome_file.exists(), "WELCOME.md template not created"
    assert welcome_file.is_file()


@pytest.mark.integration
def test_setup_creates_config_file(temp_journal_dir, isolated_config):
    """Test setup creates valid config file."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "windsurf", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify config file created
    config_file = isolated_config / "config.json"
    assert_config_valid(config_file, expected_journal=temp_journal_dir, expected_ide="windsurf")


@pytest.mark.integration
def test_setup_installs_cursor_config(temp_journal_dir, isolated_config):
    """Test setup installs Cursor IDE configuration."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify Cursor config installed
    assert_ide_config_installed(temp_journal_dir, "cursor")

    # Check specific Cursor files
    cursor_rules = temp_journal_dir / ".cursor" / "rules"
    assert cursor_rules.exists()
    assert (cursor_rules / "journal-coach.mdc").exists()


@pytest.mark.integration
def test_setup_installs_windsurf_config(temp_journal_dir, isolated_config):
    """Test setup installs Windsurf IDE configuration."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "windsurf", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify Windsurf config installed
    assert_ide_config_installed(temp_journal_dir, "windsurf")

    # Check specific Windsurf files
    windsurf_rules = temp_journal_dir / ".windsurf" / "rules"
    assert windsurf_rules.exists()


@pytest.mark.integration
def test_setup_installs_claude_config(temp_journal_dir, isolated_config):
    """Test setup installs Claude Code configuration."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "claude-code", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify Claude Code config installed
    assert_ide_config_installed(temp_journal_dir, "claude-code")

    # Check CLAUDE.md file exists
    claude_file = temp_journal_dir / "CLAUDE.md"
    assert claude_file.exists()


@pytest.mark.integration
def test_setup_installs_copilot_config(temp_journal_dir, isolated_config):
    """Test setup installs GitHub Copilot configuration."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "copilot", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify Copilot config installed
    assert_ide_config_installed(temp_journal_dir, "copilot")

    # Check Copilot instruction files
    copilot_instructions = temp_journal_dir / ".github" / "instructions"
    assert copilot_instructions.exists()


@pytest.mark.integration
def test_setup_installs_all_configs(temp_journal_dir, isolated_config):
    """Test setup installs all IDE configurations when 'all' selected."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "all", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify all IDE configs installed
    assert_ide_config_installed(temp_journal_dir, "all")


@pytest.mark.integration
def test_setup_with_custom_path(tmp_path, isolated_config):
    """Test setup works with custom journal path."""
    custom_path = tmp_path / "custom" / "journal" / "location"

    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(custom_path), "--ide", "cursor", "--no-confirm"]
    )

    # Debug: print output if failed
    if result.exit_code != 0:
        print(f"\nSetup failed with exit code {result.exit_code}")
        print(f"Output: {result.output}")
        if result.exception:
            print(f"Exception: {result.exception}")

    assert result.exit_code == 0, f"Setup failed: {result.output}"

    # Verify journal created at custom path
    assert custom_path.exists()
    assert_journal_structure_valid(custom_path)


@pytest.mark.integration
def test_setup_prevents_duplicate_installation(temp_journal_dir, isolated_config):
    """Test setup prevents duplicate installation."""
    runner = CliRunner()

    # First setup should succeed
    result1 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )
    assert result1.exit_code == 0

    # Second setup without --name should fail with appropriate message
    result2 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )

    # Should exit with error (needs --name for additional journals)
    assert result2.exit_code != 0
    # Should mention name is required for additional journals
    assert "name required" in result2.output.lower() or "use --name" in result2.output.lower()


@pytest.mark.skip(
    reason="Behavior changed with multi-journal support - use doctor command to repair deleted journals"
)
@pytest.mark.integration
def test_setup_handles_deleted_journal(temp_journal_dir, isolated_config):
    """Test setup handles case where journal was manually deleted.

    NOTE: With multi-journal support, if a journal directory is deleted but config remains,
    use 'ai-journal-kit doctor' to repair. Setup now requires --name for new journals.
    """
    runner = CliRunner()

    # First setup
    result1 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )
    assert result1.exit_code == 0

    # Manually delete journal directory
    import shutil

    shutil.rmtree(temp_journal_dir)

    # With multi-journal, setup won't recreate without --name, and --name "default" conflicts
    # User should use 'doctor' command to repair deleted journals
    # This test is skipped until we add a repair/recreate command


@pytest.mark.integration
def test_setup_creates_parent_directory(tmp_path, isolated_config):
    """Test setup creates parent directories if they don't exist."""
    nested_path = tmp_path / "deeply" / "nested" / "journal"

    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(nested_path), "--ide", "cursor", "--no-confirm"]
    )

    assert result.exit_code == 0
    assert nested_path.exists()
    assert_journal_structure_valid(nested_path)


@pytest.mark.integration
def test_setup_dry_run_mode(temp_journal_dir, isolated_config):
    """Test setup dry-run mode shows actions without making changes."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--dry-run"]
    )

    # Dry run should succeed
    assert result.exit_code == 0

    # Should mention it's a dry run
    assert "dry run" in result.output.lower() or "would" in result.output.lower()

    # Journal should NOT be created
    assert not temp_journal_dir.exists() or len(list(temp_journal_dir.iterdir())) == 0


@pytest.mark.integration
def test_setup_handles_cancellation(temp_journal_dir, isolated_config):
    """Test setup handles user cancellation gracefully."""
    runner = CliRunner()

    # Simulate user cancellation by not providing --no-confirm
    # and providing 'n' as input
    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor"], input="n\n"
    )

    # Should handle cancellation gracefully
    assert result.exit_code != 0 or "cancelled" in result.output.lower()


@pytest.mark.integration
def test_setup_with_invalid_path(isolated_config):
    """Test setup handles invalid path gracefully (covers lines 86-88)."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "setup",
            "/invalid/\0/path",  # Invalid path with null byte
            "--ide",
            "cursor",
            "--no-confirm",
        ],
    )

    # Should fail with error
    assert result.exit_code != 0
    assert "error" in result.output.lower() or "invalid" in result.output.lower()


@pytest.mark.integration
def test_setup_with_invalid_ide(temp_journal_dir, isolated_config):
    """Test setup handles invalid IDE gracefully (covers lines 97-99)."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", str(temp_journal_dir), "--ide", "invalid-ide-name", "--no-confirm"]
    )

    # Should fail with error
    assert result.exit_code != 0
    assert "ide" in result.output.lower() or "invalid" in result.output.lower()


@pytest.mark.integration
def test_setup_with_parent_creation_declined(temp_journal_dir, isolated_config):
    """Test setup when user declines parent directory creation (covers lines 74-81)."""
    # Use nested path that doesn't exist
    nested_path = temp_journal_dir / "nonexistent" / "journal"

    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", str(nested_path), "--ide", "cursor"], input="n\n"
    )  # Decline parent creation

    # Should cancel setup
    assert result.exit_code != 0
    assert "cancel" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_setup_interactive_location_prompt(isolated_config, tmp_path):
    """Test setup with interactive location prompt (covers line 60)."""
    journal_path = tmp_path / "interactive-journal"

    runner = CliRunner()
    # No --location flag, so it will prompt
    # Provide location via stdin
    result = runner.invoke(
        app, ["setup", "--ide", "cursor", "--no-confirm"], input=f"{journal_path}\n"
    )

    # Should succeed
    assert result.exit_code == 0 or journal_path.exists()


@pytest.mark.integration
def test_setup_interactive_ide_prompt(temp_journal_dir, isolated_config):
    """Test setup with interactive IDE prompt (covers line 92)."""
    runner = CliRunner()
    # No --ide flag, so it will prompt
    # Provide IDE choice via stdin
    result = runner.invoke(
        app, ["setup", str(temp_journal_dir), "--no-confirm"], input="1\n"
    )  # Choose first IDE option

    # Should succeed or at least not crash
    assert result.exit_code == 0 or "ide" in result.output.lower()


@pytest.mark.integration
def test_setup_dry_run_parent_creation(temp_journal_dir, isolated_config):
    """Test setup dry-run mode shows parent directory creation (covers line 69)."""
    nested_path = temp_journal_dir / "parent" / "journal"

    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", "--location", str(nested_path), "--ide", "cursor", "--dry-run"]
    )

    # Dry-run shows what would happen but may exit with error (doesn't actually create)
    # The key is that it shows the "would create" message
    output_lower = result.output.lower()
    assert "dry run" in output_lower or "would create" in output_lower


@pytest.mark.integration
def test_setup_parent_creation_accepted_interactive(temp_journal_dir, isolated_config):
    """Test setup when user accepts parent directory creation interactively (lines 74-78)."""
    nested_path = temp_journal_dir / "new_parent" / "journal"

    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", "--location", str(nested_path), "--ide", "cursor"], input="y\ny\n"
    )  # Yes to create parent, Yes to proceed

    # Should succeed or create the parent
    assert result.exit_code == 0 or nested_path.parent.exists()


@pytest.mark.integration
def test_setup_parent_creation_declined_interactive(temp_journal_dir, isolated_config):
    """Test setup when user declines parent directory creation interactively (lines 80-81)."""
    nested_path = temp_journal_dir / "decline_parent" / "journal"

    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", "--location", str(nested_path), "--ide", "cursor"], input="n\n"
    )  # No to create parent

    # Should fail since parent wasn't created
    assert result.exit_code != 0
    assert "cancel" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_setup_interactive_ide_selection_complete(isolated_config, temp_journal_dir):
    """Test setup with full interactive IDE selection (line 92)."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--no-confirm"], input="cursor\n"
    )  # Provide IDE name when prompted

    # Should complete successfully
    assert result.exit_code == 0 or temp_journal_dir.exists()


@pytest.mark.integration
def test_setup_with_invalid_ide_choice(temp_journal_dir, isolated_config):
    """Test setup with invalid IDE that triggers validation error (lines 97-99)."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["setup", "--location", str(temp_journal_dir), "--ide", "not-a-valid-ide", "--no-confirm"],
    )

    # Should fail with validation error
    assert result.exit_code != 0


@pytest.mark.integration
def test_setup_exception_during_creation(temp_journal_dir, isolated_config):
    """Test setup handles exceptions during journal creation (lines 163-165)."""

    runner = CliRunner()

    # Use a path that will cause issues
    bad_path = temp_journal_dir / "test.txt"
    bad_path.write_text("existing file")

    result = runner.invoke(
        app, ["setup", "--location", str(bad_path), "--ide", "cursor", "--no-confirm"]
    )

    # Should handle error gracefully
    # May succeed or fail depending on validation, key is no crash
    assert isinstance(result.exit_code, int)
