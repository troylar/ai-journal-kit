"""Unit tests for file scanner utility.

Tests for FileScanner class.

Issue: #6 - Search & Filter Enhancement
Coverage Target: 100%
"""

import pytest
from datetime import date
from pathlib import Path

from ai_journal_kit.core.file_scanner import FileScanner
from ai_journal_kit.core.search_result import EntryType


@pytest.fixture
def test_journal(tmp_path):
    """Create temporary test journal structure."""
    # Create folder structure
    daily_dir = tmp_path / "daily"
    projects_dir = tmp_path / "projects"
    people_dir = tmp_path / "people"
    memories_dir = tmp_path / "memories"

    daily_dir.mkdir()
    projects_dir.mkdir()
    people_dir.mkdir()
    memories_dir.mkdir()

    # Create sample files
    (daily_dir / "2024-11-01.md").write_text("# Daily Entry\n\nTest content")
    (daily_dir / "2024-11-05.md").write_text("# Daily Entry\n\nAnother entry")
    (daily_dir / "2024-11-10.md").write_text("# Daily Entry\n\nLatest entry")
    (projects_dir / "launch.md").write_text("# Project Launch\n\nProject notes")
    (people_dir / "sarah.md").write_text("# Sarah\n\nPerson notes")
    (memories_dir / "deadline.md").write_text("# Deadline Memory\n\nMemory notes")

    return tmp_path


class TestFileScanner:
    """Tests for FileScanner class (T014)."""

    def test_init_valid_path(self, test_journal):
        """Test initializing scanner with valid path."""
        scanner = FileScanner(test_journal)
        assert scanner.journal_path == test_journal.resolve()

    def test_init_invalid_path_raises_error(self):
        """Test initializing with non-existent path raises error."""
        with pytest.raises(ValueError) as exc_info:
            FileScanner(Path("/nonexistent/path"))

        error_msg = str(exc_info.value)
        assert "does not exist" in error_msg

    def test_init_file_not_directory(self, tmp_path):
        """Test initializing with file (not directory) raises error."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        with pytest.raises(ValueError) as exc_info:
            FileScanner(test_file)

        error_msg = str(exc_info.value)
        assert "not a directory" in error_msg

    def test_scan_all_files(self, test_journal):
        """Test scanning all markdown files."""
        scanner = FileScanner(test_journal)
        files = scanner.scan()
        assert len(files) == 6  # 3 daily + 1 project + 1 people + 1 memory

    def test_scan_with_entry_type_filter(self, test_journal):
        """Test scanning with entry type filter."""
        scanner = FileScanner(test_journal)
        files = scanner.scan(entry_types=[EntryType.DAILY])
        assert len(files) == 3
        assert all("daily" in str(f) for f in files)

    def test_scan_with_multiple_entry_types(self, test_journal):
        """Test scanning with multiple entry types."""
        scanner = FileScanner(test_journal)
        files = scanner.scan(entry_types=[EntryType.DAILY, EntryType.PROJECT])
        assert len(files) == 4  # 3 daily + 1 project

    def test_scan_with_date_filter(self, test_journal):
        """Test scanning with date range filter."""
        scanner = FileScanner(test_journal)
        files = scanner.scan(
            date_after=date(2024, 11, 5),
            date_before=date(2024, 11, 10)
        )
        # Should include 2024-11-05.md and 2024-11-10.md
        assert len(files) >= 2

    def test_scan_with_date_after_only(self, test_journal):
        """Test scanning with only date_after filter."""
        scanner = FileScanner(test_journal)
        files = scanner.scan(date_after=date(2024, 11, 10))
        # Should include only 2024-11-10.md
        dated_files = [f for f in files if "2024" in f.name]
        assert len(dated_files) == 1

    def test_get_entry_type_daily(self, test_journal):
        """Test get_entry_type for daily entry."""
        scanner = FileScanner(test_journal)
        daily_file = test_journal / "daily" / "2024-11-01.md"
        entry_type = scanner.get_entry_type(daily_file)
        assert entry_type == EntryType.DAILY

    def test_get_entry_type_project(self, test_journal):
        """Test get_entry_type for project entry."""
        scanner = FileScanner(test_journal)
        project_file = test_journal / "projects" / "launch.md"
        entry_type = scanner.get_entry_type(project_file)
        assert entry_type == EntryType.PROJECT

    def test_get_entry_type_people(self, test_journal):
        """Test get_entry_type for people entry."""
        scanner = FileScanner(test_journal)
        people_file = test_journal / "people" / "sarah.md"
        entry_type = scanner.get_entry_type(people_file)
        assert entry_type == EntryType.PEOPLE

    def test_get_entry_type_memory(self, test_journal):
        """Test get_entry_type for memory entry."""
        scanner = FileScanner(test_journal)
        memory_file = test_journal / "memories" / "deadline.md"
        entry_type = scanner.get_entry_type(memory_file)
        assert entry_type == EntryType.MEMORY

    def test_get_entry_type_invalid_raises_error(self, test_journal):
        """Test get_entry_type with invalid path raises error."""
        scanner = FileScanner(test_journal)
        invalid_file = test_journal / "unknown" / "file.md"

        with pytest.raises(ValueError) as exc_info:
            scanner.get_entry_type(invalid_file)

        error_msg = str(exc_info.value)
        assert "Unknown entry type" in error_msg or "not in journal" in error_msg


class TestFileScannerIntegration:
    """Integration tests with real file system (T046 - US3)."""

    def test_scan_with_multiple_filters(self, test_journal):
        """Test scanning with combined filters."""
        scanner = FileScanner(test_journal)
        files = scanner.scan(
            entry_types=[EntryType.DAILY],
            date_after=date(2024, 11, 1),
            date_before=date(2024, 11, 5)
        )
        # Should include 2024-11-01.md and 2024-11-05.md
        assert len(files) == 2
        assert all("daily" in str(f) for f in files)
