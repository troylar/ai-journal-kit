"""Unit tests for search engine core.

Tests for SearchEngine class and methods.

Issue: #6 - Search & Filter Enhancement
Coverage Target: 100%
"""

from datetime import date
from pathlib import Path

import pytest

from ai_journal_kit.core.search_engine import SearchEngine
from ai_journal_kit.core.search_result import EntryType, SearchQuery


@pytest.fixture
def test_journal_path(tmp_path):
    """Create test journal with sample entries."""
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
        "# Daily Entry\n\nFeeling anxious about the [[projects/q4-launch]] deadline."
    )
    (daily_dir / "2024-11-05.md").write_text(
        "# Daily Entry\n\nMet with [[people/sarah]] to discuss project features."
    )
    (daily_dir / "2024-11-10.md").write_text(
        "# Daily Entry\n\nFeeling much better about progress."
    )
    (projects_dir / "q4-launch.md").write_text(
        "# Q4 Launch\n\nProject to launch new features by Q4."
    )
    (people_dir / "sarah.md").write_text("# Sarah\n\nSenior developer on the team.")
    (memories_dir / "deadline-flexibility.md").write_text(
        "# Deadline Flexibility\n\nLearned to be flexible with deadlines."
    )

    return tmp_path


class TestSearchEngineInit:
    """Tests for SearchEngine initialization (T015 - US1)."""

    def test_init_valid_path(self, test_journal_path):
        """Test initializing with valid journal path."""
        engine = SearchEngine(test_journal_path)
        assert engine.journal_path == test_journal_path.resolve()
        assert engine.file_scanner is not None

    def test_init_nonexistent_path_raises_error(self):
        """Test initializing with non-existent path raises error."""
        with pytest.raises(ValueError) as exc_info:
            SearchEngine(Path("/nonexistent/path"))

        assert "does not exist" in str(exc_info.value)

    def test_init_file_not_directory_raises_error(self, tmp_path):
        """Test initializing with file path (not directory) raises error."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        with pytest.raises(ValueError) as exc_info:
            SearchEngine(test_file)

        assert "not a directory" in str(exc_info.value)


class TestSearchEngineBasicSearch:
    """Tests for basic text search (T015, T016, T017 - US1)."""

    def test_search_finds_single_match(self, test_journal_path):
        """Test searching for text with single match."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="Q4 Launch")

        result_set = engine.search(query)

        assert result_set.total_count == 1
        assert "q4-launch.md" in str(result_set.results[0].file_path)
        assert "Q4 Launch" in result_set.results[0].matched_line

    def test_search_finds_multiple_matches(self, test_journal_path):
        """Test searching for text with multiple matches."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="Feeling")

        result_set = engine.search(query)

        # "Feeling" appears in 2024-11-01.md and 2024-11-10.md
        assert result_set.total_count >= 2
        assert all("daily" in str(r.file_path) for r in result_set.results)

    def test_search_case_insensitive_default(self, test_journal_path):
        """Test search is case-insensitive by default."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="ANXIOUS", case_sensitive=False)

        result_set = engine.search(query)

        assert result_set.total_count >= 1
        # Should match "anxious" in lowercase
        assert any("anxious" in r.matched_line.lower() for r in result_set.results)

    def test_search_case_sensitive(self, test_journal_path):
        """Test case-sensitive search."""
        engine = SearchEngine(test_journal_path)

        # This should NOT match "feeling" (lowercase)
        query = SearchQuery(search_text="Feeling", case_sensitive=True)
        result_set = engine.search(query)

        # Should only match the exact case "Feeling"
        assert all("Feeling" in r.matched_line for r in result_set.results)

    def test_search_no_results(self, test_journal_path):
        """Test search with no matches returns empty result set."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="nonexistenttext12345")

        result_set = engine.search(query)

        assert result_set.is_empty is True
        assert result_set.total_count == 0

    def test_search_extracts_context(self, test_journal_path):
        """Test search extracts context lines before/after match."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="anxious")

        result_set = engine.search(query)

        assert result_set.total_count >= 1
        result = result_set.results[0]
        # Context should be populated (may be empty if at start/end of file)
        assert isinstance(result.context_before, list)
        assert isinstance(result.context_after, list)

    def test_search_with_limit(self, test_journal_path):
        """Test search respects limit parameter."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="Entry", limit=2)

        result_set = engine.search(query)

        assert result_set.total_count <= 2


class TestSearchEngineFileSearch:
    """Tests for _search_in_file method (T016 - US1)."""

    def test_search_in_file_with_match(self, test_journal_path):
        """Test _search_in_file finds matches."""
        engine = SearchEngine(test_journal_path)
        daily_file = test_journal_path / "daily" / "2024-11-01.md"

        results = engine._search_in_file(daily_file, "anxious")

        assert len(results) >= 1
        assert all(r.file_path == daily_file for r in results)
        assert all("anxious" in r.matched_line.lower() for r in results)

    def test_search_in_file_no_match(self, test_journal_path):
        """Test _search_in_file returns empty list with no matches."""
        engine = SearchEngine(test_journal_path)
        daily_file = test_journal_path / "daily" / "2024-11-01.md"

        results = engine._search_in_file(daily_file, "nonexistent")

        assert len(results) == 0

    def test_search_in_file_escapes_special_characters(self, tmp_path):
        """Test _search_in_file safely handles regex special chars."""
        # Create test file with special characters
        test_dir = tmp_path / "daily"
        test_dir.mkdir()
        test_file = test_dir / "2024-11-01.md"
        test_file.write_text("Looking for [special] characters like * and ?")

        engine = SearchEngine(tmp_path)
        results = engine._search_in_file(test_file, "[special]")

        # Should find the literal "[special]" text
        assert len(results) >= 1
        assert "[special]" in results[0].matched_line


class TestSearchEngineContextExtraction:
    """Tests for _extract_context method (T017 - US1)."""

    def test_extract_context_middle_of_file(self, test_journal_path):
        """Test extracting context from middle of file."""
        engine = SearchEngine(test_journal_path)
        lines = [
            "Line 0\n",
            "Line 1\n",
            "Line 2\n",
            "Matched line\n",
            "Line 4\n",
            "Line 5\n",
        ]

        context_before, context_after = engine._extract_context(
            lines, 3, context_lines=2
        )

        assert context_before == ["Line 1\n", "Line 2\n"]
        assert context_after == ["Line 4\n", "Line 5\n"]

    def test_extract_context_start_of_file(self, test_journal_path):
        """Test extracting context at start of file (no lines before)."""
        engine = SearchEngine(test_journal_path)
        lines = ["Matched line\n", "Line 1\n", "Line 2\n"]

        context_before, context_after = engine._extract_context(
            lines, 0, context_lines=2
        )

        assert context_before == []  # No lines before
        assert context_after == ["Line 1\n", "Line 2\n"]

    def test_extract_context_end_of_file(self, test_journal_path):
        """Test extracting context at end of file (no lines after)."""
        engine = SearchEngine(test_journal_path)
        lines = ["Line 0\n", "Line 1\n", "Matched line\n"]

        context_before, context_after = engine._extract_context(
            lines, 2, context_lines=2
        )

        assert context_before == ["Line 0\n", "Line 1\n"]
        assert context_after == []  # No lines after


class TestSearchEngineDateFilter:
    """Tests for date filtering (T032, T034 - US2)."""

    def test_apply_date_filter_after(self, test_journal_path):
        """Test filtering results after a date."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="Entry", date_after=date(2024, 11, 5))

        result_set = engine.search(query)

        # Should only include files dated 2024-11-05 and later
        for result in result_set.results:
            if result.entry_date:
                assert result.entry_date >= date(2024, 11, 5)

    def test_apply_date_filter_before(self, test_journal_path):
        """Test filtering results before a date."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="Entry", date_before=date(2024, 11, 5))

        result_set = engine.search(query)

        # Should only include files dated 2024-11-05 and earlier
        for result in result_set.results:
            if result.entry_date:
                assert result.entry_date <= date(2024, 11, 5)

    def test_apply_date_filter_range(self, test_journal_path):
        """Test filtering results within date range."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(
            search_text="Entry",
            date_after=date(2024, 11, 1),
            date_before=date(2024, 11, 5),
        )

        result_set = engine.search(query)

        # Should only include files in the date range
        for result in result_set.results:
            if result.entry_date:
                assert date(2024, 11, 1) <= result.entry_date <= date(2024, 11, 5)


