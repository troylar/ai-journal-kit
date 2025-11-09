"""
Unit tests for the setup CLI command.

Tests path validation, user input handling, and configuration creation.
"""

from pathlib import Path
from unittest.mock import patch

import pytest
import typer

from ai_journal_kit.cli.setup import _detect_existing_journal, _handle_existing_journal
from ai_journal_kit.core.validation import path_is_writable, validate_ide, validate_path


@pytest.mark.unit
def test_validate_path_accepts_valid_directory(tmp_path):
    """Test that validate_path accepts valid directories."""
    test_dir = tmp_path / "journal"
    test_dir.mkdir()

    result = validate_path(str(test_dir))
    assert isinstance(result, Path)
    assert result.exists()


@pytest.mark.unit
def test_validate_path_accepts_file_path(tmp_path):
    """Test that validate_path accepts file paths (returns path, doesn't validate if it's a file)."""
    test_file = tmp_path / "not_a_dir.txt"
    test_file.write_text("test")

    # validate_path doesn't check if it's a file, just normalizes the path
    result = validate_path(str(test_file))
    assert isinstance(result, Path)


@pytest.mark.unit
def test_validate_path_accepts_nonexistent_directory(tmp_path):
    """Test that validate_path accepts non-existent directories in existing parent."""
    test_dir = tmp_path / "new_journal"

    # Should accept path if parent exists
    result = validate_path(str(test_dir))
    assert isinstance(result, Path)


@pytest.mark.unit
def test_validate_path_rejects_invalid_parent():
    """Test that validate_path rejects paths with non-existent parents."""
    with pytest.raises(ValueError, match="Parent directory does not exist"):
        validate_path("/nonexistent/parent/journal")


@pytest.mark.unit
def test_validate_path_rejects_null_byte():
    """Test that validate_path rejects paths with null bytes."""
    with pytest.raises(ValueError, match="Path contains null byte"):
        validate_path("/tmp/test\0path")


@pytest.mark.unit
def test_validate_path_expands_home_directory(tmp_path):
    """Test that validate_path expands ~ to home directory."""
    result = validate_path("~")
    assert isinstance(result, Path)
    assert result.exists()
    assert str(result) != "~"


@pytest.mark.unit
def test_validate_ide_accepts_valid_choices():
    """Test that validate_ide accepts all valid IDE choices (lines 49-55)."""
    valid_ides = ["cursor", "windsurf", "claude-code", "copilot", "all"]

    for ide in valid_ides:
        result = validate_ide(ide)
        assert result == ide.lower()

    # Test case insensitivity
    assert validate_ide("CURSOR") == "cursor"
    assert validate_ide("Windsurf") == "windsurf"


@pytest.mark.unit
def test_validate_ide_rejects_invalid_choice():
    """Test that validate_ide rejects invalid IDE choices (lines 52-53)."""
    with pytest.raises(ValueError, match="Invalid IDE"):
        validate_ide("invalid-ide")

    with pytest.raises(ValueError, match="Must be one of"):
        validate_ide("vscode")


@pytest.mark.unit
def test_path_is_writable_for_existing_directory(tmp_path):
    """Test path_is_writable for existing directories (lines 67-68)."""
    test_dir = tmp_path / "writable"
    test_dir.mkdir()

    # Should be writable
    assert path_is_writable(test_dir) is True


@pytest.mark.unit
def test_path_is_writable_for_nonexistent_path(tmp_path):
    """Test path_is_writable for nonexistent paths (lines 69-71)."""
    nonexistent = tmp_path / "nonexistent"

    # Should check parent's writability
    assert path_is_writable(nonexistent) is True


@pytest.mark.unit
def test_path_is_writable_for_readonly_parent(tmp_path):
    """Test path_is_writable when parent is read-only (line 71)."""
    import os

    # Create a directory and make it read-only
    readonly_dir = tmp_path / "readonly"
    readonly_dir.mkdir()

    # Make readonly (remove write permission)
    os.chmod(readonly_dir, 0o555)

    try:
        nonexistent = readonly_dir / "test"
        result = path_is_writable(nonexistent)
        # Should be False since parent is read-only
        assert result is False
    finally:
        # Restore write permission for cleanup
        os.chmod(readonly_dir, 0o755)


# Tests for _detect_existing_journal()


@pytest.mark.unit
def test_detect_existing_journal_empty_directory(tmp_path):
    """Test _detect_existing_journal with empty directory."""
    detected = _detect_existing_journal(tmp_path)
    assert detected == {}


