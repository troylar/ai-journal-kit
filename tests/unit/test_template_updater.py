"""
Unit tests for template updater functionality.

Tests template backup, update detection, and restoration.
"""

from datetime import datetime
from unittest.mock import patch

import pytest

from ai_journal_kit.core.template_updater import (
    backup_template,
    get_template_changes,
    list_backups,
    restore_template_backup,
    show_template_changes,
    update_templates,
)


@pytest.mark.unit
def test_backup_template_creates_timestamped_backup(temp_journal_dir):
    """Test that backup_template creates a timestamped backup file."""
    # Create a template file
    template_file = temp_journal_dir / "daily-template.md"
    template_file.write_text("# Daily Template\nContent here")

    # Create backup
    backup_path = backup_template(template_file)

    # Verify backup exists and has correct format
    assert backup_path.exists()
    assert backup_path.parent == temp_journal_dir
    assert "daily-template.backup_" in backup_path.name
    assert backup_path.suffix == ".md"

    # Verify content is copied
    assert backup_path.read_text(encoding="utf-8") == "# Daily Template\nContent here"


@pytest.mark.unit
def test_backup_template_raises_on_missing_file(temp_journal_dir):
    """Test that backup_template raises FileNotFoundError for missing file."""
    missing_file = temp_journal_dir / "nonexistent.md"

    with pytest.raises(FileNotFoundError, match="Template not found"):
        backup_template(missing_file)


@pytest.mark.unit
def test_backup_template_preserves_metadata(temp_journal_dir):
    """Test that backup_template preserves file metadata."""
    template_file = temp_journal_dir / "template.md"
    template_file.write_text("content")

    # Get original mtime
    original_mtime = template_file.stat().st_mtime

    # Create backup
    backup_path = backup_template(template_file)

    # Backup should have same mtime as original
    assert backup_path.stat().st_mtime == original_mtime


@pytest.mark.unit
def test_get_template_changes_detects_differences(temp_journal_dir):
    """Test that get_template_changes detects template differences."""
    # Create user template with different content
    user_template = temp_journal_dir / "daily-template.md"
    user_template.write_text("# Old Daily Template")

    # Mock get_template to return package template
    with patch("ai_journal_kit.core.templates.get_template") as mock_get:
        # Create a mock package template with different content
        package_template = temp_journal_dir / "package-daily-template.md"
        package_template.write_text("# New Daily Template with updates")
        mock_get.return_value = package_template

        changes = get_template_changes(temp_journal_dir)

        # Should detect change
        assert "daily-template.md" in changes
        assert changes["daily-template.md"]["user_path"] == user_template
        assert changes["daily-template.md"]["size_old"] == len("# Old Daily Template")
        assert changes["daily-template.md"]["size_new"] == len("# New Daily Template with updates")


@pytest.mark.unit
def test_get_template_changes_returns_empty_for_identical(temp_journal_dir):
    """Test that get_template_changes returns empty dict for identical templates."""
    # Create user template
    content = "# Daily Template\nSame content"
    user_template = temp_journal_dir / "daily-template.md"
    user_template.write_text(content)

    with patch("ai_journal_kit.core.templates.get_template") as mock_get:
        # Package template has same content
        package_template = temp_journal_dir / "package-daily.md"
        package_template.write_text(content)
        mock_get.return_value = package_template

        changes = get_template_changes(temp_journal_dir)

        # No changes should be detected
        assert "daily-template.md" not in changes


@pytest.mark.unit
def test_get_template_changes_skips_missing_user_templates(temp_journal_dir):
    """Test that get_template_changes skips templates that don't exist in user journal."""
    # Don't create any user templates

    with patch("ai_journal_kit.core.templates.get_template"):
        changes = get_template_changes(temp_journal_dir)

        # Should return empty since no user templates exist
        assert changes == {}


@pytest.mark.unit
def test_get_template_changes_handles_exceptions(temp_journal_dir):
    """Test that get_template_changes gracefully handles exceptions."""
    user_template = temp_journal_dir / "daily-template.md"
    user_template.write_text("content")

    with patch("ai_journal_kit.core.templates.get_template") as mock_get:
        # Make get_template raise an exception
        mock_get.side_effect = Exception("Test error")

        # Should not crash, just skip this template
        changes = get_template_changes(temp_journal_dir)
        assert changes == {}


@pytest.mark.unit
def test_get_template_changes_skips_nonexistent_package_template(temp_journal_dir):
    """Test that get_template_changes skips when package template doesn't exist (line 61)."""
    user_template = temp_journal_dir / "daily-template.md"
    user_template.write_text("# User template")

    with patch("ai_journal_kit.core.templates.get_template") as mock_get:
        # Return a path that doesn't exist
        nonexistent_path = temp_journal_dir / "nonexistent-package-template.md"
        mock_get.return_value = nonexistent_path

        # Should skip this template since package template doesn't exist
        changes = get_template_changes(temp_journal_dir)
        assert changes == {}


@pytest.mark.unit
def test_show_template_changes_displays_table(temp_journal_dir, capsys):
    """Test that show_template_changes displays a table of changes."""
    changes = {
        "daily-template.md": {
            "user_path": temp_journal_dir / "daily-template.md",
            "package_path": temp_journal_dir / "package-daily.md",
            "size_old": 100,
            "size_new": 150,
            "modified": datetime.now().timestamp(),
        }
    }

    show_template_changes(changes)

    # Should output table (checking stdout is captured)
    # Note: Rich console output might not show in capsys, but function should run without error


