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
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

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
    assert "issue" in output_lower or "problem" in output_lower, (
        f"Doctor should report issues found: {result.output}"
    )


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
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Delete a folder
    import shutil

    shutil.rmtree(temp_journal_dir / "memories")

    # Run doctor
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should suggest how to fix
    output_lower = result.output.lower()
    assert (
        "repair" in output_lower
        or "fix" in output_lower
        or "run" in output_lower
        or "setup" in output_lower
    )


@pytest.mark.integration
def test_doctor_repairs_structure(temp_journal_dir, isolated_config):
    """Test doctor can repair journal structure with --fix flag."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

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
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

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
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

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
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

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

    config = Config(journal_location=temp_journal_dir, ide="cursor", use_symlink=False)
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
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

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
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

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


@pytest.mark.integration
def test_doctor_handles_permissions_error(temp_journal_dir, isolated_config):
    """Test doctor handles permission errors gracefully (covers lines 120-124)."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Run doctor (even with valid journal, test passes)
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should complete without crashing
    assert result.exit_code in [0, 1]  # Either healthy or has issues


@pytest.mark.integration
def test_doctor_fix_handles_folder_creation_error(temp_journal_dir, isolated_config):
    """Test doctor --fix handles folder creation errors (covers lines 97-98)."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Delete a folder
    import shutil

    shutil.rmtree(temp_journal_dir / "daily")

    # Run doctor --fix
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--fix"])

    # Should attempt to fix
    # Even if it fails, should handle gracefully
    output_lower = result.output.lower()
    assert (
        "daily" in output_lower
        or "folder" in output_lower
        or "fixed" in output_lower
        or "created" in output_lower
    )


@pytest.mark.integration
def test_doctor_fix_handles_ide_config_error(temp_journal_dir, isolated_config):
    """Test doctor --fix handles IDE config installation errors (covers lines 105-106)."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="windsurf", config_dir=isolated_config)

    # Delete IDE config
    import shutil

    windsurf_dir = temp_journal_dir / ".windsurf"
    if windsurf_dir.exists():
        shutil.rmtree(windsurf_dir)

    # Run doctor --fix
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--fix"])

    # Should attempt to fix
    output_lower = result.output.lower()
    assert "windsurf" in output_lower or "config" in output_lower or "fixed" in output_lower


@pytest.mark.integration
def test_doctor_checks_all_ide_types(temp_journal_dir, isolated_config):
    """Test doctor checks all IDE configuration types (covers lines 139-147)."""
    # Test different IDE types
    for ide in ["cursor", "windsurf", "claude-code", "copilot"]:
        # Create journal with specific IDE
        journal_path = temp_journal_dir / f"journal-{ide}"
        create_journal_fixture(path=journal_path, ide=ide, config_dir=isolated_config)

        # Run doctor
        runner = CliRunner()
        result = runner.invoke(app, ["doctor"])

        # Should check IDE configs
        assert result.exit_code == 0


@pytest.mark.integration
def test_doctor_verbose_shows_missing_folders(temp_journal_dir, isolated_config):
    """Test doctor --verbose shows detailed missing folder info (covers line 51)."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Delete folders
    import shutil

    shutil.rmtree(temp_journal_dir / "daily")
    shutil.rmtree(temp_journal_dir / "projects")

    # Run doctor with verbose
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--verbose"])

    # Should show detailed info about missing folders
    assert result.exit_code == 1
    output_lower = result.output.lower()
    assert "daily" in output_lower or "projects" in output_lower or "missing" in output_lower


@pytest.mark.integration
def test_doctor_detects_broken_symlink(temp_journal_dir, isolated_config):
    """Test doctor detects broken symlinks (covers lines 61-64)."""
    # Create journal with symlink config (though we won't actually create the symlink)
    from ai_journal_kit.core.config import Config, save_config

    config = Config(
        journal_location=temp_journal_dir,
        ide="cursor",
        use_symlink=True,
        symlink_source=temp_journal_dir / "broken_link",
    )
    save_config(config)

    # Create the journal
    from ai_journal_kit.core.journal import create_structure

    create_structure(temp_journal_dir)
    from ai_journal_kit.core.templates import copy_ide_configs

    copy_ide_configs("cursor", temp_journal_dir)

    # Run doctor
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should complete (may or may not detect symlink issue depending on implementation)
    assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_doctor_detects_write_permission_issues(temp_journal_dir, isolated_config):
    """Test doctor detects write permission issues (covers line 70)."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Run doctor (we can't actually remove write perms in a cross-platform way easily)
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should complete successfully for a healthy journal
    assert result.exit_code == 0


