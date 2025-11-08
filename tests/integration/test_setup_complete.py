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
from pathlib import Path
from ai_journal_kit.cli.app import app
from tests.integration.helpers import (
    assert_journal_structure_valid,
    assert_ide_config_installed,
    assert_config_valid,
)


@pytest.mark.integration
def test_setup_creates_all_folders(temp_journal_dir, isolated_config):
    """Test setup creates all required journal folders."""
    runner = CliRunner()
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor",
        "--no-confirm"
    ])
    
    # Setup should succeed
    assert result.exit_code == 0, f"Setup failed: {result.output}"
    
    # Verify all folders created
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_setup_creates_all_templates(temp_journal_dir, isolated_config):
    """Test setup creates template files."""
    runner = CliRunner()
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor",
        "--no-confirm"
    ])
    
    assert result.exit_code == 0
    
    # Check WELCOME.md template
    welcome_file = temp_journal_dir / "WELCOME.md"
    assert welcome_file.exists(), "WELCOME.md template not created"
    assert welcome_file.is_file()


@pytest.mark.integration
def test_setup_creates_config_file(temp_journal_dir, isolated_config):
    """Test setup creates valid config file."""
    runner = CliRunner()
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "windsurf",
        "--no-confirm"
    ])
    
    assert result.exit_code == 0
    
    # Verify config file created
    config_file = isolated_config / "config.json"
    assert_config_valid(config_file, expected_journal=temp_journal_dir, expected_ide="windsurf")


@pytest.mark.integration
def test_setup_installs_cursor_config(temp_journal_dir, isolated_config):
    """Test setup installs Cursor IDE configuration."""
    runner = CliRunner()
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor",
        "--no-confirm"
    ])
    
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
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "windsurf",
        "--no-confirm"
    ])
    
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
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "claude-code",
        "--no-confirm"
    ])
    
    assert result.exit_code == 0
    
    # Verify Claude Code config installed
    assert_ide_config_installed(temp_journal_dir, "claude-code")
    
    # Check SYSTEM-PROTECTION.md file exists
    protection_file = temp_journal_dir / "SYSTEM-PROTECTION.md"
    assert protection_file.exists()


@pytest.mark.integration
def test_setup_installs_copilot_config(temp_journal_dir, isolated_config):
    """Test setup installs GitHub Copilot configuration."""
    runner = CliRunner()
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "copilot",
        "--no-confirm"
    ])
    
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
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "all",
        "--no-confirm"
    ])
    
    assert result.exit_code == 0
    
    # Verify all IDE configs installed
    assert_ide_config_installed(temp_journal_dir, "all")


@pytest.mark.integration
def test_setup_with_custom_path(tmp_path, isolated_config):
    """Test setup works with custom journal path."""
    custom_path = tmp_path / "custom" / "journal" / "location"
    
    runner = CliRunner()
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(custom_path),
        "--ide", "cursor",
        "--no-confirm"
    ])
    
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
    result1 = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor",
        "--no-confirm"
    ])
    assert result1.exit_code == 0
    
    # Second setup should fail with appropriate message
    result2 = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor",
        "--no-confirm"
    ])
    
    # Should exit with error
    assert result2.exit_code != 0
    # Should mention already configured
    assert "already configured" in result2.output.lower() or "already set up" in result2.output.lower()


@pytest.mark.integration
def test_setup_handles_deleted_journal(temp_journal_dir, isolated_config):
    """Test setup handles case where journal was manually deleted."""
    runner = CliRunner()
    
    # First setup
    result1 = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor",
        "--no-confirm"
    ])
    assert result1.exit_code == 0
    
    # Manually delete journal directory
    import shutil
    shutil.rmtree(temp_journal_dir)
    
    # Setup should detect missing journal and allow recreation
    result2 = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor",
        "--no-confirm"
    ])
    
    # Should succeed (allows recreation of deleted journal)
    assert result2.exit_code == 0, f"Setup should handle deleted journal: {result2.output}"
    
    # Journal should be recreated
    assert temp_journal_dir.exists()
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_setup_creates_parent_directory(tmp_path, isolated_config):
    """Test setup creates parent directories if they don't exist."""
    nested_path = tmp_path / "deeply" / "nested" / "journal"
    
    runner = CliRunner()
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(nested_path),
        "--ide", "cursor",
        "--no-confirm"
    ])
    
    assert result.exit_code == 0
    assert nested_path.exists()
    assert_journal_structure_valid(nested_path)


@pytest.mark.integration  
def test_setup_dry_run_mode(temp_journal_dir, isolated_config):
    """Test setup dry-run mode shows actions without making changes."""
    runner = CliRunner()
    
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor",
        "--dry-run"
    ])
    
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
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor"
    ], input="n\n")
    
    # Should handle cancellation gracefully
    assert result.exit_code != 0 or "cancelled" in result.output.lower()

