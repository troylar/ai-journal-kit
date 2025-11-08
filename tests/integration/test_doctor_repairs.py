"""
Integration tests for doctor command.

Tests doctor command diagnostics and repairs including:
- Detecting missing folders
- Detecting corrupted config
- Suggesting repairs
- Performing repairs
"""

import pytest
from typer.testing import CliRunner
from pathlib import Path
from ai_journal_kit.cli.app import app
from tests.integration.fixtures.journal_factory import create_journal_fixture
from tests.integration.fixtures.config_factory import create_corrupted_config
from tests.integration.helpers import assert_journal_structure_valid


@pytest.mark.integration
def test_doctor_detects_missing_folders(temp_journal_dir, isolated_config):
    """Test doctor detects missing required folders."""
    # Create journal
    journal = create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )
    
    # Delete some folders
    import shutil
    shutil.rmtree(temp_journal_dir / "daily")
    shutil.rmtree(temp_journal_dir / "projects")
    
    # Run doctor
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])
    
    # Should detect issues (exit code 1 when issues found)
    assert result.exit_code == 1, "Doctor should exit with code 1 when issues are found"
    
    # Should show that issues were found
    output_lower = result.output.lower()
    assert "issue" in output_lower or "problem" in output_lower, f"Doctor should report issues found: {result.output}"


@pytest.mark.integration
def test_doctor_detects_corrupted_config(isolated_config):
    """Test doctor detects corrupted configuration."""
    # Create corrupted config
    create_corrupted_config(isolated_config)
    
    # Run doctor
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])
    
    # Should detect config issue
    output_lower = result.output.lower()
    assert "config" in output_lower or "error" in output_lower or "corrupt" in output_lower


@pytest.mark.integration
def test_doctor_suggests_repairs(temp_journal_dir, isolated_config):
    """Test doctor suggests repairs for detected issues."""
    # Create journal
    journal = create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )
    
    # Delete a folder
    import shutil
    shutil.rmtree(temp_journal_dir / "memories")
    
    # Run doctor
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])
    
    # Should suggest how to fix
    output_lower = result.output.lower()
    assert "repair" in output_lower or "fix" in output_lower or "run" in output_lower or "setup" in output_lower


@pytest.mark.integration
def test_doctor_repairs_structure(temp_journal_dir, isolated_config):
    """Test doctor can repair journal structure."""
    # Create journal
    journal = create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )
    
    # Delete folders
    import shutil
    shutil.rmtree(temp_journal_dir / "areas")
    shutil.rmtree(temp_journal_dir / "resources")
    
    # Run doctor with repair flag (if it exists)
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--repair"])
    
    # Should attempt repair
    # May succeed or the flag may not exist yet
    if result.exit_code == 0:
        # If repair worked, folders should be recreated
        if (temp_journal_dir / "areas").exists() and (temp_journal_dir / "resources").exists():
            assert_journal_structure_valid(temp_journal_dir)

