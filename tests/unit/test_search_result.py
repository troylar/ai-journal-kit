"""Unit tests for search result models.

Tests for EntryType, SearchQuery, SearchResult, and SearchResultSet models.

Issue: #6 - Search & Filter Enhancement
Coverage Target: 100%
"""

from datetime import date
from pathlib import Path

import pytest

from ai_journal_kit.core.search_result import (
    EntryType,
    SearchQuery,
    SearchResult,
    SearchResultSet,
)


class TestEntryType:
    """Tests for EntryType enum (T009)."""

    def test_from_string_daily(self):
        """Test parsing 'daily' string to EntryType.DAILY."""
        result = EntryType.from_string("daily")
        assert result == EntryType.DAILY

    def test_from_string_case_insensitive(self):
        """Test case-insensitive parsing."""
        assert EntryType.from_string("DAILY") == EntryType.DAILY
        assert EntryType.from_string("Daily") == EntryType.DAILY
        assert EntryType.from_string("daily") == EntryType.DAILY
        assert EntryType.from_string("PROJECT") == EntryType.PROJECT
        assert EntryType.from_string("People") == EntryType.PEOPLE
        assert EntryType.from_string("memory") == EntryType.MEMORY

    def test_from_string_invalid(self):
        """Test invalid entry type raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            EntryType.from_string("invalid")

        error_msg = str(exc_info.value)
        assert "Invalid entry type" in error_msg
        assert "invalid" in error_msg
        assert "daily" in error_msg
        assert "project" in error_msg

    def test_to_folder_name_daily(self):
        """Test folder name for daily entries."""
        assert EntryType.DAILY.to_folder_name() == "daily"

    def test_to_folder_name_memory_plural(self):
        """Test folder name for memories (plural form)."""
        assert EntryType.MEMORY.to_folder_name() == "memories"

    def test_to_folder_name_projects_plural(self):
        """Test folder name for projects (plural form)."""
        assert EntryType.PROJECT.to_folder_name() == "projects"

    def test_to_folder_name_people_plural(self):
        """Test folder name for people (plural form)."""
        assert EntryType.PEOPLE.to_folder_name() == "people"

    def test_display_name(self):
        """Test display name capitalization."""
        assert EntryType.DAILY.display_name() == "Daily"
        assert EntryType.PROJECT.display_name() == "Project"
        assert EntryType.PEOPLE.display_name() == "People"
        assert EntryType.MEMORY.display_name() == "Memory"


class TestSearchQuery:
    """Tests for SearchQuery model validation (T010)."""

    def test_create_valid_query(self):
        """Test creating valid SearchQuery."""
        query = SearchQuery(search_text="test")
        assert query.search_text == "test"
        assert query.case_sensitive is False
        assert query.limit is None

    def test_empty_search_text_raises_error(self):
        """Test empty search_text raises validation error."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            SearchQuery(search_text="")

        assert "search_text" in str(exc_info.value)

    def test_date_range_validation_pass(self):
        """Test valid date range (after <= before)."""
        query = SearchQuery(
            search_text="test",
            date_after=date(2024, 11, 1),
            date_before=date(2024, 11, 10),
        )
        assert query.date_after == date(2024, 11, 1)
        assert query.date_before == date(2024, 11, 10)

    def test_date_range_validation_fail(self):
        """Test invalid date range (after > before) raises error."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            SearchQuery(
                search_text="test",
                date_after=date(2024, 11, 10),
                date_before=date(2024, 11, 1),
            )

        error_msg = str(exc_info.value)
        assert "date_after" in error_msg or "date_before" in error_msg

    def test_limit_must_be_positive(self):
        """Test limit must be positive integer."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            SearchQuery(search_text="test", limit=0)

        with pytest.raises(ValidationError):
            SearchQuery(search_text="test", limit=-1)

    def test_entry_types_default_to_all(self):
        """Test entry_types defaults to all types."""
        query = SearchQuery(search_text="test")
        assert len(query.entry_types) == len(EntryType)
        assert EntryType.DAILY in query.entry_types
        assert EntryType.PROJECT in query.entry_types
        assert EntryType.PEOPLE in query.entry_types
        assert EntryType.MEMORY in query.entry_types

    def test_entry_types_custom(self):
        """Test setting specific entry types."""
        query = SearchQuery(
            search_text="test", entry_types=[EntryType.DAILY, EntryType.PROJECT]
        )
        assert len(query.entry_types) == 2
        assert EntryType.DAILY in query.entry_types
        assert EntryType.PROJECT in query.entry_types


