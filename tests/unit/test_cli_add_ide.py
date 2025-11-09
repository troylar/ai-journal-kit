"""
Unit tests for add-ide command.

Tests IDE configuration installation including:
- Interactive IDE selection
- Validation
- Installation success/failure
- Error handling
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from ai_journal_kit.cli.add_ide import add_ide


@pytest.mark.unit
def test_add_ide_not_set_up():
    """Test add-ide fails when journal not set up."""
    with patch("ai_journal_kit.cli.add_ide.load_config", return_value=None):
        with patch("ai_journal_kit.cli.add_ide.show_error"):
            with pytest.raises(typer.Exit) as exc_info:
                add_ide("cursor")

    assert exc_info.value.exit_code == 1


@pytest.mark.unit
def test_add_ide_interactive_selection():
    """Test add-ide with interactive IDE selection (line 37)."""
    mock_config = MagicMock()
    mock_config.journal_location = Path("/fake/journal")

    with patch("ai_journal_kit.cli.add_ide.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.add_ide.ask_ide", return_value="cursor") as mock_ask:
            with patch("ai_journal_kit.cli.add_ide.validate_ide", return_value="cursor"):
                with patch("ai_journal_kit.cli.add_ide.copy_ide_configs"):
                    with patch("ai_journal_kit.cli.add_ide.console"):
                        with patch("ai_journal_kit.cli.add_ide.show_success"):
                            add_ide(None)  # No IDE argument triggers interactive

    # Should have called ask_ide for interactive selection
    mock_ask.assert_called_once_with("Which AI editor would you like to add?")


@pytest.mark.unit
def test_add_ide_invalid_ide():
    """Test add-ide with invalid IDE name."""
    mock_config = MagicMock()
    mock_config.journal_location = Path("/fake/journal")

    with patch("ai_journal_kit.cli.add_ide.load_config", return_value=mock_config):
        with patch(
            "ai_journal_kit.cli.add_ide.validate_ide", side_effect=ValueError("Invalid IDE")
        ):
            with patch("ai_journal_kit.cli.add_ide.show_error"):
                with pytest.raises(typer.Exit) as exc_info:
                    add_ide("invalid-ide")

    assert exc_info.value.exit_code == 1


@pytest.mark.unit
def test_add_ide_copy_exception(temp_journal_dir):
    """Test add-ide handles copy_ide_configs exception (lines 68-70)."""
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.add_ide.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.add_ide.validate_ide", return_value="cursor"):
            with patch(
                "ai_journal_kit.cli.add_ide.copy_ide_configs", side_effect=Exception("Copy failed")
            ):
                with patch("ai_journal_kit.cli.add_ide.console"):
                    with patch("ai_journal_kit.cli.add_ide.show_error") as mock_error:
                        with pytest.raises(typer.Exit) as exc_info:
                            add_ide("cursor")

    assert exc_info.value.exit_code == 1
    # Should show error with exception message
    mock_error.assert_called_with("Failed to install IDE configuration", "Copy failed")


@pytest.mark.unit
def test_add_ide_cursor_success(temp_journal_dir):
    """Test successful installation of Cursor IDE."""
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.add_ide.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.add_ide.validate_ide", return_value="cursor"):
            with patch("ai_journal_kit.cli.add_ide.copy_ide_configs"):
                with patch("ai_journal_kit.cli.add_ide.console"):
                    with patch("ai_journal_kit.cli.add_ide.show_success") as mock_success:
                        add_ide("cursor")

    # Should show success message
    mock_success.assert_called_once()
    success_msg = mock_success.call_args[0][0]
    assert "cursor" in success_msg.lower()


@pytest.mark.unit
def test_add_ide_all_success(temp_journal_dir):
    """Test successful installation of all IDE configs."""
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.add_ide.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.add_ide.validate_ide", return_value="all"):
            with patch("ai_journal_kit.cli.add_ide.copy_ide_configs"):
                with patch("ai_journal_kit.cli.add_ide.console"):
                    with patch("ai_journal_kit.cli.add_ide.show_success") as mock_success:
                        add_ide("all")

    # Should mention all IDEs in success message
    success_msg = mock_success.call_args[0][0]
    assert "cursor" in success_msg.lower()
    assert "windsurf" in success_msg.lower()
    assert "claude code" in success_msg.lower()
    assert "copilot" in success_msg.lower()


@pytest.mark.unit
def test_add_ide_windsurf_success(temp_journal_dir):
    """Test successful installation of Windsurf IDE."""
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.add_ide.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.add_ide.validate_ide", return_value="windsurf"):
            with patch("ai_journal_kit.cli.add_ide.copy_ide_configs"):
                with patch("ai_journal_kit.cli.add_ide.console"):
                    with patch("ai_journal_kit.cli.add_ide.show_success") as mock_success:
                        add_ide("windsurf")

    success_msg = mock_success.call_args[0][0]
    assert "windsurf" in success_msg.lower()


@pytest.mark.unit
def test_add_ide_claude_code_success(temp_journal_dir):
    """Test successful installation of Claude Code IDE."""
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.add_ide.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.add_ide.validate_ide", return_value="claude-code"):
            with patch("ai_journal_kit.cli.add_ide.copy_ide_configs"):
                with patch("ai_journal_kit.cli.add_ide.console"):
                    with patch("ai_journal_kit.cli.add_ide.show_success") as mock_success:
                        add_ide("claude-code")

    success_msg = mock_success.call_args[0][0]
    assert "claude code" in success_msg.lower()


@pytest.mark.unit
def test_add_ide_copilot_success(temp_journal_dir):
    """Test successful installation of GitHub Copilot IDE."""
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.add_ide.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.add_ide.validate_ide", return_value="copilot"):
            with patch("ai_journal_kit.cli.add_ide.copy_ide_configs"):
                with patch("ai_journal_kit.cli.add_ide.console"):
                    with patch("ai_journal_kit.cli.add_ide.show_success") as mock_success:
                        add_ide("copilot")

    success_msg = mock_success.call_args[0][0]
    assert "copilot" in success_msg.lower()
