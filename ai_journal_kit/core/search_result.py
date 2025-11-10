"""Search result models and data structures for journal search functionality.

This module provides Pydantic models for search queries, results, and result sets,
enabling type-safe search operations across journal entries.

Issue: #6 - Search & Filter Enhancement
"""

from datetime import date
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class EntryType(str, Enum):
    """Enumeration of journal entry types."""

    DAILY = "daily"
    PROJECT = "project"
    PEOPLE = "people"
    MEMORY = "memory"

    @classmethod
    def from_string(cls, value: str) -> "EntryType":
        """
        Parse entry type from string, case-insensitive.

        Args:
            value: String value to parse (e.g., "daily", "Daily", "DAILY")

        Returns:
            EntryType enum value

        Raises:
            ValueError: If value is not a valid entry type

        Examples:
            >>> EntryType.from_string("daily")
            EntryType.DAILY
            >>> EntryType.from_string("PROJECT")
            EntryType.PROJECT
        """
        try:
            return cls(value.lower())
        except ValueError:
            valid_types = ", ".join(t.value for t in cls)
            raise ValueError(f"Invalid entry type: '{value}'. Valid types: {valid_types}")

    def to_folder_name(self) -> str:
        """
        Get the folder name for this entry type.

        Returns:
            Folder name as string

        Examples:
            >>> EntryType.DAILY.to_folder_name()
            'daily'
            >>> EntryType.MEMORY.to_folder_name()
            'memories'
        """
        # Handle plural forms
        if self == EntryType.MEMORY:
            return "memories"
        elif self == EntryType.PROJECT:
            return "projects"
        elif self == EntryType.PEOPLE:
            return "people"
        else:
            return self.value

    def display_name(self) -> str:
        """
        Get human-readable display name.

        Returns:
            Capitalized display name

        Examples:
            >>> EntryType.DAILY.display_name()
            'Daily'
            >>> EntryType.PROJECT.display_name()
            'Project'
        """
        return self.value.capitalize()


class SearchQuery(BaseModel):
    """Search query with filters and validation."""

    search_text: str = Field(..., min_length=1, description="The text pattern to search for")
    date_after: date | None = Field(None, description="Filter results after this date")
    date_before: date | None = Field(None, description="Filter results before this date")
    entry_types: list[EntryType] = Field(
        default_factory=lambda: list(EntryType), description="Filter by entry types"
    )
    cross_reference: str | None = Field(None, description="Search for cross-references")
    case_sensitive: bool = Field(False, description="Enable case-sensitive search")
    limit: int | None = Field(None, gt=0, description="Maximum number of results")

    @field_validator("date_before")
    @classmethod
    def validate_date_range(cls, v: date | None, info) -> date | None:
        """Ensure date_after <= date_before."""
        if v and "date_after" in info.data and info.data["date_after"]:
            if info.data["date_after"] > v:
                raise ValueError("date_after must be <= date_before")
        return v

    @field_validator("entry_types")
    @classmethod
    def validate_entry_types(cls, v: list[EntryType]) -> list[EntryType]:
        """Ensure at least one entry type."""
        if not v:
            return list(EntryType)
        return v


class SearchResult(BaseModel):
    """Single search result with context."""

    file_path: Path
    entry_type: EntryType
    entry_date: date | None
    line_number: int = Field(..., gt=0)
    matched_line: str
    context_before: list[str] = Field(default_factory=list)
    context_after: list[str] = Field(default_factory=list)
    match_positions: list[tuple[int, int]] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @property
    def display_date(self) -> str:
        """Format date for display."""
        return self.entry_date.strftime("%B %d, %Y") if self.entry_date else "No date"

    def format_display(self, highlight: bool = True) -> str:
        """
        Format result for terminal display with Rich.

        Args:
            highlight: Whether to highlight matches

        Returns:
            Formatted string ready for Rich console
        """
        lines = []

        # Header with file path and line number
        lines.append(f"📄 {self.file_path.name}:{self.line_number}")
        lines.append(f"📅 {self.display_date}")
        lines.append("")

        # Context before
        start_line = self.line_number - len(self.context_before)
        for i, ctx_line in enumerate(self.context_before):
            lines.append(f"   {start_line + i}│ {ctx_line}")

        # Matched line (highlighted)
        lines.append(f" → {self.line_number}│ {self.matched_line}")

        # Context after
        for i, ctx_line in enumerate(self.context_after, start=1):
            lines.append(f"   {self.line_number + i}│ {ctx_line}")

        lines.append("")
        return "\n".join(lines)

    def get_context(self, lines_before: int = 2, lines_after: int = 2) -> str:
        """
        Get context as formatted string.

        Args:
            lines_before: Number of context lines before match
            lines_after: Number of context lines after match

        Returns:
            Multi-line string with context
        """
        context_lines = (
            self.context_before[-lines_before:]
            + [self.matched_line]
            + self.context_after[:lines_after]
        )
        return "\n".join(context_lines)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "file_path": self.file_path.as_posix(),
            "entry_type": self.entry_type.value,
            "entry_date": self.entry_date.isoformat() if self.entry_date else None,
            "line_number": self.line_number,
            "matched_line": self.matched_line,
            "context_before": self.context_before,
            "context_after": self.context_after,
        }