class TestSearchResult:
    """Tests for SearchResult model (T011)."""

    def test_create_valid_result(self):
        """Test creating valid SearchResult."""
        result = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Feeling anxious about the project launch",
        )
        assert result.file_path == Path("daily/2024-11-01.md")
        assert result.entry_type == EntryType.DAILY
        assert result.line_number == 5

    def test_display_date_with_date(self):
        """Test display_date property with valid date."""
        result = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Test line",
        )
        assert result.display_date == "November 01, 2024"

    def test_display_date_no_date(self):
        """Test display_date property returns 'No date' when None."""
        result = SearchResult(
            file_path=Path("projects/launch.md"),
            entry_type=EntryType.PROJECT,
            entry_date=None,
            line_number=5,
            matched_line="Test line",
        )
        assert result.display_date == "No date"

    def test_format_display(self):
        """Test format_display method."""
        result = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Feeling anxious",
            context_before=["Previous line 1", "Previous line 2"],
            context_after=["Next line 1"],
        )
        display = result.format_display()
        assert "2024-11-01.md" in display
        assert "5" in display
        assert "Feeling anxious" in display
        assert "Previous line 1" in display
        assert "Next line 1" in display

    def test_get_context(self):
        """Test get_context method."""
        result = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Matched line",
            context_before=["Line 1", "Line 2", "Line 3"],
            context_after=["Line 6", "Line 7", "Line 8"],
        )
        context = result.get_context(lines_before=2, lines_after=2)
        assert "Line 2" in context
        assert "Line 3" in context
        assert "Matched line" in context
        assert "Line 6" in context
        assert "Line 7" in context
        assert "Line 1" not in context  # Outside the limit

    def test_to_dict(self):
        """Test to_dict method."""
        result = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Test line",
            context_before=["Before"],
            context_after=["After"],
        )
        result_dict = result.to_dict()
        assert result_dict["file_path"] == "daily/2024-11-01.md"
        assert result_dict["entry_type"] == "daily"
        assert result_dict["entry_date"] == "2024-11-01"
        assert result_dict["line_number"] == 5
        assert result_dict["matched_line"] == "Test line"
        assert result_dict["context_before"] == ["Before"]
        assert result_dict["context_after"] == ["After"]


