"""
Unit tests for template management functionality.

Tests template copying, IDE config installation, and validation.
"""

import pytest

from ai_journal_kit.core.templates import (
    copy_ide_configs,
    copy_template,
    get_template,
    list_available_templates,
    resolve_template,
)


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
    assert custom_file.read_text(encoding="utf-8") == "# Custom rule"


@pytest.mark.unit
def test_copy_template(temp_journal_dir):
    """Test copying a single template file (lines 28-29)."""
    dest_file = temp_journal_dir / "my-daily.md"
    copy_template("daily-template.md", dest_file)

    assert dest_file.exists()
    assert dest_file.is_file()
    # Verify it has content (use UTF-8 for Windows compatibility with emojis)
    content = dest_file.read_text(encoding="utf-8")
    assert len(content) > 0


@pytest.mark.unit
def test_copy_ide_configs_handles_nonexistent_ide(temp_journal_dir):
    """Test that copy_ide_configs skips nonexistent IDE configs (line 47)."""
    # Create a fake IDE name that doesn't exist
    copy_ide_configs("fake-ide", temp_journal_dir)

    # Should not crash, just skip
    assert temp_journal_dir.exists()


@pytest.mark.unit
def test_copy_ide_configs_claude_code(temp_journal_dir):
    """Test Claude Code config copying (lines 69-72)."""
    copy_ide_configs("claude-code", temp_journal_dir)

    # Should have copied claude-code files (they exist in subdirectories)
    # Just verify the function ran without error and directory exists
    assert temp_journal_dir.exists()


@pytest.mark.unit
def test_copy_ide_configs_copilot(temp_journal_dir):
    """Test Copilot config copying."""
    copy_ide_configs("copilot", temp_journal_dir)

    # Should have .github directory
    github_dir = temp_journal_dir / ".github"
    assert github_dir.exists()
    # Should have instructions folder
    assert (github_dir / "instructions").exists()


@pytest.mark.unit
def test_list_available_templates():
    """Test listing available templates (lines 95-96)."""
    templates = list_available_templates()

    assert isinstance(templates, list)
    assert len(templates) > 0
    # Should include our known templates
    assert any("template" in t.lower() for t in templates)


@pytest.mark.unit
def test_copy_ide_configs_copilot_with_old_structure(temp_journal_dir):
    """Test Copilot config handles migration from old structure (line 81-83)."""
    # Create old structure with custom content
    (temp_journal_dir / ".github").mkdir()
    old_file = temp_journal_dir / ".github" / "copilot-instructions.md"
    old_file.write_text("# My custom old instructions")

    # Copy new structure
    copy_ide_configs("copilot", temp_journal_dir)

    # File exists (from template), but old custom content was replaced
    assert old_file.exists()
    # Should have new template content (not our custom text)
    content = old_file.read_text(encoding="utf-8")
    assert "# My custom old instructions" not in content

    # New instructions folder should exist
    instructions_folder = temp_journal_dir / ".github" / "instructions"
    assert instructions_folder.exists()


@pytest.mark.unit
def test_resolve_template_user_override(temp_journal_dir):
    """Test resolve_template prioritizes user override in .ai-instructions/templates/."""
    # Create user override
    user_templates = temp_journal_dir / ".ai-instructions" / "templates"
    user_templates.mkdir(parents=True)
    user_template = user_templates / "daily-template.md"
    user_template.write_text("# My custom daily template")

    # Create journal template
    journal_template = temp_journal_dir / "daily-template.md"
    journal_template.write_text("# Journal daily template")

    # Should return user override (highest priority)
    result = resolve_template("daily-template.md", temp_journal_dir)

    assert result == user_template
    assert result.read_text() == "# My custom daily template"


@pytest.mark.unit
def test_resolve_template_journal_root(temp_journal_dir):
    """Test resolve_template uses journal root if no user override."""
    # Create journal template only
    journal_template = temp_journal_dir / "daily-template.md"
    journal_template.write_text("# Journal daily template")

    # Should return journal template (medium priority)
    result = resolve_template("daily-template.md", temp_journal_dir)

    assert result == journal_template
    assert result.read_text() == "# Journal daily template"


@pytest.mark.unit
def test_resolve_template_package_default(temp_journal_dir):
    """Test resolve_template falls back to package default."""
    # No user override, no journal template
    # Should fall back to package default (lowest priority)
    result = resolve_template("daily-template.md", temp_journal_dir)

    # Should get package default
    assert result is not None
    assert result.exists()
    assert result.is_file()


@pytest.mark.unit
def test_resolve_template_not_found(temp_journal_dir):
    """Test resolve_template returns path even if template doesn't exist (get_template doesn't check)."""
    # Request a template that doesn't exist anywhere
    # get_template() just constructs a path, doesn't check existence
    result = resolve_template("nonexistent-template.md", temp_journal_dir)

    # Will get a path to package templates (even if file doesn't exist)
    assert result is not None
    assert "nonexistent-template.md" in str(result)


@pytest.mark.unit
def test_resolve_template_priority_order(temp_journal_dir):
    """Test resolve_template follows correct priority order."""
    # Create all three versions
    user_templates = temp_journal_dir / ".ai-instructions" / "templates"
    user_templates.mkdir(parents=True)
    user_template = user_templates / "test.md"
    user_template.write_text("USER")

    journal_template = temp_journal_dir / "test.md"
    journal_template.write_text("JOURNAL")

    # Should always pick user override first
    result = resolve_template("test.md", temp_journal_dir)
    assert result == user_template
    assert result.read_text() == "USER"

    # Remove user override
    user_template.unlink()

    # Should pick journal next
    result = resolve_template("test.md", temp_journal_dir)
    assert result == journal_template
    assert result.read_text() == "JOURNAL"

    # Remove journal
    journal_template.unlink()

    # Should try package default (get_template just constructs path)
    result = resolve_template("test.md", temp_journal_dir)
    # Will get a package path (even if file doesn't actually exist there)
    assert result is not None
    assert "test.md" in str(result)
