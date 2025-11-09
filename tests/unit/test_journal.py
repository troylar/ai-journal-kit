"""
Unit tests for journal structure management.

Tests journal creation, validation, and statistics.
"""

import pytest

from ai_journal_kit.core.journal import (
    REQUIRED_FOLDERS,
    create_structure,
    get_folder_stats,
    validate_structure,
)


@pytest.mark.unit
def test_create_structure_creates_all_folders(temp_journal_dir):
    """Test that create_structure creates all required folders."""
    create_structure(temp_journal_dir)

    # Check all required folders exist
    for folder in REQUIRED_FOLDERS:
        assert (temp_journal_dir / folder).exists()

    # Check .ai-instructions folder
    assert (temp_journal_dir / ".ai-instructions").exists()

    # Check WELCOME.md
    assert (temp_journal_dir / "WELCOME.md").exists()


@pytest.mark.unit
def test_validate_structure_returns_true_for_complete(temp_journal_dir):
    """Test validate_structure returns True when all folders exist."""
    create_structure(temp_journal_dir)

    is_valid, missing = validate_structure(temp_journal_dir)

    assert is_valid is True
    assert missing == []


@pytest.mark.unit
def test_validate_structure_handles_nonexistent_path(tmp_path):
    """Test validate_structure handles nonexistent journal path (lines 46-47)."""
    nonexistent = tmp_path / "nonexistent"

    is_valid, missing = validate_structure(nonexistent)

    assert is_valid is False
    assert set(missing) == set(REQUIRED_FOLDERS)


@pytest.mark.unit
def test_validate_structure_detects_missing_folders(temp_journal_dir):
    """Test validate_structure detects missing folders (lines 49-55)."""
    # Create only some folders
    temp_journal_dir.mkdir(exist_ok=True)
    (temp_journal_dir / "daily").mkdir()
    (temp_journal_dir / "projects").mkdir()
    # Leave others missing

    is_valid, missing = validate_structure(temp_journal_dir)

    assert is_valid is False
    assert "areas" in missing
    assert "resources" in missing
    assert "people" in missing
    assert "daily" not in missing  # Should not be in missing


@pytest.mark.unit
def test_get_folder_stats_counts_files(temp_journal_dir):
    """Test get_folder_stats counts markdown files (lines 67-75)."""
    create_structure(temp_journal_dir)

    # Add some markdown files
    (temp_journal_dir / "daily" / "2025-01-01.md").write_text("# Day 1")
    (temp_journal_dir / "daily" / "2025-01-02.md").write_text("# Day 2")
    (temp_journal_dir / "projects" / "project1.md").write_text("# Project 1")

    stats = get_folder_stats(temp_journal_dir)

    assert stats["daily"] == 2
    assert stats["projects"] == 1
    assert stats["areas"] == 0  # No files


@pytest.mark.unit
def test_get_folder_stats_handles_missing_folders(temp_journal_dir):
    """Test get_folder_stats handles missing folders (line 74)."""
    temp_journal_dir.mkdir(exist_ok=True)
    # Don't create any folders

    stats = get_folder_stats(temp_journal_dir)

    # All counts should be 0
    for folder in REQUIRED_FOLDERS:
        assert stats[folder] == 0


@pytest.mark.unit
def test_get_folder_stats_ignores_non_markdown(temp_journal_dir):
    """Test get_folder_stats only counts .md files (line 72)."""
    create_structure(temp_journal_dir)

    # Add markdown and non-markdown files
    (temp_journal_dir / "daily" / "note.md").write_text("# Note")
    (temp_journal_dir / "daily" / "data.txt").write_text("text")
    (temp_journal_dir / "daily" / "image.png").write_text("fake png")

    stats = get_folder_stats(temp_journal_dir)

    # Should only count .md file
    assert stats["daily"] == 1


@pytest.mark.unit
def test_create_structure_is_idempotent(temp_journal_dir):
    """Test that create_structure can be called multiple times safely."""
    # Create structure twice
    create_structure(temp_journal_dir)
    create_structure(temp_journal_dir)

    # Should still have all folders
    for folder in REQUIRED_FOLDERS:
        assert (temp_journal_dir / folder).exists()

    # WELCOME.md should exist (not duplicated)
    assert (temp_journal_dir / "WELCOME.md").exists()


@pytest.mark.unit
def test_create_structure_with_default_framework(temp_journal_dir):
    """Test create_structure with default framework."""
    create_structure(temp_journal_dir, framework="default")

    # Should create standard structure
    for folder in REQUIRED_FOLDERS:
        assert (temp_journal_dir / folder).exists()

    # Should have WELCOME.md but no framework-specific templates
    assert (temp_journal_dir / "WELCOME.md").exists()


@pytest.mark.unit
def test_create_structure_with_gtd_framework(temp_journal_dir):
    """Test create_structure with GTD framework copies templates."""
    create_structure(temp_journal_dir, framework="gtd")

    # Should create standard structure
    for folder in REQUIRED_FOLDERS:
        assert (temp_journal_dir / folder).exists()

    # Should have GTD templates
    assert (temp_journal_dir / "daily-template.md").exists()
    assert (temp_journal_dir / "project-template.md").exists()
    assert (temp_journal_dir / "someday-maybe-template.md").exists()
    assert (temp_journal_dir / "waiting-for-template.md").exists()
