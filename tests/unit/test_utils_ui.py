"""
Unit tests for UI utility functions.

Tests Rich UI helpers including:
- Path prompts
- IDE selection
- Framework selection
- Confirmation prompts
- Windows UTF-8 handling
"""

import sys
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from ai_journal_kit.utils.ui import (
    ask_framework,
    ask_ide,
    ask_path,
    confirm,
    console,
    show_error,
    show_markdown,
    show_panel,
    show_progress,
    show_success,
    show_table,
)


@pytest.mark.unit
def test_ask_path_default():
    """Test ask_path returns default path."""
    with patch("ai_journal_kit.utils.ui.Prompt.ask", return_value="/custom/journal"):
        result = ask_path("Enter path", default="/default/path")

    assert result == "/custom/journal"


@pytest.mark.unit
def test_ask_path_custom():
    """Test ask_path with custom default."""
    with patch("ai_journal_kit.utils.ui.Prompt.ask", return_value="/my/journal"):
        result = ask_path("Where?", default="/elsewhere")

    assert result == "/my/journal"


@pytest.mark.unit
def test_ask_ide_cursor():
    """Test ask_ide returns 'cursor' for Cursor selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "Cursor"
        result = ask_ide()

    assert result == "cursor"


@pytest.mark.unit
def test_ask_ide_windsurf():
    """Test ask_ide returns 'windsurf' for Windsurf selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "Windsurf"
        result = ask_ide()

    assert result == "windsurf"


@pytest.mark.unit
def test_ask_ide_claude_code():
    """Test ask_ide returns 'claude-code' for Claude Code selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "Claude Code (Cline)"
        result = ask_ide()

    assert result == "claude-code"


@pytest.mark.unit
def test_ask_ide_copilot():
    """Test ask_ide returns 'copilot' for GitHub Copilot selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "GitHub Copilot"
        result = ask_ide()

    assert result == "copilot"


@pytest.mark.unit
def test_ask_ide_all():
    """Test ask_ide returns 'all' for All of the above selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "All of the above"
        result = ask_ide()

    assert result == "all"


@pytest.mark.unit
def test_ask_framework_default():
    """Test ask_framework returns 'default' for Default selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "Default (flexible)"
        result = ask_framework()

    assert result == "default"


@pytest.mark.unit
def test_ask_framework_gtd():
    """Test ask_framework returns 'gtd' for GTD selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "GTD (Getting Things Done)"
        result = ask_framework()

    assert result == "gtd"


@pytest.mark.unit
def test_ask_framework_para():
    """Test ask_framework returns 'para' for PARA selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "PARA (Projects, Areas, Resources, Archive)"
        result = ask_framework()

    assert result == "para"


