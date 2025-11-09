"""
Unit tests for validation utilities.

Tests framework and IDE validation functions.
"""

import pytest

from ai_journal_kit.core.validation import validate_framework, validate_ide


@pytest.mark.unit
def test_validate_framework_accepts_valid_default():
    """Test validate_framework accepts 'default'."""
    result = validate_framework("default")
    assert result == "default"


@pytest.mark.unit
def test_validate_framework_accepts_valid_gtd():
    """Test validate_framework accepts 'gtd'."""
    result = validate_framework("gtd")
    assert result == "gtd"

    # Also test case-insensitive
    result_upper = validate_framework("GTD")
    assert result_upper == "gtd"


@pytest.mark.unit
def test_validate_framework_accepts_valid_para():
    """Test validate_framework accepts 'para'."""
    result = validate_framework("para")
    assert result == "para"


@pytest.mark.unit
def test_validate_framework_accepts_valid_bullet_journal():
    """Test validate_framework accepts 'bullet-journal'."""
    result = validate_framework("bullet-journal")
    assert result == "bullet-journal"

    # Test case-insensitive
    result_upper = validate_framework("Bullet-Journal")
    assert result_upper == "bullet-journal"


@pytest.mark.unit
def test_validate_framework_accepts_valid_zettelkasten():
    """Test validate_framework accepts 'zettelkasten'."""
    result = validate_framework("zettelkasten")
    assert result == "zettelkasten"


@pytest.mark.unit
def test_validate_framework_rejects_invalid():
    """Test validate_framework rejects invalid framework names."""
    with pytest.raises(ValueError) as exc_info:
        validate_framework("invalid-framework")

    assert "Invalid framework" in str(exc_info.value)
    assert "invalid-framework" in str(exc_info.value)


@pytest.mark.unit
def test_validate_framework_rejects_empty_string():
    """Test validate_framework rejects empty string."""
    with pytest.raises(ValueError):
        validate_framework("")


@pytest.mark.unit
def test_validate_ide_accepts_all_valid_ides():
    """Test validate_ide accepts all valid IDE names."""
    valid_ides = ["cursor", "windsurf", "claude-code", "copilot", "all"]

    for ide in valid_ides:
        result = validate_ide(ide)
        assert result == ide


@pytest.mark.unit
def test_validate_ide_case_insensitive():
    """Test validate_ide is case-insensitive."""
    result = validate_ide("CURSOR")
    assert result == "cursor"

    result = validate_ide("Windsurf")
    assert result == "windsurf"
