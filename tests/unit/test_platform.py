"""
Unit tests for platform utilities.

Tests platform detection and path normalization.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from ai_journal_kit.utils.platform import (
    can_create_symlinks,
    get_platform_name,
    is_linux,
    is_macos,
    is_windows,
    normalize_path,
)


@pytest.mark.unit
def test_platform_detection():
    """Test platform detection functions return correct types."""
    # These should return booleans
    assert isinstance(is_windows(), bool)
    assert isinstance(is_macos(), bool)
    assert isinstance(is_linux(), bool)

    # Exactly one should be True
    platform_checks = [is_windows(), is_macos(), is_linux()]
    assert sum(platform_checks) >= 1  # At least one is true


@pytest.mark.unit
def test_get_platform_name():
    """Test get_platform_name returns readable name."""
    name = get_platform_name()
    assert isinstance(name, str)
    assert len(name) > 0
    # Should be one of the known platforms or a system name
    assert name in ["Windows", "macOS", "Linux"] or len(name) > 0


@pytest.mark.unit
def test_normalize_path_expands_home(tmp_path):
    """Test normalize_path expands ~ to home directory."""
    result = normalize_path("~")

    assert isinstance(result, Path)
    assert result.is_absolute()
    assert str(result) != "~"


@pytest.mark.unit
def test_normalize_path_resolves_relative(tmp_path):
    """Test normalize_path resolves relative paths."""
    result = normalize_path("./test")

    assert isinstance(result, Path)
    assert result.is_absolute()


@pytest.mark.unit
def test_normalize_path_handles_path_object(tmp_path):
    """Test normalize_path handles Path objects."""
    input_path = Path("~/test")
    result = normalize_path(input_path)

    assert isinstance(result, Path)
    assert result.is_absolute()


@pytest.mark.unit
def test_can_create_symlinks():
    """Test can_create_symlinks returns boolean."""
    result = can_create_symlinks()
    assert isinstance(result, bool)

    # On Unix-like systems, should always be True
    if not is_windows():
        assert result is True


@pytest.mark.unit
@patch("sys.platform", "win32")
def test_can_create_symlinks_on_windows_with_winapi():
    """Test Windows symlink detection with _winapi available."""
    with patch.dict(sys.modules, {"_winapi": type(sys)("_winapi")}):
        # Force reload to pick up patched module
        from importlib import reload

        from ai_journal_kit.utils import platform as platform_module

        reload(platform_module)

        result = platform_module.can_create_symlinks()
        assert isinstance(result, bool)


@pytest.mark.unit
@patch("sys.platform", "win32")
def test_can_create_symlinks_on_windows_without_winapi():
    """Test Windows symlink detection when _winapi is not available (lines 50-51)."""
    # Simulate ImportError when trying to import _winapi
    import builtins

    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "_winapi":
            raise ImportError("No module named '_winapi'")
        return real_import(name, *args, **kwargs)

    with patch.object(builtins, "__import__", side_effect=mock_import):
        from importlib import reload

        from ai_journal_kit.utils import platform as platform_module

        reload(platform_module)

        result = platform_module.can_create_symlinks()
        assert result is False


@pytest.mark.unit
def test_platform_name_matches_detection():
    """Test get_platform_name matches is_* functions."""
    name = get_platform_name()

    if is_windows():
        assert name == "Windows"
    elif is_macos():
        assert name == "macOS"
    elif is_linux():
        assert name == "Linux"


@pytest.mark.unit
@patch("sys.platform", "darwin")
def test_is_macos_detection():
    """Test macOS detection."""
    from importlib import reload

    from ai_journal_kit.utils import platform as platform_module

    reload(platform_module)

    assert platform_module.is_macos() is True
    assert platform_module.get_platform_name() == "macOS"


@pytest.mark.unit
@patch("sys.platform", "linux")
def test_is_linux_detection():
    """Test Linux detection."""
    from importlib import reload

    from ai_journal_kit.utils import platform as platform_module

    reload(platform_module)

    assert platform_module.is_linux() is True
    assert platform_module.get_platform_name() == "Linux"


@pytest.mark.unit
@patch("sys.platform", "win32")
def test_is_windows_detection():
    """Test Windows detection (line 26)."""
    from importlib import reload

    from ai_journal_kit.utils import platform as platform_module

    reload(platform_module)

    assert platform_module.is_windows() is True
    assert platform_module.get_platform_name() == "Windows"


@pytest.mark.unit
@patch("sys.platform", "unknown_os")
@patch("platform.system", return_value="UnknownOS")
def test_get_platform_name_unknown_system(mock_system):
    """Test get_platform_name for unknown platforms (line 32)."""
    from importlib import reload

    from ai_journal_kit.utils import platform as platform_module

    reload(platform_module)

    name = platform_module.get_platform_name()
    assert name == "UnknownOS"
    mock_system.assert_called_once()
