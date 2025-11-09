"""
Unit tests for UI utilities.

Tests Rich console output and interactive prompts.
"""

from io import StringIO
from unittest.mock import patch

import pytest
from rich.console import Console

from ai_journal_kit.utils.ui import (
    ask_ide,
    ask_path,
    confirm,
    show_error,
    show_markdown,
    show_panel,
    show_progress,
    show_success,
    show_table,
)


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.Prompt.ask")
def test_ask_path_with_default(mock_ask):
    """Test ask_path returns user input with default."""
    mock_ask.return_value = "/home/user/journal"

    result = ask_path("Where should we create your journal?")

    assert result == "/home/user/journal"
    mock_ask.assert_called_once()
    # Check that default was passed
    call_args = mock_ask.call_args
    assert call_args.kwargs["default"] == "~/journal"


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.Prompt.ask")
def test_ask_path_with_custom_default(mock_ask):
    """Test ask_path accepts custom default."""
    mock_ask.return_value = "/custom/path"

    result = ask_path("Path?", default="/custom/default")

    assert result == "/custom/path"
    call_args = mock_ask.call_args
    assert call_args.kwargs["default"] == "/custom/default"


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.questionary.select")
def test_ask_ide_returns_cursor(mock_select):
    """Test ask_ide maps Cursor selection correctly."""
    mock_select.return_value.ask.return_value = "Cursor"

    result = ask_ide()

    assert result == "cursor"


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.questionary.select")
def test_ask_ide_returns_windsurf(mock_select):
    """Test ask_ide maps Windsurf selection correctly."""
    mock_select.return_value.ask.return_value = "Windsurf"

    result = ask_ide()

    assert result == "windsurf"


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.questionary.select")
def test_ask_ide_returns_claude_code(mock_select):
    """Test ask_ide maps Claude Code selection correctly."""
    mock_select.return_value.ask.return_value = "Claude Code (Cline)"

    result = ask_ide()

    assert result == "claude-code"


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.questionary.select")
def test_ask_ide_returns_copilot(mock_select):
    """Test ask_ide maps GitHub Copilot selection correctly."""
    mock_select.return_value.ask.return_value = "GitHub Copilot"

    result = ask_ide()

    assert result == "copilot"


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.questionary.select")
def test_ask_ide_returns_all(mock_select):
    """Test ask_ide maps 'All of the above' selection correctly."""
    mock_select.return_value.ask.return_value = "All of the above"

    result = ask_ide()

    assert result == "all"


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.questionary.select")
def test_ask_ide_with_custom_prompt(mock_select):
    """Test ask_ide accepts custom prompt."""
    mock_select.return_value.ask.return_value = "Cursor"

    result = ask_ide("Pick your editor:")

    assert result == "cursor"
    # Verify prompt was passed
    call_args = mock_select.call_args
    assert call_args[0][0] == "Pick your editor:"


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.Confirm.ask")
def test_confirm_returns_true(mock_confirm):
    """Test confirm returns True when user confirms."""
    mock_confirm.return_value = True

    result = confirm("Continue?")

    assert result is True


@pytest.mark.unit
@patch("ai_journal_kit.utils.ui.Confirm.ask")
def test_confirm_returns_false(mock_confirm):
    """Test confirm returns False when user declines."""
    mock_confirm.return_value = False

    result = confirm("Delete everything?")

    assert result is False


@pytest.mark.unit
def test_show_progress_executes_tasks():
    """Test show_progress executes all tasks in order."""
    executed = []

    def task1():
        executed.append("task1")

    def task2():
        executed.append("task2")

    tasks = [("Task 1", task1), ("Task 2", task2)]

    show_progress(tasks)

    assert executed == ["task1", "task2"]


@pytest.mark.unit
def test_show_progress_handles_single_task():
    """Test show_progress works with single task."""
    executed = []

    def task():
        executed.append("done")

    tasks = [("Single Task", task)]

    show_progress(tasks)

    assert executed == ["done"]


@pytest.mark.unit
def test_show_table_creates_table():
    """Test show_table creates and displays table."""
    # Capture console output
    console = Console(file=StringIO())

    with patch("ai_journal_kit.utils.ui.console", console):
        show_table(
            title="Test Table",
            columns=[("Name", "cyan"), ("Value", "green")],
            rows=[["Item 1", "100"], ["Item 2", "200"]],
        )

    output = console.file.getvalue()
    assert "Test Table" in output
    assert "Name" in output
    assert "Value" in output


@pytest.mark.unit
def test_show_table_handles_empty_rows():
    """Test show_table handles empty rows gracefully."""
    console = Console(file=StringIO())

    with patch("ai_journal_kit.utils.ui.console", console):
        show_table(title="Empty Table", columns=[("Column", "white")], rows=[])

    output = console.file.getvalue()
    # Title may be split across lines in table formatting
    assert "Empty" in output or "Table" in output
    assert "Column" in output


@pytest.mark.unit
def test_show_panel_displays_content():
    """Test show_panel displays content in panel."""
    console = Console(file=StringIO())

    with patch("ai_journal_kit.utils.ui.console", console):
        show_panel("Test content", title="Test Panel", border_style="blue")

    output = console.file.getvalue()
    assert "Test content" in output
    assert "Test Panel" in output


@pytest.mark.unit
def test_show_panel_without_title():
    """Test show_panel works without title."""
    console = Console(file=StringIO())

    with patch("ai_journal_kit.utils.ui.console", console):
        show_panel("Content only")

    output = console.file.getvalue()
    assert "Content only" in output


@pytest.mark.unit
def test_show_error_displays_message():
    """Test show_error displays error message."""
    error_console = Console(file=StringIO(), stderr=True)

    with patch("ai_journal_kit.utils.ui.error_console", error_console):
        show_error("Something went wrong")

    output = error_console.file.getvalue()
    assert "Error:" in output
    assert "Something went wrong" in output


@pytest.mark.unit
def test_show_error_with_suggestion():
    """Test show_error displays suggestion when provided."""
    error_console = Console(file=StringIO(), stderr=True)

    with patch("ai_journal_kit.utils.ui.error_console", error_console):
        show_error("File not found", suggestion="Check the path")

    output = error_console.file.getvalue()
    assert "Error:" in output
    assert "File not found" in output
    assert "Suggestion:" in output
    assert "Check the path" in output


@pytest.mark.unit
def test_show_success_displays_message():
    """Test show_success displays success message."""
    console = Console(file=StringIO())

    with patch("ai_journal_kit.utils.ui.console", console):
        show_success("Setup complete!")

    output = console.file.getvalue()
    assert "Setup complete!" in output


@pytest.mark.unit
def test_show_markdown_renders_markdown():
    """Test show_markdown renders markdown text."""
    console = Console(file=StringIO())

    with patch("ai_journal_kit.utils.ui.console", console):
        show_markdown("# Heading\n\nParagraph with **bold** text.")

    output = console.file.getvalue()
    # Rich will transform markdown
    assert "Heading" in output


@pytest.mark.unit
def test_show_markdown_handles_empty_string():
    """Test show_markdown handles empty markdown."""
    console = Console(file=StringIO())

    with patch("ai_journal_kit.utils.ui.console", console):
        show_markdown("")

    # Should not raise an error
    output = console.file.getvalue()
    assert isinstance(output, str)
