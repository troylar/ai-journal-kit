"""
Unit tests for template management functionality.

Tests template copying, IDE config installation, and validation.
"""

import pytest

from ai_journal_kit.core.templates import copy_ide_configs, get_template


@pytest.mark.unit
def test_get_template_returns_valid_path():
    """Test that get_template returns a valid template file."""
    template_path = get_template("daily-template.md")
    assert template_path.exists()
    assert template_path.is_file()


@pytest.mark.unit
def test_copy_ide_configs_creates_cursor_structure(temp_journal_dir):
    """Test that copy_ide_configs creates Cursor IDE structure."""
    copy_ide_configs("cursor", temp_journal_dir)

    cursor_dir = temp_journal_dir / ".cursor"
    assert cursor_dir.exists()
    assert (cursor_dir / "rules").exists()


@pytest.mark.unit
def test_copy_ide_configs_creates_windsurf_structure(temp_journal_dir):
    """Test that copy_ide_configs creates Windsurf IDE structure."""
    copy_ide_configs("windsurf", temp_journal_dir)

    windsurf_dir = temp_journal_dir / ".windsurf"
    assert windsurf_dir.exists()
    assert (windsurf_dir / "rules").exists()


@pytest.mark.unit
def test_copy_ide_configs_handles_all_option(temp_journal_dir):
    """Test that copy_ide_configs handles 'all' option."""
    copy_ide_configs("all", temp_journal_dir)

    # Should create all IDE configs
    assert (temp_journal_dir / ".cursor").exists()
    assert (temp_journal_dir / ".windsurf").exists()
    assert (temp_journal_dir / ".github").exists()


@pytest.mark.unit
def test_copy_ide_configs_skips_existing_files(temp_journal_dir):
    """Test that copy_ide_configs doesn't overwrite existing configs."""
    cursor_dir = temp_journal_dir / ".cursor" / "rules"
    cursor_dir.mkdir(parents=True)
    custom_file = cursor_dir / "custom.mdc"
    custom_file.write_text("# Custom rule")

    copy_ide_configs("cursor", temp_journal_dir)

    # Custom file should still exist
    assert custom_file.exists()
    assert custom_file.read_text() == "# Custom rule"