class TestSearchEngineTypeFilter:
    """Tests for entry type filtering (T044, T045 - US3)."""

    def test_apply_type_filter_single(self, test_journal_path):
        """Test filtering by single entry type."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(search_text="Entry", entry_types=[EntryType.DAILY])

        result_set = engine.search(query)

        # All results should be daily entries
        assert all(r.entry_type == EntryType.DAILY for r in result_set.results)

    def test_apply_type_filter_multiple(self, test_journal_path):
        """Test filtering by multiple entry types."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(
            search_text="to", entry_types=[EntryType.DAILY, EntryType.PROJECT]
        )

        result_set = engine.search(query)

        # All results should be either daily or project entries
        assert all(
            r.entry_type in [EntryType.DAILY, EntryType.PROJECT]
            for r in result_set.results
        )

    def test_apply_type_filter_excludes_others(self, test_journal_path):
        """Test type filter excludes non-matching types."""
        engine = SearchEngine(test_journal_path)
        query = SearchQuery(
            search_text="developer",
            entry_types=[EntryType.DAILY],  # Looking for "developer" in daily only
        )

        result_set = engine.search(query)

        # Should not find "developer" since it's in people/sarah.md
        # (unless it also appears in daily entries)
        assert all(r.entry_type == EntryType.DAILY for r in result_set.results)


