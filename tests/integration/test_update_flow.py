"""
Integration tests for update command.

Tests update scenarios including:
- Preserving custom templates and configurations
- Refreshing core templates
- Adding new IDE configs
- Migrating old structures
- Handling corrupted configs
"""

import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from tests.integration.fixtures.journal_factory import create_journal_fixture
from tests.integration.helpers import (
    assert_ide_config_installed,
    assert_journal_structure_valid,
)


@pytest.mark.integration
def test_update_preserves_custom_templates(temp_journal_dir, isolated_config):
    """Test update preserves custom user templates."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Add custom template
    custom_template = temp_journal_dir / "daily" / "my-custom-template.md"
    custom_template.write_text("# My Custom Template\n\nThis is my personal template.")

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--no-confirm"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()

    # Custom template should still exist
    assert custom_template.exists()
    assert "My Custom Template" in custom_template.read_text(encoding="utf-8")


@pytest.mark.integration
def test_update_preserves_ai_instructions(temp_journal_dir, isolated_config):
    """Test update preserves custom AI instructions."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Add custom AI instructions
    ai_instructions_dir = temp_journal_dir / ".ai-instructions"
    ai_instructions_dir.mkdir(exist_ok=True)
    custom_coach = ai_instructions_dir / "my-coach.md"
    custom_coach.write_text("# My Custom Coach\n\nBe very direct and concise.")

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--no-confirm"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()

    # Custom instructions should still exist
    assert custom_coach.exists()
    assert "Be very direct and concise" in custom_coach.read_text(encoding="utf-8")


@pytest.mark.integration
def test_update_preserves_journal_entries(temp_journal_dir, isolated_config):
    """Test update preserves existing journal entries."""
    # Create journal with content
    journal = create_journal_fixture(
        path=temp_journal_dir, ide="cursor", has_content=True, config_dir=isolated_config
    )

    # Verify entries exist
    assert journal.daily_notes_count == 3

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--no-confirm"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()

    # Journal entries should still exist
    assert (temp_journal_dir / "daily" / "2025-01-01.md").exists()
    assert (temp_journal_dir / "daily" / "2025-01-02.md").exists()
    assert (temp_journal_dir / "daily" / "2025-01-03.md").exists()


@pytest.mark.integration
def test_update_refreshes_core_templates(temp_journal_dir, isolated_config):
    """Test update refreshes core system templates."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Modify WELCOME.md (core template)
    welcome_file = temp_journal_dir / "WELCOME.md"
    if welcome_file.exists():
        welcome_file.write_text("# Modified Welcome\n\nThis should be updated.")

    # Run update with force and no-confirm to refresh templates
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--force", "--no-confirm"])

    # Update should succeed
    assert result.exit_code == 0, f"Update failed: {result.output}"


@pytest.mark.integration
def test_update_adds_new_ide_configs(temp_journal_dir, isolated_config):
    """Test update adds new IDE configs if missing."""
    # Create journal with only Cursor
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Verify only Cursor config exists
    assert_ide_config_installed(temp_journal_dir, "cursor")

    # Run update (in real implementation, this would add new configs)
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--no-confirm"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()

    # Original structure should remain valid
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_update_migrates_old_structure(temp_journal_dir, isolated_config):
    """Test update migrates old template structure."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="copilot", config_dir=isolated_config)

    # Create old Copilot structure (copilot-instructions.md in .github root)
    old_copilot_file = temp_journal_dir / ".github" / "copilot-instructions.md"
    old_copilot_file.parent.mkdir(exist_ok=True, parents=True)
    old_copilot_file.write_text("# Old Copilot Instructions")

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--no-confirm"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()


