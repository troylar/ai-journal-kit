"""
Unit tests for list command.

Tests journal listing including:
- No journals configured
- Single journal
- Multiple journals
- JSON output
"""

from unittest.mock import MagicMock, patch

import pytest
import typer

from ai_journal_kit.cli.list_journals import list_journals


@pytest.mark.unit
def test_list_journals_no_journals_configured():
    """Test list command when no journals configured (lines 25-28)."""
    # Test with None multi_config
    with patch("ai_journal_kit.cli.list_journals.load_multi_journal_config", return_value=None):
        with patch("ai_journal_kit.cli.list_journals.show_error") as mock_error:
            with pytest.raises(typer.Exit) as exc_info:
                list_journals()

    assert exc_info.value.exit_code == 1
    mock_error.assert_called_once()


@pytest.mark.unit
def test_list_journals_empty_journals_dict():
    """Test list command when journals dict is empty (lines 25-28)."""
    mock_multi_config = MagicMock()
    mock_multi_config.journals = {}

    with patch("ai_journal_kit.cli.list_journals.load_multi_journal_config", return_value=mock_multi_config):
        with patch("ai_journal_kit.cli.list_journals.show_error") as mock_error:
            with pytest.raises(typer.Exit) as exc_info:
                list_journals()

    assert exc_info.value.exit_code == 1
    mock_error.assert_called_once()


@pytest.mark.unit
def test_list_journals_table_output():
    """Test list command with table output."""
    from datetime import datetime
    from pathlib import Path

    mock_profile = MagicMock()
    mock_profile.location = Path("/test/journal")
    mock_profile.framework = "gtd"
    mock_profile.ide = "cursor"
    mock_profile.version = "1.0.0"
    mock_profile.created_at = datetime.now()
    mock_profile.last_updated = datetime.now()

    mock_multi_config = MagicMock()
    mock_multi_config.journals = {"default": mock_profile}

    with patch("ai_journal_kit.cli.list_journals.load_multi_journal_config", return_value=mock_multi_config):
        with patch("ai_journal_kit.cli.list_journals.get_active_journal_name", return_value="default"):
            with patch("ai_journal_kit.cli.list_journals.console"):
                list_journals(json_output=False)


@pytest.mark.unit
def test_list_journals_json_output(capsys):
    """Test list command with JSON output."""
    from datetime import datetime
    from pathlib import Path

    mock_profile = MagicMock()
    mock_profile.location = Path("/test/journal")
    mock_profile.framework = "gtd"
    mock_profile.ide = "cursor"
    mock_profile.version = "1.0.0"
    mock_profile.created_at = datetime.now()
    mock_profile.last_updated = datetime.now()

    mock_multi_config = MagicMock()
    mock_multi_config.journals = {"default": mock_profile}

    with patch("ai_journal_kit.cli.list_journals.load_multi_journal_config", return_value=mock_multi_config):
        with patch("ai_journal_kit.cli.list_journals.get_active_journal_name", return_value="default"):
            list_journals(json_output=True)

    captured = capsys.readouterr()
    assert "default" in captured.out
    assert "gtd" in captured.out


@pytest.mark.unit
def test_list_journals_multiple_journals():
    """Test list command with multiple journals."""
    from datetime import datetime
    from pathlib import Path

    mock_profile1 = MagicMock()
    mock_profile1.location = Path("/test/journal1")
    mock_profile1.framework = "gtd"
    mock_profile1.ide = "cursor"
    mock_profile1.version = "1.0.0"
    mock_profile1.created_at = datetime.now()
    mock_profile1.last_updated = datetime.now()

    mock_profile2 = MagicMock()
    mock_profile2.location = Path("/test/journal2")
    mock_profile2.framework = "para"
    mock_profile2.ide = "windsurf"
    mock_profile2.version = "1.0.0"
    mock_profile2.created_at = datetime.now()
    mock_profile2.last_updated = datetime.now()

    mock_multi_config = MagicMock()
    mock_multi_config.journals = {"work": mock_profile1, "personal": mock_profile2}

    with patch("ai_journal_kit.cli.list_journals.load_multi_journal_config", return_value=mock_multi_config):
        with patch("ai_journal_kit.cli.list_journals.get_active_journal_name", return_value="work"):
            with patch("ai_journal_kit.cli.list_journals.console"):
                list_journals(json_output=False)


@pytest.mark.unit
def test_list_journals_inactive_journal():
    """Test list command shows inactive journal correctly."""
    from datetime import datetime
    from pathlib import Path

    mock_profile1 = MagicMock()
    mock_profile1.location = Path("/test/journal1")
    mock_profile1.framework = "gtd"
    mock_profile1.ide = "cursor"
    mock_profile1.version = "1.0.0"
    mock_profile1.created_at = datetime.now()
    mock_profile1.last_updated = datetime.now()

    mock_profile2 = MagicMock()
    mock_profile2.location = Path("/test/journal2")
    mock_profile2.framework = "para"
    mock_profile2.ide = "windsurf"
    mock_profile2.version = "1.0.0"
    mock_profile2.created_at = datetime.now()
    mock_profile2.last_updated = datetime.now()

    mock_multi_config = MagicMock()
    mock_multi_config.journals = {"work": mock_profile1, "personal": mock_profile2}

    with patch("ai_journal_kit.cli.list_journals.load_multi_journal_config", return_value=mock_multi_config):
        with patch("ai_journal_kit.cli.list_journals.get_active_journal_name", return_value="work"):
            with patch("ai_journal_kit.cli.list_journals.console"):
                list_journals(json_output=False)
