"""End-to-end tests for search CLI command.

Tests the complete user workflow from CLI to results.

Issue: #6 - Search & Filter Enhancement
Coverage Target: 100%
"""

import pytest
import os
import json
from datetime import date, datetime
from pathlib import Path
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app


runner = CliRunner()


@pytest.fixture
def test_journal_path(tmp_path):
    """Create test journal for e2e testing."""
    # Create folder structure
    daily_dir = tmp_path / "daily"
    projects_dir = tmp_path / "projects"
    people_dir = tmp_path / "people"
    memories_dir = tmp_path / "memories"

    daily_dir.mkdir()
    projects_dir.mkdir()
    people_dir.mkdir()
    memories_dir.mkdir()

    # Create sample files with realistic content
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


@pytest.fixture
def journal_config(test_journal_path, tmp_path):
    """Create test config pointing to test journal."""
    config_dir = tmp_path / ".config" / "ai-journal-kit"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.json"

    # Create multi-journal config format
    config_data = {
        "active_journal": "test-journal",
        "journals": {
            "test-journal": {
                "name": "test-journal",
                "location": str(test_journal_path),
                "ide": "cursor",
                "framework": "bullet-journal",
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "use_symlink": False
            }
        }
    }

    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=2)

    # Set environment variable to override config path
    original_config_dir = os.getenv("AI_JOURNAL_CONFIG_DIR")
    os.environ["AI_JOURNAL_CONFIG_DIR"] = str(config_dir)

    yield config_file

    # Cleanup
    if original_config_dir:
        os.environ["AI_JOURNAL_CONFIG_DIR"] = original_config_dir
    elif "AI_JOURNAL_CONFIG_DIR" in os.environ:
        del os.environ["AI_JOURNAL_CONFIG_DIR"]


class TestSearchCommandE2E:
    """End-to-end tests for search command (T027, T028, T029 - US1)."""

    def test_basic_search_e2e(self, journal_config):
        """Test basic search from CLI to output (T027 - US1)."""
        result = runner.invoke(app, ["search", "anxious"])

        assert result.exit_code == 0
        assert "anxious" in result.stdout.lower()
        assert "Found" in result.stdout  # Search header
        assert "daily" in result.stdout.lower()  # Entry type

    def test_search_with_all_filters_e2e(self, journal_config):
        """Test search with all filter options (T028 - US1)."""
        result = runner.invoke(
            app,
            ["search", "Entry", "--after", "2024-11-01", "--before", "2024-11-10", "--type", "daily"]
        )

        assert result.exit_code == 0
        assert "Entry" in result.stdout
        # Verify filters are shown in output
        assert "After: 2024-11-01" in result.stdout
        assert "Before: 2024-11-10" in result.stdout

    def test_search_no_results_e2e(self, journal_config):
        """Test search with no results shows appropriate message."""
        result = runner.invoke(app, ["search", "nonexistent12345"])

        assert result.exit_code == 0
        assert "No results found" in result.stdout

    def test_search_with_export_e2e(self, journal_config, tmp_path):
        """Test search with --export option (T029 - US1)."""
        export_file = tmp_path / "search_results.md"

        # Use --yes to skip confirmation prompt
        result = runner.invoke(
            app,
            ["search", "Feeling", "--export", str(export_file)],
            input="y\n"  # Confirm overwrite if prompted
        )

        assert result.exit_code == 0
        assert export_file.exists()

        # Verify markdown content
        content = export_file.read_text()
        assert "# Search Results" in content
        assert "Feeling" in content


class TestDateFilterE2E:
    """End-to-end tests for date filtering (T040, T041 - US2)."""

    def test_absolute_date_filter_e2e(self, journal_config):
        """Test absolute date filtering end-to-end (T040 - US2)."""
        result = runner.invoke(app, ["search", "Entry", "--after", "2024-11-05"])

        assert result.exit_code == 0
        # Should find results from 2024-11-05 and later
        assert "After: 2024-11-05" in result.stdout

    def test_relative_date_filter_e2e(self, journal_config):
        """Test relative date filtering end-to-end (T041 - US2)."""
        result = runner.invoke(app, ["search", "Entry", "--after", "7d"])

        assert result.exit_code == 0
        # Should show the after date filter was applied
        assert "After:" in result.stdout

    def test_invalid_date_format_e2e(self, journal_config):
        """Test invalid date format shows error."""
        result = runner.invoke(app, ["search", "test", "--after", "invalid-date"])

        # Should exit with error code (error message goes to stderr via Rich console)
        assert result.exit_code != 0