class TestSearchResultSet:
    """Tests for SearchResultSet model (T012)."""

    def test_create_valid_result_set(self):
        """Test creating valid SearchResultSet."""
        query = SearchQuery(search_text="test")
        result_set = SearchResultSet(
            results=[],
            query=query,
            total_count=0,
            execution_time_ms=42.5,
            files_scanned=10,
        )
        assert result_set.total_count == 0
        assert result_set.execution_time_ms == 42.5
        assert result_set.files_scanned == 10

    def test_is_empty_true(self):
        """Test is_empty property when no results."""
        query = SearchQuery(search_text="test")
        result_set = SearchResultSet(
            results=[],
            query=query,
            total_count=0,
            execution_time_ms=10.0,
            files_scanned=5,
        )
        assert result_set.is_empty is True

    def test_is_empty_false(self):
        """Test is_empty property when has results."""
        query = SearchQuery(search_text="test")
        result = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Test line",
        )
        result_set = SearchResultSet(
            results=[result],
            query=query,
            total_count=1,
            execution_time_ms=10.0,
            files_scanned=5,
        )
        assert result_set.is_empty is False

    def test_result_summary(self):
        """Test result_summary property."""
        query = SearchQuery(search_text="test")
        result1 = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Test",
        )
        result2 = SearchResult(
            file_path=Path("daily/2024-11-02.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 2),
            line_number=3,
            matched_line="Test",
        )
        result_set = SearchResultSet(
            results=[result1, result2],
            query=query,
            total_count=2,
            execution_time_ms=125.5,
            files_scanned=10,
        )
        summary = result_set.result_summary
        assert "2" in summary
        assert "2 files" in summary
        assert "125" in summary or "126" in summary  # Rounding

    def test_sort_by_date_descending(self):
        """Test sorting results by date (newest first)."""
        query = SearchQuery(search_text="test")
        result1 = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Test",
        )
        result2 = SearchResult(
            file_path=Path("daily/2024-11-05.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 5),
            line_number=3,
            matched_line="Test",
        )
        result3 = SearchResult(
            file_path=Path("daily/2024-11-03.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 3),
            line_number=7,
            matched_line="Test",
        )
        result_set = SearchResultSet(
            results=[result1, result2, result3],
            query=query,
            total_count=3,
            execution_time_ms=10.0,
            files_scanned=3,
        )
        sorted_set = result_set.sort_by_date(descending=True)
        assert sorted_set.results[0].entry_date == date(2024, 11, 5)
        assert sorted_set.results[1].entry_date == date(2024, 11, 3)
        assert sorted_set.results[2].entry_date == date(2024, 11, 1)

    def test_export_to_markdown(self, tmp_path):
        """Test exporting results to markdown file."""
        query = SearchQuery(search_text="anxious")
        result = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Feeling anxious",
            context_before=["Previous context"],
            context_after=["Following context"],
        )
        result_set = SearchResultSet(
            results=[result],
            query=query,
            total_count=1,
            execution_time_ms=50.0,
            files_scanned=10,
        )

        output_file = tmp_path / "results.md"
        result_set.export_to_markdown(output_file)

        assert output_file.exists()
        content = output_file.read_text()
        assert "# Search Results" in content
        assert "anxious" in content
        assert "2024-11-01.md" in content

    def test_filter_by_type(self):
        """Test filtering results by entry type."""
        query = SearchQuery(search_text="test")
        daily_result = SearchResult(
            file_path=Path("daily/2024-11-01.md"),
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Test",
        )
        project_result = SearchResult(
            file_path=Path("projects/launch.md"),
            entry_type=EntryType.PROJECT,
            entry_date=None,
            line_number=3,
            matched_line="Test",
        )
        result_set = SearchResultSet(
            results=[daily_result, project_result],
            query=query,
            total_count=2,
            execution_time_ms=10.0,
            files_scanned=2,
        )

        filtered = result_set.filter_by_type(EntryType.DAILY)
        assert filtered.total_count == 1
        assert filtered.results[0].entry_type == EntryType.DAILY

    def test_group_by_file(self):
        """Test grouping results by file."""
        query = SearchQuery(search_text="test")
        file1 = Path("daily/2024-11-01.md")
        file2 = Path("daily/2024-11-02.md")

        result1 = SearchResult(
            file_path=file1,
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=5,
            matched_line="Test 1",
        )
        result2 = SearchResult(
            file_path=file1,
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 1),
            line_number=10,
            matched_line="Test 2",
        )
        result3 = SearchResult(
            file_path=file2,
            entry_type=EntryType.DAILY,
            entry_date=date(2024, 11, 2),
            line_number=3,
            matched_line="Test 3",
        )

        result_set = SearchResultSet(
            results=[result1, result2, result3],
            query=query,
            total_count=3,
            execution_time_ms=10.0,
            files_scanned=2,
        )

        grouped = result_set.group_by_file()
        assert len(grouped) == 2
        assert len(grouped[file1]) == 2
        assert len(grouped[file2]) == 1
