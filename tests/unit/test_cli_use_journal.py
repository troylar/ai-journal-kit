"""
Unit tests for use command.

Tests journal switching including:
- No journals configured
- Journal not found
- Successful switch
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from ai_journal_kit.cli.use_journal import use_journal


@pytest.mark.unit
def test_use_journal_no_config():
    """Test use command when no journals configured (lines 29-30)."""
    with patch("ai_journal_kit.cli.use_journal.load_multi_journal_config", return_value=None):
        with patch("ai_journal_kit.cli.use_journal.show_error") as mock_error:
            with pytest.raises(typer.Exit) as exc_info:
                use_journal("test")

    assert exc_info.value.exit_code == 1
    mock_error.assert_called_once_with("No journals configured", "Run 'ai-journal-kit setup' first")


@pytest.mark.unit
def test_use_journal_not_found():
    """Test use command with non-existent journal."""
    mock_multi_config = MagicMock()
    mock_multi_config.has_journal.return_value = False
    mock_multi_config.journals = {"work": MagicMock(), "personal": MagicMock()}

    with patch(
        "ai_journal_kit.cli.use_journal.load_multi_journal_config", return_value=mock_multi_config
    ):
        with patch("ai_journal_kit.cli.use_journal.show_error") as mock_error:
            with pytest.raises(typer.Exit) as exc_info:
                use_journal("nonexistent")

    assert exc_info.value.exit_code == 1
    # Should suggest available journals
    error_call = mock_error.call_args
    assert "not found" in error_call[0][0].lower()
    assert "work" in error_call[0][1] or "personal" in error_call[0][1]


@pytest.mark.unit
def test_use_journal_success():
    """Test successful journal switch."""
    mock_profile = MagicMock()
    mock_profile.location = Path("/test/journal")
    mock_profile.framework = "gtd"
    mock_profile.ide = "cursor"

    mock_multi_config = MagicMock()
    mock_multi_config.has_journal.return_value = True
    mock_multi_config.journals = {"work": mock_profile}

    with patch(
        "ai_journal_kit.cli.use_journal.load_multi_journal_config", return_value=mock_multi_config
    ):
        with patch("ai_journal_kit.cli.use_journal.save_multi_journal_config") as mock_save:
            with patch("ai_journal_kit.cli.use_journal.show_success") as mock_success:
                with patch("ai_journal_kit.cli.use_journal.console"):
                    use_journal("work")

    # Should set active and save
    mock_multi_config.set_active.assert_called_once_with("work")
    mock_save.assert_called_once_with(mock_multi_config)
    mock_success.assert_called_once()


@pytest.mark.unit
def test_use_journal_displays_info():
    """Test use command displays journal info."""
    mock_profile = MagicMock()
    mock_profile.location = Path("/test/journal")
    mock_profile.framework = "para"
    mock_profile.ide = "windsurf"

    mock_multi_config = MagicMock()
    mock_multi_config.has_journal.return_value = True
    mock_multi_config.journals = {"personal": mock_profile}

    with patch(
        "ai_journal_kit.cli.use_journal.load_multi_journal_config", return_value=mock_multi_config
    ):
        with patch("ai_journal_kit.cli.use_journal.save_multi_journal_config"):
            with patch("ai_journal_kit.cli.use_journal.show_success"):
                with patch("ai_journal_kit.cli.use_journal.console"):
                    use_journal("personal")

    # Should successfully complete
    mock_multi_config.set_active.assert_called_once_with("personal")


@pytest.mark.unit
def test_use_journal_multiple_available():
    """Test use command when multiple journals available."""
    mock_profile1 = MagicMock()
    mock_profile1.location = Path("/test/journal1")
    mock_profile1.framework = "gtd"
    mock_profile1.ide = "cursor"

    mock_profile2 = MagicMock()
    mock_profile2.location = Path("/test/journal2")
    mock_profile2.framework = "para"
    mock_profile2.ide = "windsurf"

    mock_multi_config = MagicMock()
    mock_multi_config.has_journal.return_value = True
    mock_multi_config.journals = {"work": mock_profile1, "personal": mock_profile2}

    with patch(
        "ai_journal_kit.cli.use_journal.load_multi_journal_config", return_value=mock_multi_config
    ):
        with patch("ai_journal_kit.cli.use_journal.save_multi_journal_config"):
            with patch("ai_journal_kit.cli.use_journal.show_success"):
                with patch("ai_journal_kit.cli.use_journal.console"):
                    use_journal("work")

    mock_multi_config.set_active.assert_called_once_with("work")
