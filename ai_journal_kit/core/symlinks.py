"""Cross-platform symlink and junction management."""

import os
import sys
from pathlib import Path

from ai_journal_kit.utils.ui import console


def create_link(target: Path, link: Path) -> bool:
    """Create symlink or junction depending on platform.

    Args:
        target: The directory to link to (must exist)
        link: The link location (must not exist)

    Returns:
        True if successful, False otherwise
    """
    if sys.platform == "win32":
        return _create_junction_windows(target, link)
    else:
        return _create_symlink_unix(target, link)


def _create_symlink_unix(target: Path, link: Path) -> bool:
    """Create symbolic link on Unix-like systems."""
    try:
        if link.exists() or link.is_symlink():
            link.unlink()
        os.symlink(target, link, target_is_directory=True)
        return True
    except (OSError, PermissionError) as e:
        console.print(f"[yellow]Warning: Could not create symlink: {e}[/yellow]")
        return False


def _create_junction_windows(target: Path, link: Path) -> bool:
    """Create junction on Windows (no admin required for junctions)."""
    try:
        import _winapi

        if link.exists():
            if link.is_dir():
                link.rmdir()
            else:
                link.unlink()
        _winapi.CreateJunction(str(target), str(link))
        return True
    except (ImportError, OSError, PermissionError) as e:
        console.print(f"[yellow]Warning: Could not create junction: {e}[/yellow]")
        return False


def is_broken(link: Path) -> bool:
    """Check if symlink/junction is broken.

    Args:
        link: Path to check

    Returns:
        True if link is broken, False otherwise
    """
    if not link.exists():
        # Check if it's a symlink that doesn't resolve
        try:
            if link.is_symlink():
                # Symlink exists but target doesn't
                return True
            # On Windows, check if it's a junction
            if sys.platform == "win32" and link.parent.exists():
                # If the path doesn't exist and parent does, might be broken junction
                return True
        except (OSError, PermissionError):
            return True
    return False


def update_link_target(link: Path, new_target: Path):
    """Update symlink/junction to point to new target.

    Args:
        link: Existing link to update
        new_target: New target directory
    """
    # Remove old link
    if link.exists() or link.is_symlink():
        link.unlink()

    # Create new link
    create_link(new_target, link)


def get_link_target(link: Path) -> Path | None:
    """Get the target of a symlink/junction.

    Args:
        link: Link to inspect

    Returns:
        Target path or None if not a link
    """
    try:
        if link.is_symlink():
            return link.readlink()
    except (OSError, AttributeError):
        pass
    return None
