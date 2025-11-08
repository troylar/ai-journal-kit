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

from ai_journal_kit.cli.app import app
from tests.integration.fixtures.config_factory import create_corrupted_config
from tests.integration.fixtures.journal_factory import create_journal_fixture
from tests.integration.helpers import assert_journal_structure_valid


@pytest.mark.integration
def test_doctor_detects_missing_folders(temp_journal_dir, isolated_config):
    """Test doctor detects missing required folders."""
    # Create journal
    create_journal_fixture(
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
    create_journal_fixture(
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
    """Test doctor can repair journal structure with --fix flag."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Delete folders
    import shutil
    shutil.rmtree(temp_journal_dir / "areas")
    shutil.rmtree(temp_journal_dir / "resources")

    # Run doctor with --fix flag
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--fix"])

    # Should succeed
    assert result.exit_code == 0, f"Doctor --fix should succeed: {result.output}"

    # Folders should be recreated
    assert (temp_journal_dir / "areas").exists()
    assert (temp_journal_dir / "resources").exists()
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_doctor_fixes_missing_ide_configs(temp_journal_dir, isolated_config):
    """Test doctor can fix missing IDE configurations."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Delete IDE config
    import shutil
    shutil.rmtree(temp_journal_dir / ".cursor")

    # Run doctor to detect
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 1

    # Run doctor --fix to repair
    result_fix = runner.invoke(app, ["doctor", "--fix"])
    assert result_fix.exit_code == 0
    assert (temp_journal_dir / ".cursor" / "rules").exists()


@pytest.mark.integration
def test_doctor_verbose_mode(temp_journal_dir, isolated_config):
    """Test doctor --verbose shows detailed diagnostics."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Run doctor with verbose
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--verbose"])

    # Should show all checks
    output_lower = result.output.lower()
    assert "config" in output_lower
    assert "journal" in output_lower or "structure" in output_lower


@pytest.mark.integration
def test_doctor_healthy_journal(temp_journal_dir, isolated_config):
    """Test doctor reports healthy journal correctly."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Run doctor
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should succeed with no issues
    assert result.exit_code == 0
    output_lower = result.output.lower()
    assert "healthy" in output_lower or "no issues" in output_lower


@pytest.mark.integration
def test_doctor_handles_nonexistent_journal(temp_journal_dir, isolated_config):
    """Test doctor handles case where journal location doesn't exist."""
    # Create config but not journal
    from ai_journal_kit.core.config import Config, save_config
    config = Config(
        journal_location=temp_journal_dir,
        ide="cursor",
        use_symlink=False
    )
    save_config(config)

    # Run doctor
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should detect journal missing
    assert result.exit_code == 1
    output_lower = result.output.lower()
    assert "issue" in output_lower


@pytest.mark.integration
def test_doctor_suggests_fix_command(temp_journal_dir, isolated_config):
    """Test doctor suggests using --fix when issues are found."""
    # Create journal with missing folder
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    import shutil
    shutil.rmtree(temp_journal_dir / "daily")

    # Run doctor without --fix
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should suggest --fix
    assert result.exit_code == 1
    output_lower = result.output.lower()
    assert "--fix" in output_lower or "fix" in output_lower


@pytest.mark.integration  
def test_doctor_fix_reports_success(temp_journal_dir, isolated_config):
    """Test doctor --fix reports number of fixes made."""
    # Create journal with multiple issues
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    import shutil
    shutil.rmtree(temp_journal_dir / "daily")
    shutil.rmtree(temp_journal_dir / "projects")
    shutil.rmtree(temp_journal_dir / ".cursor")

    # Run doctor --fix
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--fix"])

    # Should report fixes
    output_lower = result.output.lower()
    assert "fixed" in output_lower or "created" in output_lower


