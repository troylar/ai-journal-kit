"""Integration tests for search functionality.

Tests the interaction between SearchEngine, FileScanner, and date_utils.

Issue: #6 - Search & Filter Enhancement
Coverage Target: 100%
"""

from datetime import date

import pytest

from ai_journal_kit.core.search_engine import SearchEngine
from ai_journal_kit.core.search_result import EntryType, SearchQuery


@pytest.fixture
def test_journal_path(tmp_path):
    """Create test journal with realistic structure."""
    # Create folder structure
    daily_dir = tmp_path / "daily"
    projects_dir = tmp_path / "projects"
    people_dir = tmp_path / "people"
    memories_dir = tmp_path / "memories"

    daily_dir.mkdir()
    projects_dir.mkdir()
    people_dir.mkdir()
    memories_dir.mkdir()

    # Create sample files with content
    (daily_dir / "2024-11-01.md").write_text(
        "# Daily Entry\n\nFeeling anxious about the [[projects/q4-launch]] deadline.\nNeed to focus on priorities."
    )
    (daily_dir / "2024-11-05.md").write_text(
        "# Daily Entry\n\nMet with [[people/sarah]] to discuss project features.\nFeeling more confident now."
    )
    (daily_dir / "2024-11-10.md").write_text(
        "# Daily Entry\n\nFeeling much better about progress.\nCompleted major milestone today."
    )
    (projects_dir / "q4-launch.md").write_text(
        "# Q4 Launch\n\nProject to launch new features by Q4.\nKey objectives and milestones."
    )
    (people_dir / "sarah.md").write_text(
        "# Sarah\n\nSenior developer on the team.\nExpert in backend systems."
    )
    (memories_dir / "deadline-flexibility.md").write_text(
        "# Deadline Flexibility\n\nLearned to be flexible with deadlines.\nImportant lesson from Q4 project."
    )

    return tmp_path


class TestSearchEngineIntegration:
    """Integration tests for SearchEngine with real file system (T030, T031 - US1)."""

    def test_search_with_date_filter_integration(self, test_journal_path):
        """Test end-to-end search with date filtering."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="Feeling", date_after=date(2024, 11, 5))

        result_set = engine.search(query)

        # Should find matches in files dated 2024-11-05 and later
        assert result_set.total_count >= 2
        for result in result_set.results:
            if result.entry_date:
                assert result.entry_date >= date(2024, 11, 5)
            assert "Feeling" in result.matched_line

    def test_search_with_type_filter_integration(self, test_journal_path):
        """Test end-to-end search with entry type filtering."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="Entry", entry_types=[EntryType.DAILY])

        result_set = engine.search(query)

        # All results should be from daily entries
        assert result_set.total_count >= 1
        assert all(r.entry_type == EntryType.DAILY for r in result_set.results)

    def test_search_with_combined_filters_integration(self, test_journal_path):
        """Test search with multiple filters combined."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(
            search_text="Feeling",
            date_after=date(2024, 11, 1),
            date_before=date(2024, 11, 5),
            entry_types=[EntryType.DAILY],
        )

        result_set = engine.search(query)

        # Should match all filters
        for result in result_set.results:
            assert result.entry_type == EntryType.DAILY
            if result.entry_date:
                assert date(2024, 11, 1) <= result.entry_date <= date(2024, 11, 5)
            assert "Feeling" in result.matched_line

    def test_search_performance_large_journal(self, tmp_path):
        """Test search performance with larger journal (T031 - US1)."""
        # Create a larger journal for performance testing
        daily_dir = tmp_path / "daily"
        daily_dir.mkdir()

        # Create 100 files with various content using unique dates
        from datetime import timedelta

        base_date = date(2024, 1, 1)
        for i in range(100):
            file_date = base_date + timedelta(days=i)
            content = (
                f"# Daily Entry {i}\n\nSome content here.\nMore text on line {i}.\nFeeling good."
            )
            (daily_dir / f"{file_date.isoformat()}.md").write_text(content)

        engine = SearchEngine(tmp_path)
        query = SearchQuery(search_text="Feeling")

        result_set = engine.search(query)

        # Should complete in reasonable time (< 2 seconds)
        assert result_set.execution_time_ms < 2000
        assert result_set.files_scanned == 100

    def test_search_with_context_extraction_integration(self, test_journal_path):
        """Test that context lines are correctly extracted."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="anxious")

        result_set = engine.search(query)

        assert result_set.total_count >= 1
        result = result_set.results[0]

        # Context should be populated
        assert isinstance(result.context_before, list)
        assert isinstance(result.context_after, list)

        # Should have the title in context
        assert any("Daily Entry" in line for line in result.context_before)


class TestDateFilteringIntegration:
    """Integration tests for date filtering across components (T042, T043 - US2)."""

    def test_relative_date_parsing_integration(self, test_journal_path):
        """Test relative dates work end-to-end."""
        from ai_journal_kit.core.date_utils import parse_date

        # Parse relative date
        seven_days_ago = parse_date("7d")

        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="Entry", date_after=seven_days_ago)

        result_set = engine.search(query)

        # Should find recent entries
        for result in result_set.results:
            if result.entry_date:
                assert result.entry_date >= seven_days_ago

    def test_date_range_validation_integration(self, test_journal_path):
        """Test invalid date ranges are caught."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            SearchQuery(
                search_text="test",
                date_after=date(2024, 11, 10),
                date_before=date(2024, 11, 1),
            )

    def test_date_extraction_from_files_integration(self, test_journal_path):
        """Test date extraction works with FileScanner."""
        from ai_journal_kit.core.file_scanner import FileScanner

        scanner = FileScanner(test_journal_path)
        files = scanner.scan(entry_types=[EntryType.DAILY])

        # All daily files should have dates extracted
        for file_path in files:
            from ai_journal_kit.core.date_utils import extract_date_from_filename

            extracted_date = extract_date_from_filename(file_path)
            assert extracted_date is not None
            assert isinstance(extracted_date, date)


class TestCrossReferenceIntegration:
    """Integration tests for cross-reference search (T052, T053, T054 - US3)."""

    def test_cross_reference_search_integration(self, test_journal_path):
        """Test searching for cross-references end-to-end."""
        engine = SearchEngine(test_journal_path)

        result_set = engine.search_cross_references("people/sarah")

        # Should find entries referencing [[people/sarah]]
        assert result_set.total_count >= 1
        assert any("sarah" in r.matched_line.lower() for r in result_set.results)

    def test_cross_reference_with_type_filter(self, test_journal_path):
        """Test cross-reference search combined with type filter."""
        engine = SearchEngine(test_journal_path)

        result_set = engine.search_cross_references("people/sarah", entry_types=[EntryType.DAILY])

        # Should find only daily entries with the reference
        for result in result_set.results:
            assert result.entry_type == EntryType.DAILY
            assert "sarah" in result.matched_line.lower()

    def test_cross_reference_with_date_filter(self, test_journal_path):
        """Test cross-reference with date filtering."""
        engine = SearchEngine(test_journal_path)

        result_set = engine.search_cross_references(
            "people/sarah", date_after=date(2024, 11, 5), date_before=date(2024, 11, 5)
        )

        # Should find only references in date range
        for result in result_set.results:
            if result.entry_date:
                assert result.entry_date == date(2024, 11, 5)

    def test_invalid_cross_reference_format(self, test_journal_path):
        """Test handling of invalid cross-reference formats."""
        engine = SearchEngine(test_journal_path)

        # Empty reference should raise error
        with pytest.raises(ValueError):
            engine.search_cross_references("")