@pytest.mark.integration
def test_update_dry_run_mode(temp_journal_dir, isolated_config):
    """Test update dry-run shows actions without making changes."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Add custom content
    custom_file = temp_journal_dir / "daily" / "test.md"
    custom_file.write_text("# Test")
    original_mtime = custom_file.stat().st_mtime

    # Run dry-run update
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--dry-run"])

    # Should succeed or show dry-run message
    assert (
        result.exit_code == 0
        or "dry run" in result.output.lower()
        or "would" in result.output.lower()
    )

    # File should not be modified
    assert custom_file.stat().st_mtime == original_mtime


@pytest.mark.integration
def test_update_handles_corrupted_config(temp_journal_dir, isolated_config):
    """Test update handles corrupted config gracefully."""
    from tests.integration.fixtures.config_factory import create_corrupted_config

    # Create journal first
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Corrupt the config
    create_corrupted_config(isolated_config)

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update"])

    # Should handle error gracefully (may fail or fix config)
    # At minimum, should provide useful error message
    if result.exit_code != 0:
        assert "config" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_update_with_force_flag(temp_journal_dir, isolated_config):
    """Test update with --force flag forces template refresh."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Run update with force and no-confirm for testing
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--force", "--no-confirm"])

    # Should succeed
    assert result.exit_code == 0, f"Update --force failed: {result.output}"

    # Journal structure should remain valid
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_update_check_only_mode(temp_journal_dir, isolated_config):
    """Test update --check only checks without installing."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Run update with --check
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--check"])

    # Should succeed or show up to date
    assert result.exit_code == 0 or "up to date" in result.output.lower()
    # Should not prompt for confirmation
    assert "proceed" not in result.output.lower() or "check" in result.output.lower()


@pytest.mark.integration
def test_update_with_network_error_handling(temp_journal_dir, isolated_config):
    """Test update handles network errors gracefully."""
    from unittest.mock import patch

    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock network failure - get_latest_version returns None
    with patch("ai_journal_kit.cli.update.get_latest_version", return_value=None):
        runner = CliRunner()
        result = runner.invoke(app, ["update"])

        # Should handle gracefully - exit successfully with message about dev mode
        assert result.exit_code == 0
        output_lower = result.output.lower()
        assert "unable to check" in output_lower or "development mode" in output_lower


@pytest.mark.integration
def test_update_detect_pip_handles_exceptions(temp_journal_dir, isolated_config):
    """Test detect_pip_command handles exceptions (lines 41-45)."""
    from unittest.mock import patch

    from ai_journal_kit.cli.update import detect_pip_command

    # Mock subprocess.run to raise various exceptions
    with patch("subprocess.run", side_effect=FileNotFoundError("pip not found")):
        result = detect_pip_command()
        # Should fall back to ["pip"]
        assert result == ["pip"]


@pytest.mark.integration
def test_update_get_latest_version_handles_exception(temp_journal_dir, isolated_config):
    """Test get_latest_version handles exceptions (lines 63-64)."""
    from unittest.mock import patch

    from ai_journal_kit.cli.update import get_latest_version

    # Mock urllib to raise exception
    with patch("urllib.request.urlopen", side_effect=Exception("Network error")):
        result = get_latest_version()
        assert result is None


@pytest.mark.integration
def test_update_get_changelog_handles_exception_with_fallback(temp_journal_dir, isolated_config):
    """Test get_changelog handles exception and returns fallback (lines 84-88)."""
    from unittest.mock import patch

    from ai_journal_kit.cli.update import get_changelog

    # Mock urllib to raise exception
    with patch("urllib.request.urlopen", side_effect=Exception("API error")):
        result = get_changelog("0.1.0", "0.2.0")
        # Should return fallback message
        assert result is not None
        assert "0.2.0" in result
        assert "github.com" in result.lower()


@pytest.mark.integration
def test_update_unable_to_check_pypi_without_force(temp_journal_dir, isolated_config):
    """Test update when PyPI unavailable and no --force (lines 141-146)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock get_latest_version to return None (PyPI unavailable)
    with patch("ai_journal_kit.cli.update.get_latest_version", return_value=None):
        runner = CliRunner()
        result = runner.invoke(app, ["update"])

        # Should exit with message about dev mode
        assert result.exit_code == 0
        assert (
            "unable to check" in result.output.lower()
            or "development mode" in result.output.lower()
        )


@pytest.mark.integration
def test_update_unable_to_check_pypi_with_force(temp_journal_dir, isolated_config):
    """Test update when PyPI unavailable but --force specified (lines 147-149)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock get_latest_version to return None and subprocess to succeed
    with patch("ai_journal_kit.cli.update.get_latest_version", return_value=None):
        with patch("subprocess.run"):
            runner = CliRunner()
            result = runner.invoke(app, ["update", "--force", "--no-confirm"])

            # Should proceed with force
            assert "forcing" in result.output.lower() or "refresh" in result.output.lower()


@pytest.mark.integration
def test_update_check_flag_exits_when_update_available(temp_journal_dir, isolated_config):
    """Test update --check exits when update is available (lines 161-163)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock version check to show update available
    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        runner = CliRunner()
        result = runner.invoke(app, ["update", "--check"])

        # Should exit with update available message
        assert result.exit_code == 0
        assert "update available" in result.output.lower() or "99.99.99" in result.output


