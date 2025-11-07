"""Platform detection and platform-specific path handling."""

import platform
import sys
from pathlib import Path


def is_windows() -> bool:
    """Check if running on Windows."""
    return sys.platform == "win32"


def is_macos() -> bool:
    """Check if running on macOS."""
    return sys.platform == "darwin"


def is_linux() -> bool:
    """Check if running on Linux."""
    return sys.platform.startswith("linux")


def get_platform_name() -> str:
    """Get human-readable platform name."""
    if is_windows():
        return "Windows"
    elif is_macos():
        return "macOS"
    elif is_linux():
        return "Linux"
    else:
        return platform.system()


def normalize_path(path: str | Path) -> Path:
    """Normalize path for current platform."""
    p = Path(path).expanduser().resolve()
    return p


def can_create_symlinks() -> bool:
    """Check if system supports symlink creation."""
    if is_windows():
        # On Windows, junctions don't require admin privileges
        # but we need to check if _winapi is available
        try:
            import _winapi  # noqa: F401

            return True
        except ImportError:
            return False
    else:
        # Unix-like systems support symlinks
        return True
