"""Path and input validation utilities."""

from pathlib import Path
from typing import Literal

IDE_CHOICES = Literal["cursor", "windsurf", "claude-code", "copilot", "all"]
FRAMEWORK_CHOICES = Literal["default", "gtd", "para", "bullet-journal", "zettelkasten"]


def validate_path(path: str | Path) -> Path:
    """Validate and normalize a filesystem path.

    Args:
        path: Path to validate

    Returns:
        Normalized absolute Path

    Raises:
        ValueError: If path is invalid
    """
    path_str = str(path)

    # Check for null bytes
    if "\0" in path_str:
        raise ValueError("Path contains null byte")

    # Expand ~ and resolve to absolute
    expanded = Path(path).expanduser().resolve()

    # Check if parent directory exists
    if not expanded.parent.exists():
        raise ValueError(f"Parent directory does not exist: {expanded.parent}")

    return expanded


def validate_ide(ide: str) -> str:
    """Validate IDE choice.

    Args:
        ide: IDE name to validate

    Returns:
        Validated IDE name

    Raises:
        ValueError: If IDE is not supported
    """
    valid_ides = ["cursor", "windsurf", "claude-code", "copilot", "all"]
    ide_lower = ide.lower()

    if ide_lower not in valid_ides:
        raise ValueError(f"Invalid IDE: {ide}. Must be one of: {', '.join(valid_ides)}")

    return ide_lower


def validate_framework(framework: str) -> str:
    """Validate framework choice.

    Args:
        framework: Framework name to validate

    Returns:
        Validated framework name

    Raises:
        ValueError: If framework is not supported
    """
    valid_frameworks = ["default", "gtd", "para", "bullet-journal", "zettelkasten"]
    framework_lower = framework.lower()

    if framework_lower not in valid_frameworks:
        raise ValueError(
            f"Invalid framework: {framework}. Must be one of: {', '.join(valid_frameworks)}"
        )

    return framework_lower


def path_is_writable(path: Path) -> bool:
    """Check if path is writable.

    Args:
        path: Path to check

    Returns:
        True if writable, False otherwise
    """
    if path.exists():
        return bool(path.is_dir() and (path.stat().st_mode & 0o200))
    else:
        # Check if parent is writable
        return bool(path.parent.exists() and (path.parent.stat().st_mode & 0o200))
