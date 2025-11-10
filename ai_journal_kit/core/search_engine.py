"""Search engine core functionality.

This module implements the main search engine for journal entries,
coordinating file scanning, text search, and result aggregation.

Issue: #6 - Search & Filter Enhancement
"""

import re
import time
from collections import deque
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

from ai_journal_kit.core.date_utils import extract_date_from_filename
from ai_journal_kit.core.file_scanner import FileScanner
from ai_journal_kit.core.search_result import (
    EntryType,
    SearchQuery,
    SearchResult,
    SearchResultSet,
)

# Wiki-link pattern for cross-reference detection
WIKILINK_PATTERN = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'


class SearchEngine:
    """Main search engine class coordinating file scanning and search."""

    def __init__(self, journal_path: Path) -> None:
        """
        Initialize search engine for a journal.

        Args:
            journal_path: Absolute path to journal directory

        Raises:
            ValueError: If journal_path doesn't exist or isn't a directory
            PermissionError: If journal_path isn't readable
        """
        if not journal_path.exists():
            raise ValueError(f"Journal path does not exist: {journal_path}")
        if not journal_path.is_dir():
            raise ValueError(f"Journal path is not a directory: {journal_path}")

        # Check readability
        try:
            list(journal_path.iterdir())
        except PermissionError as e:
            raise PermissionError(f"Journal path is not readable: {journal_path}") from e

        self.journal_path = journal_path.resolve()
        self.file_scanner = FileScanner(journal_path)

    def search(self, query: SearchQuery) -> SearchResultSet:
        """
        Execute search query across journal entries.

        Args:
            query: SearchQuery object with search criteria

        Returns:
            SearchResultSet containing all matching results

        Raises:
            ValueError: If query validation fails
            RuntimeError: If search encounters fatal error
        """
        start_time = time.time()

        # Scan files using FileScanner with query filters
        files = self.file_scanner.scan(
            entry_types=query.entry_types if query.entry_types else None,
            date_after=query.date_after,
            date_before=query.date_before,
        )

        # Search each file for matches
        all_results: List[SearchResult] = []
        for file_path in files:
            file_results = self._search_in_file(
                file_path, query.search_text, query.case_sensitive
            )
            all_results.extend(file_results)

            # Apply limit if specified
            if query.limit and len(all_results) >= query.limit:
                all_results = all_results[: query.limit]
                break

        # Calculate execution time
        execution_time = (time.time() - start_time) * 1000  # Convert to ms

        # Create and return result set
        return SearchResultSet(
            results=all_results,
            query=query,
            total_count=len(all_results),
            execution_time_ms=execution_time,
            files_scanned=len(files),
        )

    def scan_files(
        self,
        entry_types: Optional[List[EntryType]] = None,
        date_after: Optional[date] = None,
        date_before: Optional[date] = None,
    ) -> List[Path]:
        """
        Scan journal directory for matching files.

        Args:
            entry_types: Filter by entry types (None = all types)
            date_after: Include files dated on or after
            date_before: Include files dated on or before

        Returns:
            List of Path objects for matching files

        Notes:
            - Returns absolute paths
            - Date filtering only applies to daily entries
            - Non-existent types are silently ignored
        """
        return self.file_scanner.scan(
            entry_types=entry_types,
            date_after=date_after,
            date_before=date_before,
        )

    def search_cross_references(
        self,
        reference: str,
        entry_types: Optional[List[EntryType]] = None,
        date_after: Optional[date] = None,
        date_before: Optional[date] = None,
    ) -> SearchResultSet:
        """
        Find all entries that reference a specific note.

        Args:
            reference: Reference path (e.g., "people/sarah")
            entry_types: Optional list of entry types to search
            date_after: Optional date filter (after)
            date_before: Optional date filter (before)

        Returns:
            SearchResultSet with entries containing the reference

        Raises:
            ValueError: If reference format is invalid
        """
        # Normalize reference (remove .md extension if present)
        normalized_ref = reference.strip()
        if normalized_ref.endswith(".md"):
            normalized_ref = normalized_ref[:-3]

        if not normalized_ref:
            raise ValueError("Reference cannot be empty")

        # Build search pattern for [[reference]] format
        # Using the actual wiki-link syntax
        search_pattern = f"[[{normalized_ref}"

        # Create SearchQuery
        query = SearchQuery(
            search_text=search_pattern,
            entry_types=entry_types or list(EntryType),
            date_after=date_after,
            date_before=date_before,
        )

        # Execute search and return results
        return self.search(query)

    def _search_in_file(
        self, file_path: Path, pattern: str, case_sensitive: bool = False
    ) -> List[SearchResult]:
        """
        Search for pattern in file and extract context.

        Args:
            file_path: Path to file to search
            pattern: Text pattern to search for (will be escaped)
            case_sensitive: Whether search is case-sensitive

        Returns:
            List of SearchResult objects for matches in this file
        """
        results: List[SearchResult] = []

        # Compile regex with escaped pattern for safety
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(re.escape(pattern), flags)
        except re.error:
            return results

        # Open file with UTF-8 encoding
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except (IOError, OSError):
            return results

        # Get entry metadata
        try:
            entry_type = self.file_scanner.get_entry_type(file_path)
        except ValueError:
            return results

        entry_date = extract_date_from_filename(file_path)

        # Search each line for matches
        for line_idx, line in enumerate(lines):
            line = line.rstrip("\n\r")
            match = regex.search(line)

            if match:
                # Extract context
                context_before, context_after = self._extract_context(lines, line_idx)

                # Get match positions
                match_positions = [(m.start(), m.end()) for m in regex.finditer(line)]

                # Create search result
                result = SearchResult(
                    file_path=file_path,
                    entry_type=entry_type,
                    entry_date=entry_date,
                    line_number=line_idx + 1,  # 1-indexed for display
                    matched_line=line,
                    context_before=[l.rstrip("\n\r") for l in context_before],
                    context_after=[l.rstrip("\n\r") for l in context_after],
                    match_positions=match_positions,
                )
                results.append(result)

        return results

    def _extract_context(
        self, lines: List[str], match_line_idx: int, context_lines: int = 2
    ) -> Tuple[List[str], List[str]]:
        """
        Extract context lines before and after a match.

        Args:
            lines: All lines from the file
            match_line_idx: Index of the matched line (0-based)
            context_lines: Number of context lines before/after

        Returns:
            Tuple of (context_before, context_after) as lists of strings
        """
        # Extract context before (handle start of file)
        start_idx = max(0, match_line_idx - context_lines)
        context_before = lines[start_idx:match_line_idx]

        # Extract context after (handle end of file)
        end_idx = min(len(lines), match_line_idx + context_lines + 1)
        context_after = lines[match_line_idx + 1 : end_idx]

        return (context_before, context_after)

    def _extract_cross_references(self, content: str) -> List[str]:
        """
        Extract all wiki-style cross-references from content.

        Args:
            content: Text content to search

        Returns:
            List of reference paths (e.g., ["people/sarah", "projects/launch"])
        """
        # Use re.findall() with WIKILINK_PATTERN
        matches = re.findall(WIKILINK_PATTERN, content)

        # Strip whitespace from each reference
        references = [ref.strip() for ref in matches]

        return references

    def _apply_date_filter(
        self, file_path: Path, date_after: Optional[date], date_before: Optional[date]
    ) -> bool:
        """
        Check if file passes date filters.

        Args:
            file_path: Path to file
            date_after: Filter for dates on or after
            date_before: Filter for dates on or before

        Returns:
            True if file passes filters, False otherwise
        """
        # Extract date from filename
        file_date = extract_date_from_filename(file_path)

        # If no date found, include the file (non-daily entries)
        if not file_date:
            return True

        # Check date_after constraint
        if date_after and file_date < date_after:
            return False

        # Check date_before constraint
        if date_before and file_date > date_before:
            return False

        # All constraints pass
        return True

    def _apply_type_filter(self, file_path: Path, entry_types: List[EntryType]) -> bool:
        """
        Check if file matches entry type filter.

        Args:
            file_path: Path to file
            entry_types: List of allowed entry types

        Returns:
            True if file matches one of the entry types
        """
        try:
            # Get entry type using FileScanner
            entry_type = self.file_scanner.get_entry_type(file_path)

            # Check if entry_type is in the allowed list
            return entry_type in entry_types
        except ValueError:
            # If entry type cannot be determined, exclude the file
            return False
