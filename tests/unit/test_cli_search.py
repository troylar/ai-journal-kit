"""Unit tests for search CLI command.

Tests for search command argument parsing and output formatting.

Issue: #6 - Search & Filter Enhancement
Coverage Target: 100%
"""

import pytest
from datetime import date
from pathlib import Path
from typer.testing import CliRunner

from ai_journal_kit.cli.search import (
    search,
    parse_entry_types,
    validate_date_range,
    format_search_results,
    display_search_header,
)
from ai_journal_kit.core.search_result import EntryType, SearchQuery, SearchResult, SearchResultSet
from rich.console import Console


runner = CliRunner()


class TestSearchCommand:
    """Tests for search CLI command (T018 - US1)."""

    def test_format_search_results_with_results(self, capsys):
        """Test formatting results with matches."""
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
            execution_time_ms=50.0,
            files_scanned=1,
        )

        console = Console()
        format_search_results(result_set, console)

        # Verify output contains result
        # Note: Rich output goes to console, we just verify no errors

    def test_format_search_results_empty(self, capsys):
        """Test formatting with no results."""
        query = SearchQuery(search_text="test")
        result_set = SearchResultSet(
            results=[],
            query=query,
            total_count=0,
            execution_time_ms=10.0,
            files_scanned=5,
        )

        console = Console()
        format_search_results(result_set, console)

        # Verify no error

    def test_display_search_header(self):
        """Test search header display."""
        query = SearchQuery(
            search_text="anxiety",
            date_after=date(2024, 11, 1),
            entry_types=[EntryType.DAILY],
        )

        # Should not raise error
        display_search_header(query, 5, 125.5)


class TestParseEntryTypes:
    """Tests for parse_entry_types function."""

    def test_parse_single_type(self):
        """Test parsing single entry type."""
        result = parse_entry_types("daily")
        assert result == [EntryType.DAILY]

    def test_parse_multiple_types(self):
        """Test parsing comma-separated types."""
        result = parse_entry_types("daily,project")
        assert len(result) == 2
        assert EntryType.DAILY in result
        assert EntryType.PROJECT in result

    def test_parse_multiple_types_with_spaces(self):
        """Test parsing with extra whitespace."""
        result = parse_entry_types("daily, project, people")
        assert len(result) == 3
        assert EntryType.DAILY in result
        assert EntryType.PROJECT in result
        assert EntryType.PEOPLE in result

    def test_parse_case_insensitive(self):
        """Test case-insensitive parsing."""
        result = parse_entry_types("DAILY,Project")
        assert len(result) == 2
        assert EntryType.DAILY in result
        assert EntryType.PROJECT in result

    def test_parse_invalid_type_raises_error(self):
        """Test parsing invalid type raises error."""
        with pytest.raises(ValueError) as exc_info:
            parse_entry_types("invalid")

        error_msg = str(exc_info.value)
        assert "invalid" in error_msg.lower()

    def test_parse_empty_string_raises_error(self):
        """Test empty string raises error."""
        with pytest.raises(ValueError) as exc_info:
            parse_entry_types("")

        assert "No entry types" in str(exc_info.value)

    def test_parse_mixed_valid_invalid(self):
        """Test mix of valid and invalid types."""
        with pytest.raises(ValueError) as exc_info:
            parse_entry_types("daily,invalid,project")

        error_msg = str(exc_info.value)
        assert "invalid" in error_msg.lower()


class TestValidateDateRange:
    """Tests for validate_date_range function."""

    def test_valid_range_passes(self):
        """Test valid date range doesn't raise error."""
        # Should not raise
        validate_date_range(date(2024, 11, 1), date(2024, 11, 10))

    def test_invalid_range_raises_error(self):
        """Test invalid range (after > before) raises error."""
        with pytest.raises(ValueError) as exc_info:
            validate_date_range(date(2024, 11, 10), date(2024, 11, 1))

        error_msg = str(exc_info.value)
        assert "Invalid date range" in error_msg
        assert "cannot be later than" in error_msg

    def test_none_dates_pass(self):
        """Test None values don't cause errors."""
        # Should not raise
        validate_date_range(None, None)

    def test_only_after_passes(self):
        """Test with only after date."""
        # Should not raise
        validate_date_range(date(2024, 11, 1), None)

    def test_only_before_passes(self):
        """Test with only before date."""
        # Should not raise
        validate_date_range(None, date(2024, 11, 10))

    def test_same_date_passes(self):
        """Test with same date for both."""
        # Should not raise
        validate_date_range(date(2024, 11, 5), date(2024, 11, 5))
