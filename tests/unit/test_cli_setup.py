"""
Unit tests for the setup CLI command.

Tests path validation, user input handling, and configuration creation.
"""

from pathlib import Path

import pytest

from ai_journal_kit.core.validation import path_is_writable, validate_ide, validate_path


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


@pytest.mark.unit
def test_validate_ide_accepts_valid_choices():
    """Test that validate_ide accepts all valid IDE choices (lines 49-55)."""
    valid_ides = ["cursor", "windsurf", "claude-code", "copilot", "all"]

    for ide in valid_ides:
        result = validate_ide(ide)
        assert result == ide.lower()

    # Test case insensitivity
    assert validate_ide("CURSOR") == "cursor"
    assert validate_ide("Windsurf") == "windsurf"


@pytest.mark.unit
def test_validate_ide_rejects_invalid_choice():
    """Test that validate_ide rejects invalid IDE choices (lines 52-53)."""
    with pytest.raises(ValueError, match="Invalid IDE"):
        validate_ide("invalid-ide")

    with pytest.raises(ValueError, match="Must be one of"):
        validate_ide("vscode")


@pytest.mark.unit
def test_path_is_writable_for_existing_directory(tmp_path):
    """Test path_is_writable for existing directories (lines 67-68)."""
    test_dir = tmp_path / "writable"
    test_dir.mkdir()

    # Should be writable
    assert path_is_writable(test_dir) is True


@pytest.mark.unit
def test_path_is_writable_for_nonexistent_path(tmp_path):
    """Test path_is_writable for nonexistent paths (lines 69-71)."""
    nonexistent = tmp_path / "nonexistent"

    # Should check parent's writability
    assert path_is_writable(nonexistent) is True


@pytest.mark.unit
def test_path_is_writable_for_readonly_parent(tmp_path):
    """Test path_is_writable when parent is read-only (line 71)."""
    import os

    # Create a directory and make it read-only
    readonly_dir = tmp_path / "readonly"
    readonly_dir.mkdir()

    # Make readonly (remove write permission)
    os.chmod(readonly_dir, 0o555)

    try:
        nonexistent = readonly_dir / "test"
        result = path_is_writable(nonexistent)
        # Should be False since parent is read-only
        assert result is False
    finally:
        # Restore write permission for cleanup
        os.chmod(readonly_dir, 0o755)
