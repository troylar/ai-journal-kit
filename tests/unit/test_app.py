"""Unit tests for CLI app and version command."""

import pytest
from typer.testing import CliRunner

from ai_journal_kit import __version__
from ai_journal_kit.cli.app import app


@pytest.mark.unit
def test_version_flag():
    """Test --version flag shows version and exits (covers lines 22-23)."""
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output


@pytest.mark.unit
def test_version_flag_short():
    """Test -v flag shows version."""
    runner = CliRunner()
    result = runner.invoke(app, ["-v"])

    assert result.exit_code == 0
    assert __version__ in result.output


@pytest.mark.unit
def test_app_help():
    """Test app shows help message."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "AI Journal Kit" in result.output or "journal" in result.output.lower()


@pytest.mark.unit
def test_app_has_all_commands():
    """Test app registers all commands."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    output_lower = result.output.lower()
    assert "setup" in output_lower
    assert "status" in output_lower
    assert "doctor" in output_lower
    assert "update" in output_lower
    assert "move" in output_lower