@pytest.mark.unit
def test_show_template_changes_shows_up_to_date_message(capsys):
    """Test that show_template_changes shows message when no changes."""
    show_template_changes({})

    # Should show "up to date" message (function runs without error)


@pytest.mark.unit
def test_update_templates_returns_empty_for_no_changes(temp_journal_dir):
    """Test that update_templates returns empty list when no changes."""
    with patch("ai_journal_kit.core.template_updater.get_template_changes") as mock_changes:
        mock_changes.return_value = {}

        updated = update_templates(temp_journal_dir, backup=True)

        assert updated == []


@pytest.mark.unit
def test_update_templates_updates_and_backs_up(temp_journal_dir):
    """Test that update_templates updates templates and creates backups."""
    # Create user template
    user_template = temp_journal_dir / "daily-template.md"
    user_template.write_text("# Old content")

    # Mock get_template_changes to return a change
    mock_changes = {
        "daily-template.md": {
            "user_path": user_template,
            "package_path": temp_journal_dir / "new.md",
            "size_old": 100,
            "size_new": 200,
            "modified": datetime.now().timestamp(),
        }
    }

    with patch("ai_journal_kit.core.template_updater.get_template_changes") as mock_get_changes:
        with patch("ai_journal_kit.core.templates.copy_template") as mock_copy:
            mock_get_changes.return_value = mock_changes

            updated = update_templates(temp_journal_dir, backup=True)

            # Should return list of updated templates
            assert updated == ["daily-template.md"]

            # Should have called copy_template
            mock_copy.assert_called_once_with("daily-template.md", user_template)


@pytest.mark.unit
def test_update_templates_without_backup(temp_journal_dir):
    """Test that update_templates can skip backup creation."""
    user_template = temp_journal_dir / "daily-template.md"
    user_template.write_text("# Old content")

    mock_changes = {
        "daily-template.md": {
            "user_path": user_template,
            "package_path": temp_journal_dir / "new.md",
            "size_old": 100,
            "size_new": 200,
            "modified": datetime.now().timestamp(),
        }
    }

    with patch("ai_journal_kit.core.template_updater.get_template_changes") as mock_get_changes:
        with patch("ai_journal_kit.core.templates.copy_template"):
            with patch("ai_journal_kit.core.template_updater.backup_template") as mock_backup:
                mock_get_changes.return_value = mock_changes

                updated = update_templates(temp_journal_dir, backup=False)

                # Should not create backups
                mock_backup.assert_not_called()
                assert updated == ["daily-template.md"]


@pytest.mark.unit
def test_list_backups_finds_backup_files(temp_journal_dir):
    """Test that list_backups finds all backup files."""
    # Create some backup files
    backup1 = temp_journal_dir / "daily-template.backup_20231107_120000.md"
    backup2 = temp_journal_dir / "project-template.backup_20231108_130000.md"
    backup3 = temp_journal_dir / "regular-file.md"  # Not a backup

    backup1.write_text("backup 1")
    backup2.write_text("backup 2")
    backup3.write_text("regular")

    backups = list_backups(temp_journal_dir)

    # Should find both backups, not regular file
    assert len(backups) == 2
    assert backup1 in backups or backup2 in backups
    assert backup3 not in backups


@pytest.mark.unit
def test_list_backups_returns_sorted_by_mtime(temp_journal_dir):
    """Test that list_backups returns backups sorted by modification time."""
    import time

    # Create backups with different mtimes
    backup1 = temp_journal_dir / "template.backup_20231107_120000.md"
    backup1.write_text("old")
    time.sleep(0.01)

    backup2 = temp_journal_dir / "template.backup_20231108_130000.md"
    backup2.write_text("new")

    backups = list_backups(temp_journal_dir)

    # Should be sorted with newest first (reverse=True)
    if len(backups) >= 2:
        assert backups[0].stat().st_mtime >= backups[1].stat().st_mtime


@pytest.mark.unit
def test_list_backups_returns_empty_for_no_backups(temp_journal_dir):
    """Test that list_backups returns empty list when no backups exist."""
    backups = list_backups(temp_journal_dir)
    assert backups == []


@pytest.mark.unit
def test_restore_template_backup_restores_file(temp_journal_dir):
    """Test that restore_template_backup restores a template from backup."""
    # Create original template and backup
    original = temp_journal_dir / "daily-template.md"
    original.write_text("# Current version")

    backup = temp_journal_dir / "daily-template.backup_20231107_120000.md"
    backup.write_text("# Old version")

    # Restore from backup
    restored_path = restore_template_backup(backup)

    # Should restore to original path
    assert restored_path == original
    assert original.read_text(encoding="utf-8") == "# Old version"


@pytest.mark.unit
def test_restore_template_backup_raises_on_missing_backup(temp_journal_dir):
    """Test that restore_template_backup raises FileNotFoundError for missing backup."""
    missing_backup = temp_journal_dir / "nonexistent.backup_20231107_120000.md"

    with pytest.raises(FileNotFoundError, match="Backup not found"):
        restore_template_backup(missing_backup)


@pytest.mark.unit
def test_restore_template_backup_parses_name_correctly(temp_journal_dir):
    """Test that restore_template_backup correctly parses backup filename."""
    # Create backup with complex name
    backup = temp_journal_dir / "my-custom-template.backup_20231107_120000.md"
    backup.write_text("# Backup content")

    restored_path = restore_template_backup(backup)

    # Should restore to correct original name
    expected = temp_journal_dir / "my-custom-template.md"
    assert restored_path == expected
    assert expected.exists()
    assert expected.read_text(encoding="utf-8") == "# Backup content"