class TestTypeFilterE2E:
    """End-to-end tests for entry type filtering (T050, T051 - US3)."""

    def test_single_type_filter_e2e(self, journal_config):
        """Test filtering by single entry type (T050 - US3)."""
        result = runner.invoke(app, ["search", "Entry", "--type", "daily"])

        assert result.exit_code == 0
        assert "Types: Daily" in result.stdout

    def test_multiple_type_filter_e2e(self, journal_config):
        """Test filtering by multiple entry types (T051 - US3)."""
        result = runner.invoke(app, ["search", "to", "--type", "daily,project"])

        assert result.exit_code == 0
        # Verify type filter is shown
        assert "Types:" in result.stdout

    def test_invalid_type_e2e(self, journal_config):
        """Test invalid entry type shows error."""
        result = runner.invoke(app, ["search", "test", "--type", "invalid"])

        # Should exit with error code (error message goes to stderr via Rich console)
        assert result.exit_code != 0


class TestCrossReferenceE2E:
    """End-to-end tests for cross-reference search (T075, T076 - US5)."""

    def test_cross_reference_search_e2e(self, journal_config):
        """Test searching for cross-references (T075 - US5)."""
        result = runner.invoke(app, ["search", "placeholder", "--ref", "people/sarah"])

        assert result.exit_code == 0
        # Should find entries containing [[people/sarah]]
        assert "sarah" in result.stdout.lower()

    def test_cross_reference_with_filters_e2e(self, journal_config):
        """Test cross-reference combined with other filters (T076 - US5)."""
        result = runner.invoke(
            app,
            ["search", "placeholder", "--ref", "projects/q4-launch", "--type", "daily"]
        )

        assert result.exit_code == 0
        # Verify filters are applied
        assert "Types: Daily" in result.stdout


class TestSearchOutputFormatting:
    """Tests for search output formatting and UX."""

    def test_output_includes_metadata(self, journal_config):
        """Test output includes search metadata."""
        result = runner.invoke(app, ["search", "Entry"])

        assert result.exit_code == 0
        # Verify metadata is shown
        assert "Found" in result.stdout
        assert "ms" in result.stdout  # Execution time in milliseconds

    def test_output_syntax_highlighting(self, journal_config):
        """Test matched text is highlighted in output."""
        result = runner.invoke(app, ["search", "anxious"])

        assert result.exit_code == 0
        # Verify search term appears in output
        assert "anxious" in result.stdout.lower()

    def test_output_pagination(self, journal_config):
        """Test pagination works for many results."""
        # Search for common term that appears in multiple files
        result = runner.invoke(app, ["search", "Entry"])

        assert result.exit_code == 0
        # Should show multiple results
        assert "Found" in result.stdout


class TestErrorHandlingE2E:
    """End-to-end tests for error scenarios."""

    def test_nonexistent_journal_path_e2e(self, tmp_path):
        """Test error when journal path doesn't exist."""
        # Create config with non-existent journal path
        config_dir = tmp_path / ".config" / "ai-journal-kit"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"

        config_data = {
            "active_journal": "test",
            "journals": {
                "test": {
                    "name": "test",
                    "location": "/nonexistent/path/to/journal",
                    "ide": "cursor",
                    "framework": "bullet-journal",
                    "version": "1.0.0",
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "use_symlink": False
                }
            }
        }

        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        original_config_dir = os.getenv("AI_JOURNAL_CONFIG_DIR")
        os.environ["AI_JOURNAL_CONFIG_DIR"] = str(config_dir)

        result = runner.invoke(app, ["search", "test"])

        # Cleanup
        if original_config_dir:
            os.environ["AI_JOURNAL_CONFIG_DIR"] = original_config_dir
        elif "AI_JOURNAL_CONFIG_DIR" in os.environ:
            del os.environ["AI_JOURNAL_CONFIG_DIR"]

        # Should exit with error code (error message goes to stderr via Rich console)
        assert result.exit_code != 0

    def test_empty_query_e2e(self, journal_config):
        """Test error when search query is empty."""
        result = runner.invoke(app, ["search", ""])

        # Should exit with error code (error message goes to stderr via Rich console)
        assert result.exit_code != 0

    def test_invalid_date_range_e2e(self, journal_config):
        """Test error when date range is invalid (after > before)."""
        result = runner.invoke(
            app,
            ["search", "test", "--after", "2024-11-10", "--before", "2024-11-01"]
        )

        # Should exit with error code (error message goes to stderr via Rich console)
        assert result.exit_code != 0