@pytest.mark.unit
def test_detect_existing_journal_with_folders(tmp_path):
    """Test _detect_existing_journal detects journal folders."""
    # Create some journal folders
    (tmp_path / "daily").mkdir()
    (tmp_path / "projects").mkdir()
    (tmp_path / "people").mkdir()

    detected = _detect_existing_journal(tmp_path)

    assert "folder_daily" in detected
    assert "folder_projects" in detected
    assert "folder_people" in detected
    assert detected["folder_daily"] is True


@pytest.mark.unit
def test_detect_existing_journal_with_cursor_ide(tmp_path):
    """Test _detect_existing_journal detects Cursor IDE config."""
    cursor_dir = tmp_path / ".cursor" / "rules"
    cursor_dir.mkdir(parents=True)

    detected = _detect_existing_journal(tmp_path)

    assert "ide_cursor" in detected
    assert detected["ide_cursor"] is True


@pytest.mark.unit
def test_detect_existing_journal_with_windsurf_ide(tmp_path):
    """Test _detect_existing_journal detects Windsurf IDE config."""
    windsurf_dir = tmp_path / ".windsurf" / "rules"
    windsurf_dir.mkdir(parents=True)

    detected = _detect_existing_journal(tmp_path)

    assert "ide_windsurf" in detected
    assert detected["ide_windsurf"] is True


@pytest.mark.unit
def test_detect_existing_journal_with_claude_code_ide(tmp_path):
    """Test _detect_existing_journal detects Claude Code IDE config."""
    claude_file = tmp_path / "CLAUDE.md"
    claude_file.write_text("# Claude instructions")

    detected = _detect_existing_journal(tmp_path)

    assert "ide_claude_code" in detected
    assert detected["ide_claude_code"] is True


@pytest.mark.unit
def test_detect_existing_journal_with_system_protection(tmp_path):
    """Test _detect_existing_journal detects Claude Code via SYSTEM-PROTECTION.md."""
    system_file = tmp_path / "SYSTEM-PROTECTION.md"
    system_file.write_text("# System protection")

    detected = _detect_existing_journal(tmp_path)

    assert "ide_claude_code" in detected
    assert detected["ide_claude_code"] is True


@pytest.mark.unit
def test_detect_existing_journal_with_copilot_ide(tmp_path):
    """Test _detect_existing_journal detects Copilot IDE config."""
    copilot_dir = tmp_path / ".github" / "instructions"
    copilot_dir.mkdir(parents=True)

    detected = _detect_existing_journal(tmp_path)

    assert "ide_copilot" in detected
    assert detected["ide_copilot"] is True


@pytest.mark.unit
def test_detect_existing_journal_with_templates(tmp_path):
    """Test _detect_existing_journal detects template files."""
    (tmp_path / "daily-template.md").write_text("# Daily template")
    (tmp_path / "project-template.md").write_text("# Project template")

    detected = _detect_existing_journal(tmp_path)

    assert "templates" in detected
    assert detected["templates"] is True


@pytest.mark.unit
def test_detect_existing_journal_with_customizations(tmp_path):
    """Test _detect_existing_journal detects .ai-instructions directory."""
    customizations_dir = tmp_path / ".ai-instructions"
    customizations_dir.mkdir()

    detected = _detect_existing_journal(tmp_path)

    assert "customizations" in detected
    assert detected["customizations"] is True


@pytest.mark.unit
def test_detect_existing_journal_comprehensive(tmp_path):
    """Test _detect_existing_journal with all types of content."""
    # Create journal folders
    (tmp_path / "daily").mkdir()
    (tmp_path / "projects").mkdir()
    (tmp_path / "people").mkdir()
    (tmp_path / "memories").mkdir()
    (tmp_path / "areas").mkdir()
    (tmp_path / "resources").mkdir()
    (tmp_path / "archive").mkdir()

    # Create IDE configs
    (tmp_path / ".cursor").mkdir()
    (tmp_path / ".windsurf").mkdir()
    (tmp_path / "CLAUDE.md").write_text("# Claude")
    (tmp_path / ".github" / "instructions").mkdir(parents=True)

    # Create templates
    (tmp_path / "daily-template.md").write_text("# Daily")

    # Create customizations
    (tmp_path / ".ai-instructions").mkdir()

    detected = _detect_existing_journal(tmp_path)

    # Should detect all types
    assert len([k for k in detected if k.startswith("folder_")]) == 7
    assert "ide_cursor" in detected
    assert "ide_windsurf" in detected
    assert "ide_claude_code" in detected
    assert "ide_copilot" in detected
    assert "templates" in detected
    assert "customizations" in detected