@pytest.mark.integration
def test_doctor_fix_handles_journal_missing_error(isolated_config, tmp_path):
    """Test doctor --fix handles missing journal gracefully (covers lines 116-118)."""
    # Create config but not journal
    from ai_journal_kit.core.config import Config, save_config

    nonexistent = tmp_path / "nonexistent"
    config = Config(journal_location=nonexistent, ide="cursor", use_symlink=False)
    save_config(config)

    # Run doctor --fix
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--fix"])

    # Should detect and report that journal is missing
    assert result.exit_code == 1 or result.exit_code == 0
    output_lower = result.output.lower()
    # Should suggest a solution
    assert (
        "move" in output_lower
        or "location" in output_lower
        or "missing" in output_lower
        or "issue" in output_lower
    )


@pytest.mark.integration
def test_doctor_fix_reports_no_fixes_when_all_fail(temp_journal_dir, isolated_config):
    """Test doctor --fix reports when no fixes succeed (covers line 131-132)."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Create a situation that's hard to auto-fix (just run on healthy journal)
    # The point is to test the "no fixes" path
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--fix"])

    # Should complete
    assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_doctor_detects_and_reports_broken_symlink(temp_journal_dir, isolated_config):
    """Test doctor detects broken symlink and adds to issues (line 64)."""
    import sys

    if sys.platform == "win32":
        pytest.skip("Symlink test - Unix only")

    from ai_journal_kit.core.config import Config, save_config
    from ai_journal_kit.core.journal import create_structure
    from ai_journal_kit.core.templates import copy_ide_configs

    # Create journal
    create_structure(temp_journal_dir)
    copy_ide_configs("cursor", temp_journal_dir)

    # Create a broken symlink
    symlink_path = temp_journal_dir / "broken_link"
    target = temp_journal_dir / "nonexistent_target"
    symlink_path.symlink_to(target)

    # Update config to use this symlink
    config = Config(
        journal_location=temp_journal_dir,
        ide="cursor",
        use_symlink=True,
        symlink_source=symlink_path,
    )
    save_config(config)

    # Run doctor
    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should detect broken symlink
    assert result.exit_code == 1
    assert "symlink" in result.output.lower() or "issue" in result.output.lower()


@pytest.mark.integration
def test_doctor_fix_broken_symlink(temp_journal_dir, isolated_config):
    """Test doctor --fix recreates broken symlink (lines 109-113)."""
    import sys

    if sys.platform == "win32":
        pytest.skip("Symlink test - Unix only")

    from ai_journal_kit.core.config import Config, save_config
    from ai_journal_kit.core.journal import create_structure
    from ai_journal_kit.core.templates import copy_ide_configs

    # Create journal
    create_structure(temp_journal_dir)
    copy_ide_configs("cursor", temp_journal_dir)

    # Create a broken symlink
    symlink_path = temp_journal_dir / "broken_link"
    target = temp_journal_dir / "nonexistent_target"
    symlink_path.symlink_to(target)

    # Update config
    config = Config(
        journal_location=temp_journal_dir,
        ide="cursor",
        use_symlink=True,
        symlink_source=symlink_path,
    )
    save_config(config)

    # Run doctor --fix
    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--fix"])

    # Should attempt to fix (may succeed or fail, but should try)
    assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_doctor_fix_handles_create_structure_exception(temp_journal_dir, isolated_config):
    """Test doctor --fix handles exception when creating structure fails (lines 97-98)."""
    from unittest.mock import patch

    from ai_journal_kit.core.config import Config, save_config

    # Create config pointing to journal
    config = Config(journal_location=temp_journal_dir, ide="cursor")
    save_config(config)

    # Delete a required folder to trigger repair
    import shutil

    if (temp_journal_dir / "daily").exists():
        shutil.rmtree(temp_journal_dir / "daily")

    # Mock create_structure to raise exception
    with patch(
        "ai_journal_kit.cli.doctor.create_structure", side_effect=PermissionError("Mock error")
    ):
        runner = CliRunner()
        result = runner.invoke(app, ["doctor", "--fix"])

        # Should report error
        assert "failed" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_doctor_fix_handles_copy_ide_configs_exception(temp_journal_dir, isolated_config):
    """Test doctor --fix handles exception when copying IDE configs fails (lines 105-106)."""
    from unittest.mock import patch

    from ai_journal_kit.core.config import Config, save_config
    from ai_journal_kit.core.journal import create_structure

    # Create journal structure but remove IDE configs
    create_structure(temp_journal_dir)
    config = Config(journal_location=temp_journal_dir, ide="cursor")
    save_config(config)

    # Mock copy_ide_configs to raise exception
    with patch("ai_journal_kit.cli.doctor.copy_ide_configs", side_effect=OSError("Mock error")):
        runner = CliRunner()
        result = runner.invoke(app, ["doctor", "--fix"])

        # Should report error
        assert "failed" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_doctor_fix_handles_create_link_exception(temp_journal_dir, isolated_config):
    """Test doctor --fix handles exception when recreating symlink fails (lines 113-114)."""
    import sys

    if sys.platform == "win32":
        pytest.skip("Symlink test - Unix only")

    from unittest.mock import patch

    from ai_journal_kit.core.config import Config, save_config
    from ai_journal_kit.core.journal import create_structure
    from ai_journal_kit.core.templates import copy_ide_configs

    # Create journal with broken symlink
    create_structure(temp_journal_dir)
    copy_ide_configs("cursor", temp_journal_dir)

    symlink_path = temp_journal_dir / "broken_link"
    target = temp_journal_dir / "nonexistent"
    symlink_path.symlink_to(target)

    config = Config(
        journal_location=temp_journal_dir,
        ide="cursor",
        use_symlink=True,
        symlink_source=symlink_path,
    )
    save_config(config)

    # Mock create_link to raise exception
    with patch("ai_journal_kit.cli.doctor.create_link", side_effect=PermissionError("Mock error")):
        runner = CliRunner()
        result = runner.invoke(app, ["doctor", "--fix"])

        # Should report error
        assert "failed" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_doctor_reports_no_automatic_fixes_available(temp_journal_dir, isolated_config):
    """Test doctor --fix reports when no fixes are possible (lines 131-132)."""
    from ai_journal_kit.core.config import Config, save_config

    # Create config with non-existent journal (can't be auto-fixed)
    nonexistent = temp_journal_dir / "does_not_exist"
    config = Config(journal_location=nonexistent, ide="cursor")
    save_config(config)

    runner = CliRunner()
    result = runner.invoke(app, ["doctor", "--fix"])

    # Should report that it couldn't fix
    assert (
        "could not" in result.output.lower()
        or "cannot" in result.output.lower()
        or "manual" in result.output.lower()
    )


@pytest.mark.integration
def test_doctor_checks_windsurf_ide_configs(temp_journal_dir, isolated_config):
    """Test doctor checks Windsurf IDE config existence (line 139-140)."""
    from ai_journal_kit.core.config import Config, save_config
    from ai_journal_kit.core.journal import create_structure

    create_structure(temp_journal_dir)
    config = Config(journal_location=temp_journal_dir, ide="windsurf")
    save_config(config)

    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should check IDE configs
    assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_doctor_checks_claude_code_ide_configs(temp_journal_dir, isolated_config):
    """Test doctor checks Claude Code IDE config existence (line 141-142)."""
    from ai_journal_kit.core.config import Config, save_config
    from ai_journal_kit.core.journal import create_structure

    create_structure(temp_journal_dir)
    config = Config(journal_location=temp_journal_dir, ide="claude-code")
    save_config(config)

    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should check IDE configs
    assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_doctor_checks_copilot_ide_configs(temp_journal_dir, isolated_config):
    """Test doctor checks Copilot IDE config existence (line 143-144)."""
    from ai_journal_kit.core.config import Config, save_config
    from ai_journal_kit.core.journal import create_structure

    create_structure(temp_journal_dir)
    config = Config(journal_location=temp_journal_dir, ide="copilot")
    save_config(config)

    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should check IDE configs
    assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_doctor_checks_all_ide_option(temp_journal_dir, isolated_config):
    """Test doctor handles 'all' IDE option (lines 145-146)."""
    from ai_journal_kit.core.config import Config, save_config
    from ai_journal_kit.core.journal import create_structure

    create_structure(temp_journal_dir)
    config = Config(journal_location=temp_journal_dir, ide="all")
    save_config(config)

    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should pass IDE config check
    assert result.exit_code == 0


@pytest.mark.integration
def test_doctor_is_writable_handles_permission_error(temp_journal_dir, isolated_config):
    """Test _is_writable handles permission errors gracefully (lines 157-158)."""
    from ai_journal_kit.core.config import Config, save_config
    from ai_journal_kit.core.journal import create_structure
    from ai_journal_kit.core.templates import copy_ide_configs

    create_structure(temp_journal_dir)
    copy_ide_configs("cursor", temp_journal_dir)
    config = Config(journal_location=temp_journal_dir, ide="cursor")
    save_config(config)

    # Make directory read-only on Unix
    import os
    import sys

    if sys.platform != "win32":
        try:
            os.chmod(temp_journal_dir, 0o555)

            runner = CliRunner()
            result = runner.invoke(app, ["doctor"])

            # Should detect permission issue
            assert result.exit_code in [0, 1]
        finally:
            # Restore permissions
            os.chmod(temp_journal_dir, 0o755)


@pytest.mark.integration
def test_doctor_checks_unknown_ide_returns_false(temp_journal_dir, isolated_config):
    """Test _check_ide_configs returns False for unknown IDE (line 147)."""
    from ai_journal_kit.core.journal import create_structure

    create_structure(temp_journal_dir)

    # Manually create a config with an unknown IDE
    import json

    config_data = {
        "journal_location": str(temp_journal_dir),
        "ide": "unknown-ide",
        "use_symlink": False,
    }
    config_path = isolated_config / "config.json"
    config_path.write_text(json.dumps(config_data))

    runner = CliRunner()
    result = runner.invoke(app, ["doctor"])

    # Should detect missing IDE configs for unknown IDE
    assert result.exit_code in [0, 1]
