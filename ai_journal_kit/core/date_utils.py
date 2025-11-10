"""Date utility functions for search filtering.

This module provides utilities for parsing dates from filenames and
handling relative date specifications.

Issue: #6 - Search & Filter Enhancement
"""

import re
from datetime import date, timedelta
from pathlib import Path


def parse_date(date_str: str) -> date:
    """
    Parse date from string.

    Supports:
    - Absolute: YYYY-MM-DD
    - Relative: Nd (N days ago), Nw (N weeks ago), Nm (N months ago)

    Args:
        date_str: Date string to parse

    Returns:
        Parsed date object

    Raises:
        ValueError: If date string is invalid

    Examples:
        >>> parse_date("2024-10-01")
        date(2024, 10, 1)

        >>> parse_date("7d")  # 7 days ago from today
        date(...)
    """
    # Try absolute date format first
    absolute_pattern = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
    match = absolute_pattern.match(date_str)
    if match:
        try:
            year, month, day = map(int, match.groups())
            return date(year, month, day)
        except ValueError as e:
            raise ValueError(f"Invalid date: {date_str}") from e

    # Try relative date format
    relative_pattern = re.compile(r"^(\d+)([dwm])$")
    match = relative_pattern.match(date_str)
    if match:
        return parse_relative_date(date_str)

    raise ValueError(
        f"Invalid date format: '{date_str}'. "
        "Expected YYYY-MM-DD or relative format (e.g., '7d', '2w', '1m')"
    )


def parse_relative_date(relative: str) -> date:
    """
    Parse relative dates like '7d', '1w', '1m' to absolute dates.

    Args:
        relative: Relative date string (e.g., "7d", "2w", "1m")

    Returns:
        Absolute date object

    Raises:
        ValueError: If relative date format is invalid

    Examples:
        >>> parse_relative_date("7d")
        date(...)  # 7 days ago

        >>> parse_relative_date("2w")
        date(...)  # 2 weeks ago
    """
    today = date.today()

    pattern = re.compile(r"^(\d+)([dwm])$")
    match = pattern.match(relative)

    if not match:
        raise ValueError(
            f"Invalid relative date format: '{relative}'. "
            "Expected format like '7d' (days), '2w' (weeks), or '1m' (months)"
        )

    amount, unit = match.groups()
    amount = int(amount)

    if unit == "d":
        # N days ago
        return today - timedelta(days=amount)
    elif unit == "w":
        # N weeks ago
        return today - timedelta(weeks=amount)
    elif unit == "m":
        # N months ago (approximate as 30 days per month)
        return today - timedelta(days=amount * 30)
    else:
        raise ValueError(f"Invalid time unit: '{unit}'. Expected 'd', 'w', or 'm'")


def extract_date_from_filename(file_path: Path) -> date | None:
    """
    Extract date from filename if present.

    Looks for YYYY-MM-DD pattern in filename.

    Args:
        file_path: Path to file

    Returns:
        Extracted date or None if no date found

    Examples:
        >>> extract_date_from_filename(Path("daily/2024-11-01.md"))
        date(2024, 11, 1)

        >>> extract_date_from_filename(Path("projects/launch.md"))
        None
    """
    # Look for YYYY-MM-DD pattern in filename
    pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    match = pattern.search(file_path.name)

    if not match:
        return None

    try:
        year, month, day = map(int, match.groups())
        return date(year, month, day)
    except ValueError:
        # Invalid date (e.g., 2024-13-01)
        return None