@pytest.mark.unit
def test_detect_existing_journal_nonexistent_path():
    """Test _detect_existing_journal with nonexistent path."""
    nonexistent = Path("/nonexistent/path/that/does/not/exist")
    detected = _detect_existing_journal(nonexistent)
    assert detected == {}


@pytest.mark.unit
def test_detect_existing_journal_only_daily_folder(tmp_path):
    """Test _detect_existing_journal with only daily folder."""
    (tmp_path / "daily").mkdir()

    detected = _detect_existing_journal(tmp_path)

    assert len(detected) == 1
    assert "folder_daily" in detected
    assert "folder_projects" not in detected


@pytest.mark.unit
def test_detect_existing_journal_mixed_content(tmp_path):
    """Test _detect_existing_journal with partial content."""
    # Some folders
    (tmp_path / "daily").mkdir()
    (tmp_path / "projects").mkdir()

    # One IDE config
    (tmp_path / ".cursor").mkdir()

    # No templates
    # No customizations

    detected = _detect_existing_journal(tmp_path)

    assert "folder_daily" in detected
    assert "folder_projects" in detected
    assert "ide_cursor" in detected
    assert "templates" not in detected
    assert "customizations" not in detected
    assert "ide_windsurf" not in detected


@pytest.mark.unit
def test_detect_existing_journal_with_random_files(tmp_path):
    """Test _detect_existing_journal ignores random files that aren't journal content."""
    # Create some random files that shouldn't be detected
    (tmp_path / "README.md").write_text("# Readme")
    (tmp_path / "notes.txt").write_text("Random notes")
    (tmp_path / "config.json").write_text("{}")

    detected = _detect_existing_journal(tmp_path)

    # Should not detect these as journal content
    assert detected == {}


@pytest.mark.unit
def test_detect_existing_journal_with_multiple_templates(tmp_path):
    """Test _detect_existing_journal detects multiple templates."""
    (tmp_path / "daily-template.md").write_text("# Daily")
    (tmp_path / "project-template.md").write_text("# Project")
    (tmp_path / "people-template.md").write_text("# People")
    (tmp_path / "memory-template.md").write_text("# Memory")

    detected = _detect_existing_journal(tmp_path)

    # Should detect templates (as a group, not individually)
    assert "templates" in detected
    assert detected["templates"] is True


# Tests for _handle_existing_journal()


@pytest.mark.unit
def test_handle_existing_journal_no_confirm_mode(tmp_path, capsys):
    """Test _handle_existing_journal in no-confirm mode."""
    detected = {"folder_daily": True, "templates": True}

    # Should not raise exception in no-confirm mode
    result = _handle_existing_journal(
        tmp_path, detected, no_confirm=True, location=str(tmp_path), name="test"
    )

    # Should print warning
    captured = capsys.readouterr()
    assert "Running in --no-confirm mode" in captured.out

    # Should return is_reinstall=True
    assert result["is_reinstall"] is True
    assert result["detected_ide"] is None


@pytest.mark.unit
@patch("ai_journal_kit.cli.setup.confirm")
@patch("ai_journal_kit.cli.setup.show_panel")
def test_handle_existing_journal_user_proceeds(mock_show_panel, mock_confirm, tmp_path):
    """Test _handle_existing_journal when user chooses to proceed."""
    detected = {"folder_daily": True, "ide_cursor": True}
    mock_confirm.return_value = True

    # Should not raise exception when user confirms
    result = _handle_existing_journal(
        tmp_path, detected, no_confirm=False, location=str(tmp_path), name="test"
    )

    # Should show panel and ask for confirmation
    assert mock_show_panel.called
    assert mock_confirm.called

    # Should return detected IDE
    assert result["detected_ide"] == "cursor"
    assert result["is_reinstall"] is True


@pytest.mark.unit
@patch("ai_journal_kit.cli.setup.confirm")
@patch("ai_journal_kit.cli.setup.show_panel")
def test_handle_existing_journal_user_cancels(mock_show_panel, mock_confirm, tmp_path):
    """Test _handle_existing_journal when user cancels."""
    detected = {"folder_daily": True}
    mock_confirm.return_value = False

    # Should raise typer.Exit when user cancels
    with pytest.raises(typer.Exit) as exc_info:
        _handle_existing_journal(
            tmp_path, detected, no_confirm=False, location=str(tmp_path), name="test"
        )

    assert exc_info.value.exit_code == 0
    assert mock_show_panel.called
    assert mock_confirm.called


