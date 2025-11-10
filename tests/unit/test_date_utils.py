"""Unit tests for date utility functions.

Tests for date parsing and extraction functions.

Issue: #6 - Search & Filter Enhancement
Coverage Target: 100%
"""

import pytest
from datetime import date, timedelta
from pathlib import Path

from ai_journal_kit.core.date_utils import (
    parse_date,
    parse_relative_date,
    extract_date_from_filename,
)


class TestParseDate:
    """Tests for parse_date function (T013)."""

    def test_parse_absolute_date(self):
        """Test parsing absolute date in YYYY-MM-DD format."""
        result = parse_date("2024-10-01")
        assert result == date(2024, 10, 1)

    def test_parse_relative_days(self):
        """Test parsing relative date in 'Nd' format."""
        result = parse_date("7d")
        expected = date.today() - timedelta(days=7)
        assert result == expected

    def test_parse_relative_weeks(self):
        """Test parsing relative date in 'Nw' format."""
        result = parse_date("2w")
        expected = date.today() - timedelta(weeks=2)
        assert result == expected

    def test_parse_relative_months(self):
        """Test parsing relative date in 'Nm' format."""
        result = parse_date("1m")
        expected = date.today() - timedelta(days=30)
        assert result == expected

    def test_parse_invalid_format_raises_error(self):
        """Test invalid date format raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            parse_date("invalid")

        error_msg = str(exc_info.value)
        assert "Invalid date format" in error_msg

    def test_parse_invalid_date_values(self):
        """Test invalid date values raise error."""
        with pytest.raises(ValueError):
            parse_date("2024-13-01")  # Invalid month

        with pytest.raises(ValueError):
            parse_date("2024-02-30")  # Invalid day


class TestParseRelativeDate:
    """Tests for parse_relative_date function (T033 - US2)."""

    def test_parse_days_ago(self):
        """Test parsing 'Nd' format (N days ago)."""
        result = parse_relative_date("7d")
        expected = date.today() - timedelta(days=7)
        assert result == expected

    def test_parse_weeks_ago(self):
        """Test parsing 'Nw' format (N weeks ago)."""
        result = parse_relative_date("2w")
        expected = date.today() - timedelta(weeks=2)
        assert result == expected

    def test_parse_months_ago(self):
        """Test parsing 'Nm' format (N months ago)."""
        result = parse_relative_date("1m")
        expected = date.today() - timedelta(days=30)
        assert result == expected

    def test_parse_multiple_months(self):
        """Test parsing multiple months."""
        result = parse_relative_date("3m")
        expected = date.today() - timedelta(days=90)
        assert result == expected

    def test_invalid_format_raises_error(self):
        """Test invalid relative format raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            parse_relative_date("invalid")

        error_msg = str(exc_info.value)
        assert "Invalid relative date format" in error_msg

        with pytest.raises(ValueError) as exc_info:
            parse_relative_date("7x")

        error_msg = str(exc_info.value)
        assert "Invalid relative date format" in error_msg


class TestExtractDateFromFilename:
    """Tests for extract_date_from_filename function (T013)."""

    def test_extract_from_daily_entry(self):
        """Test extracting date from daily entry filename."""
        result = extract_date_from_filename(Path("daily/2024-11-01.md"))
        assert result == date(2024, 11, 1)

    def test_extract_no_date_returns_none(self):
        """Test returns None when no date in filename."""
        result = extract_date_from_filename(Path("projects/launch.md"))
        assert result is None

    def test_extract_from_nested_path(self):
        """Test extracting date from nested path."""
        result = extract_date_from_filename(
            Path("/path/to/journal/daily/2024-11-01.md")
        )
        assert result == date(2024, 11, 1)

    def test_invalid_date_returns_none(self):
        """Test invalid date (like 2024-13-01) returns None."""
        result = extract_date_from_filename(Path("2024-13-01.md"))
        assert result is None  # 13 is not a valid month

    def test_extract_from_filename_only(self):
        """Test extracting date when pattern is in filename only."""
        result = extract_date_from_filename(Path("2024-11-05.md"))
        assert result == date(2024, 11, 5)

    def test_extract_with_text_before_date(self):
        """Test extracting date with text before date pattern."""
        result = extract_date_from_filename(Path("notes-2024-11-15.md"))
        assert result == date(2024, 11, 15)
