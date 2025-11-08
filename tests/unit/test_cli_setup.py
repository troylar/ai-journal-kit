"""
Unit tests for the setup CLI command.

Tests path validation, user input handling, and configuration creation.
"""

from pathlib import Path

import pytest

from ai_journal_kit.core.validation import validate_path


@pytest.mark.unit
def test_validate_path_accepts_valid_directory(tmp_path):
    """Test that validate_path accepts valid directories."""
    test_dir = tmp_path / "journal"
    test_dir.mkdir()

    result = validate_path(str(test_dir))
    assert isinstance(result, Path)
    assert result.exists()


@pytest.mark.unit
def test_validate_path_accepts_file_path(tmp_path):
    """Test that validate_path accepts file paths (returns path, doesn't validate if it's a file)."""
    test_file = tmp_path / "not_a_dir.txt"
    test_file.write_text("test")

    # validate_path doesn't check if it's a file, just normalizes the path
    result = validate_path(str(test_file))
    assert isinstance(result, Path)


@pytest.mark.unit
def test_validate_path_accepts_nonexistent_directory(tmp_path):
    """Test that validate_path accepts non-existent directories in existing parent."""
    test_dir = tmp_path / "new_journal"

    # Should accept path if parent exists
    result = validate_path(str(test_dir))
    assert isinstance(result, Path)


@pytest.mark.unit
def test_validate_path_rejects_invalid_parent():
    """Test that validate_path rejects paths with non-existent parents."""
    with pytest.raises(ValueError, match="Parent directory does not exist"):
        validate_path("/nonexistent/parent/journal")


@pytest.mark.unit
def test_validate_path_rejects_null_byte():
    """Test that validate_path rejects paths with null bytes."""
    with pytest.raises(ValueError, match="Path contains null byte"):
        validate_path("/tmp/test\0path")


@pytest.mark.unit
def test_validate_path_expands_home_directory(tmp_path):
    """Test that validate_path expands ~ to home directory."""
    result = validate_path("~")
    assert isinstance(result, Path)
    assert result.exists()
    assert str(result) != "~"
