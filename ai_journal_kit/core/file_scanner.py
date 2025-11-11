"""File scanner utility for journal entries.

This module provides efficient file scanning across journal folders
with entry type detection.

Issue: #6 - Search & Filter Enhancement
"""

from datetime import date
from pathlib import Path

from ai_journal_kit.core.date_utils import extract_date_from_filename
from ai_journal_kit.core.search_result import EntryType


class FileScanner:
    """Efficient file scanner with caching."""

    def __init__(self, journal_path: Path):
        """
        Initialize file scanner.

        Args:
            journal_path: Absolute path to journal directory

        Raises:
            ValueError: If journal_path doesn't exist or is not a directory
        """
        if not journal_path.exists():
            raise ValueError(f"Journal path does not exist: {journal_path}")
        if not journal_path.is_dir():
            raise ValueError(f"Journal path is not a directory: {journal_path}")

        self.journal_path = journal_path.resolve()

    def scan(
        self,
        pattern: str = "*.md",
        entry_types: list[EntryType] | None = None,
        date_after: date | None = None,
        date_before: date | None = None,
    ) -> list[Path]:
        """
        Scan for files matching criteria.

        Args:
            pattern: Glob pattern (default: *.md)
            entry_types: Filter by entry types
            date_after: Include files dated on or after
            date_before: Include files dated on or before

        Returns:
            List of matching file paths
        """
        # Use pathlib.Path.rglob() for cross-platform recursive search
        all_files = list(self.journal_path.rglob(pattern))

        filtered_files = []
        for file_path in all_files:
            # Filter by entry type if specified
            if entry_types:
                try:
                    file_entry_type = self.get_entry_type(file_path)
                    if file_entry_type not in entry_types:
                        continue
                except ValueError:
                    # Skip files that don't match known entry types
                    continue

            # Filter by date if specified
            if date_after or date_before:
                file_date = extract_date_from_filename(file_path)
                if file_date:
                    if date_after and file_date < date_after:
                        continue
                    if date_before and file_date > date_before:
                        continue

            filtered_files.append(file_path)

        return filtered_files

    def get_entry_type(self, file_path: Path) -> EntryType:
        """
        Determine entry type from file path.

        Args:
            file_path: Path to file

        Returns:
            EntryType enum value

        Raises:
            ValueError: If entry type cannot be determined

        Examples:
            >>> scanner.get_entry_type(Path("journal/daily/2024-11-01.md"))
            EntryType.DAILY

            >>> scanner.get_entry_type(Path("journal/projects/launch.md"))
            EntryType.PROJECT
        """
        # Get relative path from journal root
        try:
            relative_path = file_path.relative_to(self.journal_path)
        except ValueError:
            # File is not in journal directory
            raise ValueError(f"File is not in journal directory: {file_path}")

        # Check the parent folder name
        parts = relative_path.parts
        if not parts:
            raise ValueError(f"Cannot determine entry type for: {file_path}")

        folder = parts[0] if len(parts) > 0 else ""

        # Map folder names to entry types
        folder_mapping = {
            "daily": EntryType.DAILY,
            "projects": EntryType.PROJECT,
            "people": EntryType.PEOPLE,
            "memories": EntryType.MEMORY,
        }

        if folder in folder_mapping:
            return folder_mapping[folder]

        raise ValueError(
            f"Unknown entry type for folder '{folder}'. "
            f"Expected one of: {', '.join(folder_mapping.keys())}"
        )
