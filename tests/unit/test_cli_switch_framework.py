"""
Unit tests for switch-framework command.

Tests framework switching workflow including:
- Customization detection
- Interactive checklist display
- Customization resolution options
- Template backup and replacement
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from ai_journal_kit.cli.switch_framework import (
    ask_customization_resolution,
    execute_framework_switch,
    show_interactive_checklist,
    switch_framework,
)
from ai_journal_kit.core.manifest import Manifest


@pytest.mark.unit
def test_switch_framework_not_set_up():
    """Test switch-framework fails when journal not set up."""
    with patch("ai_journal_kit.cli.switch_framework.load_config", return_value=None):
        with patch("ai_journal_kit.cli.switch_framework.show_error"):
            with pytest.raises(typer.Exit) as exc_info:
                switch_framework("gtd")

    assert exc_info.value.exit_code == 1


@pytest.mark.unit
def test_switch_framework_same_framework(temp_journal_dir):
    """Test switch-framework handles switching to same framework."""
    # Mock config with GTD framework
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir
    mock_config.framework = "gtd"

    with patch("ai_journal_kit.cli.switch_framework.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.switch_framework.ensure_manifest_exists"):
            with patch("ai_journal_kit.cli.switch_framework.console"):
                with pytest.raises(typer.Exit) as exc_info:
                    switch_framework("gtd", no_confirm=True)

    assert exc_info.value.exit_code == 0


@pytest.mark.unit
def test_switch_framework_invalid_framework(temp_journal_dir):
    """Test switch-framework fails with invalid framework."""
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir
    mock_config.framework = "default"

    with patch("ai_journal_kit.cli.switch_framework.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.switch_framework.ensure_manifest_exists"):
            with patch("ai_journal_kit.cli.switch_framework.show_error"):
                with pytest.raises(typer.Exit) as exc_info:
                    switch_framework("invalid-framework", no_confirm=True)

    assert exc_info.value.exit_code == 1


@pytest.mark.unit
def test_show_interactive_checklist_no_customizations(capsys):
    """Test show_interactive_checklist with no customizations."""
    from io import StringIO

    from rich.console import Console

    # Create a console that writes to string buffer
    string_buffer = StringIO()
    test_console = Console(file=string_buffer, force_terminal=True)

    with patch("ai_journal_kit.cli.switch_framework.console", test_console):
        show_interactive_checklist(
            framework="gtd", framework_name="GTD (Getting Things Done)", customized_count=0
        )

    output = string_buffer.getvalue()
    assert "what will happen" in output.lower()
    assert "what will not happen" in output.lower()
    assert "gtd" in output.lower()


@pytest.mark.unit
def test_show_interactive_checklist_with_customizations(capsys):
    """Test show_interactive_checklist with customizations."""
    from io import StringIO

    from rich.console import Console

    string_buffer = StringIO()
    test_console = Console(file=string_buffer, force_terminal=True)

    with patch("ai_journal_kit.cli.switch_framework.console", test_console):
        show_interactive_checklist(framework="para", framework_name="PARA", customized_count=3)

    output = string_buffer.getvalue()
    assert "3 customized" in output.lower()
    assert "choose what to do" in output.lower() or "detected" in output.lower()


@pytest.mark.unit
def test_ask_customization_resolution_move(monkeypatch):
    """Test ask_customization_resolution returns 'move' action."""
    test_templates = [Path("/test/daily-template.md"), Path("/test/project-template.md")]

    # Mock questionary.select to return 'move'
    mock_select = MagicMock()
    mock_select.ask.return_value = "move"

    with patch("ai_journal_kit.cli.switch_framework.questionary.select", return_value=mock_select):
        with patch("ai_journal_kit.cli.switch_framework.console"):
            result = ask_customization_resolution(test_templates, "GTD")

    assert result == "move"


@pytest.mark.unit
def test_ask_customization_resolution_replace(monkeypatch):
    """Test ask_customization_resolution returns 'replace' action."""
    test_templates = [Path("/test/daily-template.md")]

    mock_select = MagicMock()
    mock_select.ask.return_value = "replace"

    with patch("ai_journal_kit.cli.switch_framework.questionary.select", return_value=mock_select):
        with patch("ai_journal_kit.cli.switch_framework.console"):
            result = ask_customization_resolution(test_templates, "PARA")

    assert result == "replace"


@pytest.mark.unit
def test_ask_customization_resolution_cancel(monkeypatch):
    """Test ask_customization_resolution returns 'cancel' action."""
    test_templates = [Path("/test/daily-template.md")]

    mock_select = MagicMock()
    mock_select.ask.return_value = None  # User cancelled

    with patch("ai_journal_kit.cli.switch_framework.questionary.select", return_value=mock_select):
        with patch("ai_journal_kit.cli.switch_framework.console"):
            result = ask_customization_resolution(test_templates, "GTD")

    assert result == "cancel"


@pytest.mark.unit
def test_execute_framework_switch_replace_action(tmp_path):
    """Test execute_framework_switch with 'replace' action."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()

    # Create existing templates
    old_template = journal_path / "daily-template.md"
    old_template.write_text("# Old Daily Template")

    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()

    manifest = Manifest()
    manifest.add_file(old_template, source="framework:default")

    with patch("ai_journal_kit.cli.switch_framework.copy_framework_templates"):
        with patch("ai_journal_kit.cli.switch_framework.console"):
            execute_framework_switch(
                journal_path=journal_path,
                framework="gtd",
                action="replace",
                customized_templates=[],
                backup_dir=backup_dir,
                manifest=manifest,
            )

    # Old template should be backed up
    backup_file = backup_dir / "daily-template.md"
    assert backup_file.exists()


@pytest.mark.unit
def test_execute_framework_switch_move_action(tmp_path):
    """Test execute_framework_switch with 'move' action for customized templates."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()

    # Create customized template
    custom_template = journal_path / "daily-template.md"
    custom_template.write_text("# My Custom Daily Template")

    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()

    manifest = Manifest()
    manifest.add_file(custom_template, source="framework:default")

    with patch("ai_journal_kit.cli.switch_framework.copy_framework_templates"):
        with patch("ai_journal_kit.cli.switch_framework.console"):
            execute_framework_switch(
                journal_path=journal_path,
                framework="gtd",
                action="move",
                customized_templates=[custom_template],
                backup_dir=backup_dir,
                manifest=manifest,
            )

    # Custom template should be moved to safe zone
    safe_zone = journal_path / ".ai-instructions" / "templates" / "daily-template.md"
    assert safe_zone.exists()
    assert safe_zone.read_text() == "# My Custom Daily Template"


@pytest.mark.unit
def test_execute_framework_switch_no_templates(tmp_path):
    """Test execute_framework_switch with no existing templates."""
    journal_path = tmp_path / "journal"
    journal_path.mkdir()

    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()

    manifest = Manifest()

    with patch("ai_journal_kit.cli.switch_framework.copy_framework_templates"):
        with patch("ai_journal_kit.cli.switch_framework.console"):
            execute_framework_switch(
                journal_path=journal_path,
                framework="gtd",
                action="replace",
                customized_templates=[],
                backup_dir=backup_dir,
                manifest=manifest,
            )

    # Should complete without errors
    assert True
