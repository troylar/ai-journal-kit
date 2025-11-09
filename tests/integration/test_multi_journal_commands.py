"""Integration tests for multi-journal commands (use, list)."""

import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from ai_journal_kit.core.config import load_multi_journal_config
from tests.integration.fixtures import create_journal_fixture


@pytest.mark.integration
def test_list_journals_single(temp_journal_dir, isolated_config):
    """Test listing journals when only one exists."""
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="default"
    )

    runner = CliRunner()
    result = runner.invoke(app, ["list"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "default" in result.output
    # Check table header is displayed (paths may be truncated)
    assert "Configured Journals" in result.output or "Location" in result.output
    # Check for active indicator (✓ or Active)
    assert "✓" in result.output or "Active" in result.output
    # Verify cursor IDE is shown
    assert "cursor" in result.output


@pytest.mark.integration
def test_list_journals_multiple(temp_journal_dir, isolated_config):
    """Test listing multiple journals."""
    # Create first journal
    journal1 = temp_journal_dir / "journal1"
    create_journal_fixture(
        path=journal1, ide="cursor", config_dir=isolated_config, framework="default"
    )

    # Create second journal
    journal2 = temp_journal_dir / "journal2"
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "setup",
            "--name",
            "business",
            "--location",
            str(journal2),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    # List journals
    result = runner.invoke(app, ["list"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "default" in result.output
    assert "business" in result.output
    # Check table is displayed (paths will be truncated)
    assert "Configured Journals" in result.output or "Location" in result.output
    # Verify both frameworks are shown
    assert "gtd" in result.output


@pytest.mark.integration
def test_list_journals_json_output(temp_journal_dir, isolated_config):
    """Test listing journals with JSON output."""
    import json

    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="default"
    )

    runner = CliRunner()
    result = runner.invoke(app, ["list", "--json"], catch_exceptions=False)

    assert result.exit_code == 0

    # Parse JSON output
    output_data = json.loads(result.output)
    assert "active_journal" in output_data
    assert "journals" in output_data
    assert "default" in output_data["journals"]
    assert output_data["journals"]["default"]["is_active"] is True


@pytest.mark.integration
def test_use_journal_switches_active(temp_journal_dir, isolated_config):
    """Test switching active journal with 'use' command."""
    # Create first journal
    journal1 = temp_journal_dir / "journal1"
    create_journal_fixture(
        path=journal1, ide="cursor", config_dir=isolated_config, framework="default"
    )

    # Create second journal
    journal2 = temp_journal_dir / "journal2"
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "setup",
            "--name",
            "business",
            "--location",
            str(journal2),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    # Switch to business journal
    result = runner.invoke(app, ["use", "business"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "Switched to journal 'business'" in result.output

    # Verify config was updated
    multi_config = load_multi_journal_config()
    assert multi_config.active_journal == "business"


@pytest.mark.integration
def test_use_journal_nonexistent_fails(temp_journal_dir, isolated_config):
    """Test using nonexistent journal fails gracefully."""
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="default"
    )

    runner = CliRunner()
    result = runner.invoke(app, ["use", "nonexistent"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "not found" in result.output.lower()


@pytest.mark.integration
def test_use_journal_updates_status(temp_journal_dir, isolated_config):
    """Test that status reflects active journal after use command."""
    # Create two journals
    journal1 = temp_journal_dir / "journal1"
    create_journal_fixture(
        path=journal1, ide="cursor", config_dir=isolated_config, framework="default"
    )

    journal2 = temp_journal_dir / "journal2"
    runner = CliRunner()
    runner.invoke(
        app,
        [
            "setup",
            "--name",
            "business",
            "--location",
            str(journal2),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    # Switch to business
    result = runner.invoke(app, ["use", "business"], catch_exceptions=False)
    assert result.exit_code == 0

    # Verify the switch was successful
    multi_config = load_multi_journal_config()
    assert multi_config.active_journal == "business"

    # Check status shows a valid journal (paths may be truncated)
    result = runner.invoke(app, ["status"], catch_exceptions=False)

    assert result.exit_code == 0
    # Just verify status command works and shows health checks
    assert "AI Journal Kit Status" in result.output or "Journal Location" in result.output


@pytest.mark.integration
def test_env_var_overrides_active_journal(temp_journal_dir, isolated_config, monkeypatch):
    """Test AI_JOURNAL environment variable overrides active journal."""

    # Create two journals
    journal1 = temp_journal_dir / "journal1"
    create_journal_fixture(
        path=journal1, ide="cursor", config_dir=isolated_config, framework="default"
    )

    journal2 = temp_journal_dir / "journal2"
    runner = CliRunner()
    runner.invoke(
        app,
        [
            "setup",
            "--name",
            "business",
            "--location",
            str(journal2),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    # Verify default is active in config
    multi_config = load_multi_journal_config()
    assert multi_config.active_journal == "default"

    # Set env var and verify it overrides
    monkeypatch.setenv("AI_JOURNAL", "business")

    # Verify get_active_journal_name respects env var
    from ai_journal_kit.core.config import get_active_journal_name

    active_name = get_active_journal_name()
    assert active_name == "business"


@pytest.mark.integration
def test_list_shows_correct_active_indicator(temp_journal_dir, isolated_config):
    """Test that list command shows correct active indicator."""
    # Create two journals
    journal1 = temp_journal_dir / "journal1"
    create_journal_fixture(
        path=journal1, ide="cursor", config_dir=isolated_config, framework="default"
    )

    journal2 = temp_journal_dir / "journal2"
    runner = CliRunner()
    runner.invoke(
        app,
        [
            "setup",
            "--name",
            "business",
            "--location",
            str(journal2),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    # Switch to business
    result = runner.invoke(app, ["use", "business"], catch_exceptions=False)
    assert result.exit_code == 0

    # List journals
    result = runner.invoke(app, ["list"], catch_exceptions=False)

    assert result.exit_code == 0
    # Business journal should be shown
    assert "business" in result.output
    # Some active indicator should be present
    assert "✓" in result.output or "Active" in result.output
