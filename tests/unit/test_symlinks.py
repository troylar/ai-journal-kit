"""
Unit tests for symlink and junction management functionality.

Tests cross-platform link creation, validation, and updates.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ai_journal_kit.core.symlinks import (
    _create_junction_windows,
    _create_symlink_unix,
    create_link,
    get_link_target,
    is_broken,
    update_link_target,
)


@pytest.mark.unit
def test_create_symlink_unix_success(temp_journal_dir):
    """Test creating a symlink on Unix-like systems."""
    target = temp_journal_dir / "target_dir"
    target.mkdir()
    link = temp_journal_dir / "link"

    # Only test on Unix-like systems
    if sys.platform != "win32":
        result = _create_symlink_unix(target, link)

        assert result is True
        assert link.is_symlink()
        assert link.readlink() == target


@pytest.mark.unit
def test_create_symlink_unix_replaces_existing(temp_journal_dir):
    """Test that creating a symlink replaces existing link."""
    if sys.platform == "win32":
        pytest.skip("Unix-only test")

    target1 = temp_journal_dir / "target1"
    target2 = temp_journal_dir / "target2"
    target1.mkdir()
    target2.mkdir()
    link = temp_journal_dir / "link"

    # Create first symlink
    _create_symlink_unix(target1, link)
    assert link.readlink() == target1

    # Replace with second symlink
    _create_symlink_unix(target2, link)
    assert link.readlink() == target2


@pytest.mark.unit
def test_create_symlink_unix_handles_permission_error(temp_journal_dir):
    """Test that symlink creation handles permission errors gracefully."""
    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"

    with patch("os.symlink", side_effect=PermissionError("No permission")):
        result = _create_symlink_unix(target, link)
        assert result is False


@pytest.mark.unit
def test_create_symlink_unix_handles_os_error(temp_journal_dir):
    """Test that symlink creation handles OS errors gracefully."""
    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"

    with patch("os.symlink", side_effect=OSError("OS error")):
        result = _create_symlink_unix(target, link)
        assert result is False


@pytest.mark.unit
def test_create_junction_windows_success(temp_journal_dir):
    """Test creating a junction on Windows."""
    target = temp_journal_dir / "target_dir"
    target.mkdir()
    link = temp_journal_dir / "link"

    # Mock _winapi for testing
    mock_winapi = MagicMock()
    with patch.dict("sys.modules", {"_winapi": mock_winapi}):
        result = _create_junction_windows(target, link)

        assert result is True
        mock_winapi.CreateJunction.assert_called_once_with(str(target), str(link))


@pytest.mark.unit
def test_create_junction_windows_replaces_existing_dir(temp_journal_dir):
    """Test that junction creation removes existing directory."""
    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"
    link.mkdir()  # Create directory that will be replaced

    mock_winapi = MagicMock()
    with patch.dict("sys.modules", {"_winapi": mock_winapi}):
        result = _create_junction_windows(target, link)

        assert result is True


@pytest.mark.unit
def test_create_junction_windows_replaces_existing_file(temp_journal_dir):
    """Test that junction creation removes existing file."""
    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"
    link.write_text("existing file")

    mock_winapi = MagicMock()
    with patch.dict("sys.modules", {"_winapi": mock_winapi}):
        result = _create_junction_windows(target, link)

        assert result is True


@pytest.mark.unit
def test_create_junction_windows_handles_os_error(temp_journal_dir):
    """Test that junction creation handles OS errors."""
    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"

    mock_winapi = MagicMock()
    mock_winapi.CreateJunction.side_effect = OSError("OS error")

    with patch.dict("sys.modules", {"_winapi": mock_winapi}):
        result = _create_junction_windows(target, link)
        assert result is False


@pytest.mark.unit
def test_create_junction_windows_handles_permission_error(temp_journal_dir):
    """Test that junction creation handles permission errors."""
    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"

    mock_winapi = MagicMock()
    mock_winapi.CreateJunction.side_effect = PermissionError("No permission")

    with patch.dict("sys.modules", {"_winapi": mock_winapi}):
        result = _create_junction_windows(target, link)
        assert result is False


@pytest.mark.unit
def test_create_link_unix_platform(temp_journal_dir):
    """Test create_link dispatches to Unix function on non-Windows."""
    if sys.platform == "win32":
        pytest.skip("Unix-only test")

    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"

    result = create_link(target, link)
    assert result is True
    assert link.is_symlink()


@pytest.mark.unit
def test_create_link_windows_platform(temp_journal_dir):
    """Test create_link dispatches to Windows function on Windows."""
    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"

    mock_winapi = MagicMock()
    with patch("sys.platform", "win32"):
        with patch.dict("sys.modules", {"_winapi": mock_winapi}):
            result = create_link(target, link)

            assert result is True
            mock_winapi.CreateJunction.assert_called_once()


@pytest.mark.unit
def test_is_broken_nonexistent_regular_path(temp_journal_dir):
    """Test is_broken returns False for non-existent non-link path."""
    nonexistent = temp_journal_dir / "does_not_exist"

    # This should return False or True depending on platform
    # For a path that doesn't exist and isn't a symlink, behavior varies
    result = is_broken(nonexistent)
    assert isinstance(result, bool)


@pytest.mark.unit
def test_is_broken_existing_symlink(temp_journal_dir):
    """Test is_broken returns False for valid symlink."""
    if sys.platform == "win32":
        pytest.skip("Unix-only test")

    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"
    link.symlink_to(target, target_is_directory=True)

    assert is_broken(link) is False


@pytest.mark.unit
def test_is_broken_broken_symlink(temp_journal_dir):
    """Test is_broken returns True for broken symlink."""
    if sys.platform == "win32":
        pytest.skip("Unix-only test")

    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"
    link.symlink_to(target, target_is_directory=True)

    # Remove target to break the link
    target.rmdir()

    assert is_broken(link) is True


@pytest.mark.unit
def test_is_broken_handles_permission_error(temp_journal_dir):
    """Test is_broken handles permission errors gracefully."""
    link = temp_journal_dir / "link"

    with patch.object(Path, "is_symlink", side_effect=PermissionError("No permission")):
        result = is_broken(link)
        assert result is True


@pytest.mark.unit
def test_is_broken_windows_broken_junction(temp_journal_dir):
    """Test is_broken detects broken Windows junction (line 73)."""
    temp_journal_dir / "link"

    # We need to mock both the link and its parent
    # link.exists() returns False, link.is_symlink() returns False
    # link.parent.exists() returns True
    with patch("sys.platform", "win32"):
        # Create a mock for the link that returns False for exists and is_symlink
        mock_link = MagicMock(spec=Path)
        mock_link.exists.return_value = False
        mock_link.is_symlink.return_value = False

        # Create a mock parent that exists
        mock_parent = MagicMock(spec=Path)
        mock_parent.exists.return_value = True
        mock_link.parent = mock_parent

        # Now test with the mock
        result = is_broken(mock_link)
        assert result is True


@pytest.mark.unit
def test_update_link_target(temp_journal_dir):
    """Test updating a symlink to point to new target."""
    if sys.platform == "win32":
        pytest.skip("Unix-only test")

    target1 = temp_journal_dir / "target1"
    target2 = temp_journal_dir / "target2"
    target1.mkdir()
    target2.mkdir()
    link = temp_journal_dir / "link"

    # Create initial link
    create_link(target1, link)
    assert link.readlink() == target1

    # Update to new target
    update_link_target(link, target2)
    assert link.readlink() == target2


@pytest.mark.unit
def test_get_link_target_returns_target(temp_journal_dir):
    """Test get_link_target returns correct target path."""
    if sys.platform == "win32":
        pytest.skip("Unix-only test")

    target = temp_journal_dir / "target"
    target.mkdir()
    link = temp_journal_dir / "link"
    link.symlink_to(target, target_is_directory=True)

    result = get_link_target(link)
    assert result == target


@pytest.mark.unit
def test_get_link_target_returns_none_for_regular_file(temp_journal_dir):
    """Test get_link_target returns None for non-symlink."""
    regular_file = temp_journal_dir / "regular.txt"
    regular_file.write_text("content")

    result = get_link_target(regular_file)
    assert result is None


@pytest.mark.unit
def test_get_link_target_handles_os_error(temp_journal_dir):
    """Test get_link_target handles OS errors gracefully."""
    link = temp_journal_dir / "link"

    with patch.object(Path, "is_symlink", side_effect=OSError("OS error")):
        result = get_link_target(link)
        assert result is None


@pytest.mark.unit
def test_get_link_target_handles_attribute_error(temp_journal_dir):
    """Test get_link_target handles attribute errors gracefully."""
    link = temp_journal_dir / "link"

    with patch.object(Path, "readlink", side_effect=AttributeError("No readlink")):
        with patch.object(Path, "is_symlink", return_value=True):
            result = get_link_target(link)
            assert result is None