@pytest.mark.unit
@patch("ai_journal_kit.cli.setup.show_panel")
def test_handle_existing_journal_message_content(mock_show_panel, tmp_path):
    """Test _handle_existing_journal displays correct message content."""
    detected = {
        "folder_daily": True,
        "folder_projects": True,
        "ide_cursor": True,
        "templates": True,
        "customizations": True,
    }

    result = _handle_existing_journal(
        tmp_path, detected, no_confirm=True, location=str(tmp_path), name="test"
    )

    # Verify panel was called with expected content
    assert mock_show_panel.called
    call_args = mock_show_panel.call_args

    # Check kwargs for title (show_panel signature changed)
    assert "title" in call_args.kwargs
    assert call_args.kwargs["title"] == "Existing Journal"

    # Get the message (first positional arg)
    message = call_args[0][0]

    assert "2 journal folder(s)" in message
    assert "cursor" in message
    assert "template files" in message
    assert "user customizations (.ai-instructions/)" in message
    assert "What will happen if you proceed:" in message
    assert "Journal folders will be preserved" in message

    # Verify return value
    assert result["detected_ide"] == "cursor"
    assert result["is_reinstall"] is True


@pytest.mark.unit
@patch("ai_journal_kit.cli.setup.show_panel")
def test_handle_existing_journal_with_all_ide_configs(mock_show_panel, tmp_path):
    """Test _handle_existing_journal detects all IDE configs."""
    detected = {
        "ide_cursor": True,
        "ide_windsurf": True,
        "ide_claude_code": True,
        "ide_copilot": True,
    }

    result = _handle_existing_journal(
        tmp_path, detected, no_confirm=True, location=str(tmp_path), name="test"
    )

    # Verify all IDEs are mentioned
    call_args = mock_show_panel.call_args
    message = call_args[0][0]

    assert "cursor" in message
    assert "windsurf" in message
    assert "claude code" in message
    assert "copilot" in message

    # First detected IDE should be returned (cursor in priority order)
    assert result["detected_ide"] == "cursor"


@pytest.mark.unit
@patch("ai_journal_kit.cli.setup.show_panel")
def test_handle_existing_journal_with_customizations_note(mock_show_panel, tmp_path):
    """Test _handle_existing_journal shows note about customizations."""
    detected = {"customizations": True}

    result = _handle_existing_journal(
        tmp_path, detected, no_confirm=True, location=str(tmp_path), name="test"
    )

    # Verify customization note is included
    call_args = mock_show_panel.call_args
    message = call_args[0][0]

    assert ".ai-instructions/ customizations will be preserved" in message
    assert result["is_reinstall"] is True


@pytest.mark.unit
@patch("ai_journal_kit.cli.setup.confirm")
@patch("ai_journal_kit.cli.setup.show_panel")
@patch("ai_journal_kit.cli.setup.console")
def test_handle_existing_journal_cancel_guidance(
    mock_console, mock_show_panel, mock_confirm, tmp_path
):
    """Test _handle_existing_journal provides guidance when user cancels."""
    detected = {"folder_daily": True}
    mock_confirm.return_value = False

    with pytest.raises(typer.Exit):
        _handle_existing_journal(
            tmp_path, detected, no_confirm=False, location=str(tmp_path), name="myjournal"
        )

    # Verify guidance message was printed
    assert mock_console.print.called
    print_calls = [str(call) for call in mock_console.print.call_args_list]
    message = "".join(print_calls)

    assert "Setup cancelled" in message
    assert "To create a new journal:" in message
    assert "ai-journal-kit setup --location" in message
    assert "myjournal-new" in message


@pytest.mark.unit
@patch("ai_journal_kit.cli.setup.show_panel")
def test_handle_existing_journal_formats_ide_names_correctly(mock_show_panel, tmp_path):
    """Test _handle_existing_journal formats IDE names correctly."""
    detected = {"ide_claude_code": True}

    result = _handle_existing_journal(
        tmp_path, detected, no_confirm=True, location=str(tmp_path), name="test"
    )

    # Verify IDE name is formatted (underscores replaced with spaces)
    call_args = mock_show_panel.call_args
    message = call_args[0][0]

    assert "claude code" in message  # Should replace underscores with spaces
    assert result["detected_ide"] == "claude-code"