class SearchResultSet(BaseModel):
    """Collection of search results with metadata."""

    results: list[SearchResult]
    query: SearchQuery
    total_count: int
    execution_time_ms: float
    files_scanned: int

    class Config:
        arbitrary_types_allowed = True

    @property
    def is_empty(self) -> bool:
        """Check if result set is empty."""
        return self.total_count == 0

    @property
    def result_summary(self) -> str:
        """Get human-readable summary."""
        file_count = len(set(r.file_path for r in self.results))
        return f"{self.total_count} results in {file_count} files ({self.execution_time_ms:.0f}ms)"

    def sort_by_date(self, descending: bool = True) -> "SearchResultSet":
        """
        Sort results chronologically.

        Args:
            descending: Sort newest first (True) or oldest first (False)

        Returns:
            New SearchResultSet with sorted results
        """
        sorted_results = sorted(
            self.results, key=lambda r: r.entry_date or date.min, reverse=descending
        )
        return SearchResultSet(
            results=sorted_results,
            query=self.query,
            total_count=self.total_count,
            execution_time_ms=self.execution_time_ms,
            files_scanned=self.files_scanned,
        )

    def export_to_markdown(self, output_path: Path) -> None:
        """
        Export results to markdown file.

        Args:
            output_path: Path where markdown file will be written

        Raises:
            IOError: If file cannot be written
        """
        from datetime import datetime

        lines = []
        lines.append("# Search Results")
        lines.append("")
        lines.append(f'**Query**: "{self.query.search_text}"')

        # Add filter information
        filters = []
        if self.query.date_after:
            filters.append(f"After {self.query.date_after}")
        if self.query.date_before:
            filters.append(f"Before {self.query.date_before}")
        if self.query.entry_types and len(self.query.entry_types) < len(EntryType):
            types = ", ".join(t.value for t in self.query.entry_types)
            filters.append(f"Types: {types}")

        if filters:
            lines.append(f"**Filters**: {', '.join(filters)}")

        lines.append(
            f"**Results**: {self.total_count} matches in {len(set(r.file_path for r in self.results))} files"
        )
        lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Add each result
        for result in self.results:
            lines.append(f"## {result.file_path.name} (Line {result.line_number})")
            lines.append("")
            lines.append(f"**Date**: {result.display_date}")
            lines.append("")
            lines.append("### Context")
            lines.append("")
            lines.append("```markdown")
            lines.append(result.get_context())
            lines.append("```")
            lines.append("")
            lines.append("---")
            lines.append("")

        output_path.write_text("\n".join(lines))

    def filter_by_type(self, entry_type: EntryType) -> "SearchResultSet":
        """
        Further filter results by entry type.

        Args:
            entry_type: Entry type to filter by

        Returns:
            New SearchResultSet with filtered results
        """
        filtered_results = [r for r in self.results if r.entry_type == entry_type]
        return SearchResultSet(
            results=filtered_results,
            query=self.query,
            total_count=len(filtered_results),
            execution_time_ms=self.execution_time_ms,
            files_scanned=self.files_scanned,
        )

    def group_by_file(self) -> dict[Path, list[SearchResult]]:
        """
        Group results by source file.

        Returns:
            Dictionary mapping file paths to lists of results
        """
        grouped: dict[Path, list[SearchResult]] = {}
        for result in self.results:
            if result.file_path not in grouped:
                grouped[result.file_path] = []
            grouped[result.file_path].append(result)
        return grouped
