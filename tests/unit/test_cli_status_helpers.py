"""
Unit tests for status command.

Tests configuration display and health checks.
"""

from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console

from ai_journal_kit.cli.status import _check_ide_configs, _print_check


@pytest.mark.unit
def test_check_ide_configs_cursor(temp_journal_dir):
    """Test IDE config check for Cursor."""
    (temp_journal_dir / ".cursor" / "rules").mkdir(parents=True)

    config = MagicMock()
    config.ide = "cursor"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    assert result is True


@pytest.mark.unit
def test_check_ide_configs_cursor_missing(temp_journal_dir):
    """Test IDE config check when Cursor config is missing."""
    config = MagicMock()
    config.ide = "cursor"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    assert result is False


@pytest.mark.unit
def test_check_ide_configs_windsurf(temp_journal_dir):
    """Test IDE config check for Windsurf."""
    (temp_journal_dir / ".windsurf" / "rules").mkdir(parents=True)

    config = MagicMock()
    config.ide = "windsurf"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    assert result is True


@pytest.mark.unit
def test_check_ide_configs_windsurf_missing(temp_journal_dir):
    """Test IDE config check when Windsurf config is missing."""
    config = MagicMock()
    config.ide = "windsurf"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    assert result is False


@pytest.mark.unit
def test_check_ide_configs_claude_code(temp_journal_dir):
    """Test IDE config check for Claude Code."""
    (temp_journal_dir / "CLAUDE.md").touch()

    config = MagicMock()
    config.ide = "claude-code"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    assert result is True


@pytest.mark.unit
def test_check_ide_configs_claude_code_missing(temp_journal_dir):
    """Test IDE config check when Claude Code config is missing."""
    config = MagicMock()
    config.ide = "claude-code"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    assert result is False


@pytest.mark.unit
def test_check_ide_configs_copilot(temp_journal_dir):
    """Test IDE config check for GitHub Copilot."""
    (temp_journal_dir / ".github").mkdir()
    (temp_journal_dir / ".github" / "copilot-instructions.md").touch()

    config = MagicMock()
    config.ide = "copilot"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    assert result is True


@pytest.mark.unit
def test_check_ide_configs_copilot_missing(temp_journal_dir):
    """Test IDE config check when Copilot config is missing."""
    config = MagicMock()
    config.ide = "copilot"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    assert result is False


@pytest.mark.unit
def test_check_ide_configs_all(temp_journal_dir):
    """Test IDE config check for 'all' option."""
    config = MagicMock()
    config.ide = "all"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    # 'all' always returns True
    assert result is True


@pytest.mark.unit
def test_check_ide_configs_unknown(temp_journal_dir):
    """Test IDE config check for unknown IDE."""
    config = MagicMock()
    config.ide = "unknown"
    config.journal_location = temp_journal_dir

    result = _check_ide_configs(config)

    assert result is False


@pytest.mark.unit
def test_print_check_passed():
    """Test _print_check displays passed check."""
    console = Console(file=StringIO())

    with patch("ai_journal_kit.cli.status.console", console):
        _print_check("Test check", True)

    output = console.file.getvalue()
    assert "✓" in output
    assert "Test check" in output


@pytest.mark.unit
def test_print_check_failed():
    """Test _print_check displays failed check."""
    console = Console(file=StringIO())

    with patch("ai_journal_kit.cli.status.console", console):
        _print_check("Test check", False)

    output = console.file.getvalue()
    assert "✗" in output
    assert "Test check" in output