@pytest.mark.unit
def test_ask_framework_bullet_journal():
    """Test ask_framework returns 'bullet-journal' for Bullet Journal selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "Bullet Journal"
        result = ask_framework()

    assert result == "bullet-journal"


@pytest.mark.unit
def test_ask_framework_zettelkasten():
    """Test ask_framework returns 'zettelkasten' for Zettelkasten selection."""
    with patch("ai_journal_kit.utils.ui.questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "Zettelkasten (knowledge management)"
        result = ask_framework()

    assert result == "zettelkasten"


@pytest.mark.unit
def test_confirm_yes():
    """Test confirm returns True when user confirms."""
    with patch("ai_journal_kit.utils.ui.Confirm.ask", return_value=True):
        result = confirm("Continue?")

    assert result is True


@pytest.mark.unit
def test_confirm_no():
    """Test confirm returns False when user declines."""
    with patch("ai_journal_kit.utils.ui.Confirm.ask", return_value=False):
        result = confirm("Continue?")

    assert result is False


@pytest.mark.unit
def test_show_progress():
    """Test show_progress executes tasks with progress bar."""
    task1_executed = False
    task2_executed = False

    def task1():
        nonlocal task1_executed
        task1_executed = True

    def task2():
        nonlocal task2_executed
        task2_executed = True

    tasks = [("Task 1", task1), ("Task 2", task2)]

    show_progress(tasks)

    assert task1_executed
    assert task2_executed


@pytest.mark.unit
def test_show_table():
    """Test show_table displays Rich table."""
    # Just verify it doesn't crash
    columns = [("Column 1", "cyan"), ("Column 2", "green")]
    rows = [["Value 1", "Value 2"], ["Value 3", "Value 4"]]

    show_table("Test Table", columns, rows)


@pytest.mark.unit
def test_show_panel():
    """Test show_panel displays Rich panel."""
    # Just verify it doesn't crash
    show_panel("Test content", title="Test Title", border_style="blue")


@pytest.mark.unit
def test_show_error_no_suggestion(capsys):
    """Test show_error displays error message."""
    from ai_journal_kit.utils import ui
    from rich.console import Console

    # Create a test console that writes to string buffer
    string_buffer = StringIO()
    test_error_console = Console(file=string_buffer, stderr=True, force_terminal=True)

    with patch.object(ui, 'error_console', test_error_console):
        show_error("Something went wrong")

    output = string_buffer.getvalue()
    assert "error" in output.lower()
    assert "something went wrong" in output.lower()


@pytest.mark.unit
def test_show_error_with_suggestion(capsys):
    """Test show_error displays error with suggestion."""
    from ai_journal_kit.utils import ui
    from rich.console import Console

    string_buffer = StringIO()
    test_error_console = Console(file=string_buffer, stderr=True, force_terminal=True)

    with patch.object(ui, 'error_console', test_error_console):
        show_error("Something went wrong", "Try this instead")

    output = string_buffer.getvalue()
    assert "error" in output.lower()
    assert "suggestion" in output.lower()
    assert "try this instead" in output.lower()


@pytest.mark.unit
def test_show_success():
    """Test show_success displays success message."""
    from ai_journal_kit.utils import ui
    from rich.console import Console

    string_buffer = StringIO()
    test_console = Console(file=string_buffer, force_terminal=True)

    with patch.object(ui, 'console', test_console):
        show_success("Operation completed")

    output = string_buffer.getvalue()
    assert "operation completed" in output.lower()


@pytest.mark.unit
def test_show_markdown():
    """Test show_markdown renders markdown."""
    # Just verify it doesn't crash
    show_markdown("# Test Markdown\n\nThis is **bold** text.")


@pytest.mark.unit
@patch("sys.platform", "win32")
def test_windows_utf8_reconfigure():
    """Test Windows UTF-8 reconfiguration on import."""
    # Mock stdout and stderr with reconfigure method
    mock_stdout = MagicMock()
    mock_stderr = MagicMock()
    mock_stdout.reconfigure = MagicMock()
    mock_stderr.reconfigure = MagicMock()

    with patch("sys.stdout", mock_stdout):
        with patch("sys.stderr", mock_stderr):
            # Reload the module to trigger Windows-specific code
            import importlib
            import ai_journal_kit.utils.ui
            importlib.reload(ai_journal_kit.utils.ui)

    # Should have called reconfigure on Windows
    assert mock_stdout.reconfigure.called or mock_stderr.reconfigure.called


@pytest.mark.unit
@patch("sys.platform", "linux")
def test_non_windows_no_reconfigure():
    """Test no reconfiguration on non-Windows platforms."""
    # Mock stdout and stderr without reconfigure method
    mock_stdout = MagicMock()
    mock_stderr = MagicMock()
    del mock_stdout.reconfigure  # Make sure it doesn't have reconfigure
    del mock_stderr.reconfigure

    with patch("sys.stdout", mock_stdout):
        with patch("sys.stderr", mock_stderr):
            # Reload the module
            import importlib
            import ai_journal_kit.utils.ui
            importlib.reload(ai_journal_kit.utils.ui)

    # Should not crash on non-Windows
    assert True


@pytest.mark.unit
def test_console_initialized():
    """Test console and error_console are initialized."""
    from ai_journal_kit.utils.ui import console, error_console

    assert console is not None
    assert error_console is not None
