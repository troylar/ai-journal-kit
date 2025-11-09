"""
Unit tests for customize-template command.

Tests template customization workflow including:
- Template name normalization
- Template resolution
- Safe zone copying
- Error handling
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from ai_journal_kit.cli.customize_template import customize_template


@pytest.mark.unit
def test_customize_template_not_set_up():
    """Test customize-template fails when journal not set up."""
    with patch("ai_journal_kit.cli.customize_template.load_config", return_value=None):
        with patch("ai_journal_kit.cli.customize_template.show_error"):
            with pytest.raises(typer.Exit) as exc_info:
                customize_template("daily-template.md")

    assert exc_info.value.exit_code == 1


@pytest.mark.unit
def test_customize_template_normalizes_name_add_md(temp_journal_dir):
    """Test customize-template adds .md extension if missing."""
    # Create source template
    source_template = temp_journal_dir / "daily-template.md"
    source_template.write_text("# Daily Template")

    # Mock config
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.customize_template.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.customize_template.ensure_manifest_exists"):
            with patch(
                "ai_journal_kit.cli.customize_template.resolve_template",
                return_value=source_template,
            ):
                with patch("ai_journal_kit.cli.customize_template.show_success"):
                    with patch("ai_journal_kit.cli.customize_template.console"):
                        customize_template("daily-template")  # No .md

    # Should create customized template
    custom_template = temp_journal_dir / ".ai-instructions" / "templates" / "daily-template.md"
    assert custom_template.exists()


@pytest.mark.unit
def test_customize_template_normalizes_name_add_template(temp_journal_dir):
    """Test customize-template adds -template suffix if missing."""
    # Create source template
    source_template = temp_journal_dir / "daily-template.md"
    source_template.write_text("# Daily Template")

    # Mock config
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.customize_template.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.customize_template.ensure_manifest_exists"):
            with patch(
                "ai_journal_kit.cli.customize_template.resolve_template",
                return_value=source_template,
            ):
                with patch("ai_journal_kit.cli.customize_template.show_success"):
                    with patch("ai_journal_kit.cli.customize_template.console"):
                        customize_template("daily.md")  # No -template

    # Should create customized template with normalized name
    custom_template = temp_journal_dir / ".ai-instructions" / "templates" / "daily-template.md"
    assert custom_template.exists()


@pytest.mark.unit
def test_customize_template_template_not_found(temp_journal_dir):
    """Test customize-template fails when template doesn't exist."""
    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.customize_template.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.customize_template.ensure_manifest_exists"):
            with patch("ai_journal_kit.cli.customize_template.resolve_template", return_value=None):
                with patch("ai_journal_kit.cli.customize_template.show_error"):
                    with pytest.raises(typer.Exit) as exc_info:
                        customize_template("nonexistent-template.md")

    assert exc_info.value.exit_code == 1


@pytest.mark.unit
def test_customize_template_already_customized(temp_journal_dir):
    """Test customize-template handles already customized template."""
    # Create source template
    source_template = temp_journal_dir / "daily-template.md"
    source_template.write_text("# Daily Template")

    # Create already customized template
    custom_dir = temp_journal_dir / ".ai-instructions" / "templates"
    custom_dir.mkdir(parents=True)
    custom_template = custom_dir / "daily-template.md"
    custom_template.write_text("# My Custom Daily Template")

    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.customize_template.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.customize_template.ensure_manifest_exists"):
            with patch(
                "ai_journal_kit.cli.customize_template.resolve_template",
                return_value=source_template,
            ):
                with patch("ai_journal_kit.cli.customize_template.console"):
                    with pytest.raises(typer.Exit) as exc_info:
                        customize_template("daily-template.md")

    # Should exit with success code
    assert exc_info.value.exit_code == 0
    # Original customization should be unchanged
    assert custom_template.read_text() == "# My Custom Daily Template"


@pytest.mark.unit
def test_customize_template_successful_copy(temp_journal_dir):
    """Test successful template customization."""
    # Create source template
    source_template = temp_journal_dir / "daily-template.md"
    source_template.write_text("# Daily Template\n\nOriginal content")

    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.customize_template.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.customize_template.ensure_manifest_exists"):
            with patch(
                "ai_journal_kit.cli.customize_template.resolve_template",
                return_value=source_template,
            ):
                with patch("ai_journal_kit.cli.customize_template.show_success"):
                    with patch("ai_journal_kit.cli.customize_template.console"):
                        customize_template("daily-template.md")

    # Verify template copied
    custom_template = temp_journal_dir / ".ai-instructions" / "templates" / "daily-template.md"
    assert custom_template.exists()
    assert custom_template.read_text() == "# Daily Template\n\nOriginal content"


@pytest.mark.unit
def test_customize_template_creates_directory(temp_journal_dir):
    """Test customize-template creates .ai-instructions/templates/ directory."""
    # Create source template
    source_template = temp_journal_dir / "project-template.md"
    source_template.write_text("# Project Template")

    # Ensure directory doesn't exist
    custom_dir = temp_journal_dir / ".ai-instructions" / "templates"
    assert not custom_dir.exists()

    mock_config = MagicMock()
    mock_config.journal_location = temp_journal_dir

    with patch("ai_journal_kit.cli.customize_template.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.customize_template.ensure_manifest_exists"):
            with patch(
                "ai_journal_kit.cli.customize_template.resolve_template",
                return_value=source_template,
            ):
                with patch("ai_journal_kit.cli.customize_template.show_success"):
                    with patch("ai_journal_kit.cli.customize_template.console"):
                        customize_template("project-template.md")

    # Directory should be created
    assert custom_dir.exists()
    assert (custom_dir / "project-template.md").exists()


@pytest.mark.unit
def test_customize_template_calls_ensure_manifest():
    """Test customize-template calls ensure_manifest_exists."""
    mock_config = MagicMock()
    mock_config.journal_location = Path("/fake/journal")

    with patch("ai_journal_kit.cli.customize_template.load_config", return_value=mock_config):
        with patch("ai_journal_kit.cli.customize_template.ensure_manifest_exists") as mock_ensure:
            with patch("ai_journal_kit.cli.customize_template.resolve_template", return_value=None):
                with patch("ai_journal_kit.cli.customize_template.show_error"):
                    with pytest.raises(typer.Exit):
                        customize_template("daily-template.md")

    # Should have called ensure_manifest_exists
    mock_ensure.assert_called_once()