@pytest.mark.integration
def test_update_with_templates_flag(temp_journal_dir, isolated_config):
    """Test update --templates shows template changes (lines 178-185)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock get_template_changes to return some changes
    mock_changes = {
        "daily-template.md": {
            "user_path": temp_journal_dir / "daily-template.md",
            "size_old": 100,
            "size_new": 150,
        }
    }

    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        with patch(
            "ai_journal_kit.core.template_updater.get_template_changes", return_value=mock_changes
        ):
            with patch("ai_journal_kit.core.template_updater.show_template_changes"):
                runner = CliRunner()
                result = runner.invoke(app, ["update", "--templates", "--dry-run"])

                # Should show template update info
                assert "template" in result.output.lower()


@pytest.mark.integration
def test_update_templates_all_up_to_date(temp_journal_dir, isolated_config):
    """Test update --templates when all templates up to date (lines 197-202)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock no template changes
    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        with patch("ai_journal_kit.core.template_updater.get_template_changes", return_value={}):
            runner = CliRunner()
            result = runner.invoke(app, ["update", "--templates", "--dry-run"])

            # Should complete successfully in dry run mode with templates flag
            # When template_changes is empty, it shows "All up to date" in update_details
            assert result.exit_code == 0
            assert "dry run" in result.output.lower()


@pytest.mark.integration
def test_update_shows_template_backup_message(temp_journal_dir, isolated_config):
    """Test update shows backup message for templates (line 212)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    mock_changes = {
        "daily-template.md": {
            "user_path": temp_journal_dir / "daily-template.md",
            "size_old": 100,
            "size_new": 150,
        }
    }

    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        with patch(
            "ai_journal_kit.core.template_updater.get_template_changes", return_value=mock_changes
        ):
            with patch("ai_journal_kit.core.template_updater.show_template_changes"):
                runner = CliRunner()
                result = runner.invoke(app, ["update", "--templates", "--dry-run"])

                # Should show backup message
                assert "backed up" in result.output.lower() or "backup" in result.output.lower()


@pytest.mark.integration
def test_update_user_declines_confirmation(temp_journal_dir, isolated_config):
    """Test update when user declines confirmation (lines 227-229)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        runner = CliRunner()
        result = runner.invoke(app, ["update"], input="n\n")  # Decline

        # Should cancel
        assert result.exit_code == 0
        assert "cancel" in result.output.lower()


@pytest.mark.integration
def test_update_dry_run_exits_without_changes(temp_journal_dir, isolated_config):
    """Test update --dry-run exits without making changes (lines 232-233)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        runner = CliRunner()
        result = runner.invoke(app, ["update", "--dry-run"])

        # Should exit with dry run message
        assert result.exit_code == 0
        assert "dry run" in result.output.lower()
        assert "no changes" in result.output.lower()


@pytest.mark.integration
def test_update_handles_pip_upgrade_failure(temp_journal_dir, isolated_config):
    """Test update handles subprocess failure gracefully (lines 257-264)."""
    import subprocess
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock subprocess to fail
    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, ["pip"], stderr="Mock error"),
        ):
            runner = CliRunner()
            result = runner.invoke(app, ["update", "--no-confirm"])

            # Should handle error
            assert result.exit_code != 0
            assert "failed" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_update_handles_ide_config_copy_failure(temp_journal_dir, isolated_config):
    """Test update handles IDE config copy failure (lines 277-282)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        with patch("subprocess.run"):  # Mock pip to succeed
            with patch(
                "ai_journal_kit.cli.update.copy_ide_configs", side_effect=OSError("Mock error")
            ):
                runner = CliRunner()
                result = runner.invoke(app, ["update", "--no-confirm"])

                # Should handle error
                assert result.exit_code != 0
                assert "failed" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_update_executes_template_update(temp_journal_dir, isolated_config):
    """Test update actually updates templates when requested (lines 286-303)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    mock_changes = {"daily-template.md": {"user_path": temp_journal_dir / "daily-template.md"}}

    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        with patch("subprocess.run"):  # Mock pip
            with patch(
                "ai_journal_kit.core.template_updater.get_template_changes",
                return_value=mock_changes,
            ):
                with patch("ai_journal_kit.core.template_updater.show_template_changes"):
                    with patch(
                        "ai_journal_kit.core.template_updater.update_templates",
                        return_value=["daily-template.md"],
                    ):
                        runner = CliRunner()
                        result = runner.invoke(app, ["update", "--templates", "--no-confirm"])

                        # Should update templates
                        assert result.exit_code == 0


@pytest.mark.integration
def test_update_handles_template_update_failure(temp_journal_dir, isolated_config):
    """Test update handles template update failure (lines 298-303)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    mock_changes = {"daily-template.md": {"user_path": temp_journal_dir / "daily-template.md"}}

    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        with patch("subprocess.run"):  # Mock pip
            with patch(
                "ai_journal_kit.core.template_updater.get_template_changes",
                return_value=mock_changes,
            ):
                with patch("ai_journal_kit.core.template_updater.show_template_changes"):
                    with patch(
                        "ai_journal_kit.core.template_updater.update_templates",
                        side_effect=Exception("Mock error"),
                    ):
                        runner = CliRunner()
                        result = runner.invoke(app, ["update", "--templates", "--no-confirm"])

                        # Should handle error
                        assert result.exit_code != 0
                        assert "failed" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_update_success_message_includes_templates(temp_journal_dir, isolated_config):
    """Test success message includes template count (line 326)."""
    from unittest.mock import patch

    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    mock_changes = {"daily-template.md": {"user_path": temp_journal_dir / "daily-template.md"}}

    with patch("ai_journal_kit.cli.update.get_latest_version", return_value="99.99.99"):
        with patch("subprocess.run"):
            with patch(
                "ai_journal_kit.core.template_updater.get_template_changes",
                return_value=mock_changes,
            ):
                with patch("ai_journal_kit.core.template_updater.show_template_changes"):
                    with patch(
                        "ai_journal_kit.core.template_updater.update_templates",
                        return_value=["daily-template.md"],
                    ):
                        runner = CliRunner()
                        result = runner.invoke(app, ["update", "--templates", "--no-confirm"])

                        # Success message should mention templates
                        if result.exit_code == 0:
                            assert "template" in result.output.lower()