class TestSearchEngineCrossReferences:
    """Tests for cross-reference search."""

    def test_search_cross_references(self, test_journal_path):
        """Test searching for cross-references."""
        engine = SearchEngine(test_journal_path)

        result_set = engine.search_cross_references("people/sarah")

        # Should find entries that reference [[people/sarah]]
        assert result_set.total_count >= 1
        assert any("sarah" in r.matched_line.lower() for r in result_set.results)

    def test_search_cross_references_normalizes_extension(self, test_journal_path):
        """Test that .md extension is normalized."""
        engine = SearchEngine(test_journal_path)

        result_set = engine.search_cross_references("people/sarah.md")

        # Should still find references even with .md extension
        assert result_set.total_count >= 1

    def test_extract_cross_references(self, test_journal_path):
        """Test extracting wiki-links from content."""
        engine = SearchEngine(test_journal_path)
        content = "Met with [[people/sarah]] to discuss [[projects/q4-launch]]."

        refs = engine._extract_cross_references(content)

        assert len(refs) == 2
        assert "people/sarah" in refs
        assert "projects/q4-launch" in refs

    def test_extract_cross_references_with_aliases(self, test_journal_path):
        """Test extracting wiki-links with aliases."""
        engine = SearchEngine(test_journal_path)
        content = "Met with [[people/sarah|Sarah]] today."

        refs = engine._extract_cross_references(content)

        # Should extract just the reference, not the alias
        assert len(refs) >= 1
        assert "people/sarah" in refs

    def test_search_cross_references_empty_raises_error(self, test_journal_path):
        """Test that empty reference raises error."""
        engine = SearchEngine(test_journal_path)

        with pytest.raises(ValueError) as exc_info:
            engine.search_cross_references("")

        assert "empty" in str(exc_info.value).lower()


class TestSearchEngineScanFiles:
    """Tests for scan_files method."""

    def test_scan_files_all(self, test_journal_path):
        """Test scanning all files."""
        engine = SearchEngine(test_journal_path)

        files = engine.scan_files()

        assert len(files) >= 6  # All test files

    def test_scan_files_with_type_filter(self, test_journal_path):
        """Test scanning with entry type filter."""
        engine = SearchEngine(test_journal_path)

        files = engine.scan_files(entry_types=[EntryType.DAILY])

        assert len(files) == 3  # Three daily files
        assert all("daily" in str(f) for f in files)

    def test_scan_files_with_date_filter(self, test_journal_path):
        """Test scanning with date filter."""
        engine = SearchEngine(test_journal_path)

        files = engine.scan_files(
            date_after=date(2024, 11, 5), date_before=date(2024, 11, 10)
        )

        # Should include files in date range
        assert len(files) >= 2