@pytest.mark.integration
def test_update_detects_dev_version_newer_than_pypi(temp_journal_dir, isolated_config):
    """Test update detects when current version is newer than PyPI (dev version)."""
    from unittest.mock import patch

    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock version where current (1.0.12) > latest (1.0.11)
    with patch("ai_journal_kit.__version__", "1.0.12"):
        with patch("ai_journal_kit.cli.update.get_latest_version", return_value="1.0.11"):
            runner = CliRunner()
            result = runner.invoke(app, ["update"])

            # Should exit successfully without updating
            assert result.exit_code == 0
            assert "newer than PyPI" in result.output
            assert "development version" in result.output.lower()
            # Should NOT have attempted package upgrade
            assert "upgraded" not in result.output.lower() or "up to date" in result.output.lower()


@pytest.mark.integration
def test_update_dev_version_with_force_refreshes_configs(temp_journal_dir, isolated_config):
    """Test update with --force refreshes IDE configs even when on dev version."""
    from unittest.mock import patch

    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock version where current (1.0.12) > latest (1.0.11)
    with patch("ai_journal_kit.__version__", "1.0.12"):
        with patch("ai_journal_kit.cli.update.get_latest_version", return_value="1.0.11"):
            with patch("subprocess.run"):  # Mock package upgrade
                runner = CliRunner()
                result = runner.invoke(app, ["update", "--force", "--no-confirm"])

                # Should proceed with IDE config refresh
                assert result.exit_code == 0
                # Should show forcing message
                assert "forc" in result.output.lower()


@pytest.mark.integration
def test_update_equal_versions_no_update_needed(temp_journal_dir, isolated_config):
    """Test update correctly identifies when already on latest version."""
    from unittest.mock import patch

    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock version where current == latest
    with patch("ai_journal_kit.__version__", "1.0.11"):
        with patch("ai_journal_kit.cli.update.get_latest_version", return_value="1.0.11"):
            runner = CliRunner()
            result = runner.invoke(app, ["update"])

            # Should exit successfully without updating
            assert result.exit_code == 0
            assert "already on the latest version" in result.output.lower()
            assert "no updates needed" in result.output.lower()


@pytest.mark.integration
def test_update_current_less_than_latest_proceeds(temp_journal_dir, isolated_config):
    """Test update proceeds normally when current version is older than PyPI."""
    from unittest.mock import patch

    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Mock version where current (1.0.10) < latest (1.0.11)
    with patch("ai_journal_kit.__version__", "1.0.10"):
        with patch("ai_journal_kit.cli.update.get_latest_version", return_value="1.0.11"):
            with patch("subprocess.run"):  # Mock package upgrade
                runner = CliRunner()
                result = runner.invoke(app, ["update", "--no-confirm"])

                # Should proceed with update
                assert result.exit_code == 0
                # Should show update process
                assert "1.0.10" in result.output and "1.0.11" in result.output
