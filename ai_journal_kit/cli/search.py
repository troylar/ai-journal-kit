"""Search command for AI Journal Kit CLI.

This module implements the search command for finding journal entries
using text search and filters.

Issue: #6 - Search & Filter Enhancement
"""

import os
from datetime import date
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from ai_journal_kit.core.config import load_config
from ai_journal_kit.core.date_utils import parse_date
from ai_journal_kit.core.search_engine import SearchEngine
from ai_journal_kit.core.search_result import EntryType, SearchQuery
from ai_journal_kit.utils.ui import console, error_console, show_error, show_success

# Typer app for search command
app = typer.Typer()


def search(
    query: str = typer.Argument(..., help="Text to search for in journal entries"),
    after: Optional[str] = typer.Option(
        None,
        "--after",
        help="Filter results after date (YYYY-MM-DD or relative like '7d')",
    ),
    before: Optional[str] = typer.Option(
        None,
        "--before",
        help="Filter results before date (YYYY-MM-DD)",
    ),
    type: Optional[str] = typer.Option(
        None,
        "--type",
        help="Filter by entry type: daily, project, people, memory (comma-separated)",
    ),
    ref: Optional[str] = typer.Option(
        None,
        "--ref",
        help="Search for cross-references (e.g., 'people/sarah')",
    ),
    export: Optional[Path] = typer.Option(
        None,
        "--export",
        help="Export results to markdown file",
    ),
    case_sensitive: bool = typer.Option(
        False,
        "--case-sensitive",
        help="Enable case-sensitive search",
    ),
    limit: Optional[int] = typer.Option(
        None,
        "--limit",
        help="Limit results to N matches",
    ),
):
    """
    Search for text in journal entries with optional filters.

    Examples:
        ai-journal-kit search "anxiety"
        ai-journal-kit search "meeting" --after 7d
        ai-journal-kit search "deadline" --type project
        ai-journal-kit search --ref people/sarah
    """
    try:
        # Validate query is not empty
        if not query or not query.strip():
            show_error("Search query cannot be empty")
            raise typer.Exit(1)

        # Get journal path from config
        config = load_config()
        if not config:
            show_error("No journal configuration found. Please run setup first.")
            raise typer.Exit(1)
        journal_path = config.journal_location

        if not journal_path.exists():
            show_error(f"Journal path does not exist: {journal_path}")
            raise typer.Exit(1)

        # Parse date filters
        date_after = None
        date_before = None

        if after:
            try:
                date_after = parse_date(after)
            except ValueError as e:
                show_error(f"Invalid --after date: {e}")
                raise typer.Exit(1)

        if before:
            try:
                date_before = parse_date(before)
            except ValueError as e:
                show_error(f"Invalid --before date: {e}")
                raise typer.Exit(1)

        # Validate date range
        try:
            validate_date_range(date_after, date_before)
        except ValueError as e:
            show_error(str(e))
            raise typer.Exit(1)

        # Parse entry types
        entry_types = None
        if type:
            try:
                entry_types = parse_entry_types(type)
            except ValueError as e:
                show_error(str(e))
                raise typer.Exit(1)

        # Create SearchEngine
        engine = SearchEngine(journal_path)

        # Execute search (cross-reference or regular)
        if ref:
            # Cross-reference search
            try:
                result_set = engine.search_cross_references(
                    reference=ref,
                    entry_types=entry_types,
                    date_after=date_after,
                    date_before=date_before,
                )
            except ValueError as e:
                show_error(f"Invalid cross-reference: {e}")
                raise typer.Exit(1)
        else:
            # Regular text search
            search_query = SearchQuery(
                search_text=query,
                date_after=date_after,
                date_before=date_before,
                entry_types=entry_types or list(EntryType),
                case_sensitive=case_sensitive,
                limit=limit,
            )
            result_set = engine.search(search_query)

        # Display header
        display_search_header(result_set.query, result_set.total_count, result_set.execution_time_ms)

        # Display results
        format_search_results(result_set, console)

        # Export if requested
        if export:
            if confirm_file_overwrite(export):
                try:
                    result_set.export_to_markdown(export)
                    show_success(f"Results exported to {export}")
                except Exception as e:
                    show_error(f"Failed to export results: {e}")
                    raise typer.Exit(1)
            else:
                console.print("[yellow]Export cancelled[/yellow]")

    except typer.Exit:
        raise
    except Exception as e:
        show_error(f"Search failed: {e}")
        raise typer.Exit(1)


def format_search_results(result_set, console: Console) -> None:
    """
    Format and display search results with Rich.

    Args:
        result_set: SearchResultSet to display
        console: Rich Console instance
    """
    if result_set.is_empty:
        console.print("[yellow]No results found[/yellow]")
        return

    # Display each result
    for i, result in enumerate(result_set.results):
        if i > 0:
            console.print("[dim]" + "─" * 80 + "[/dim]")

        # Display result with formatting
        display_text = result.format_display(highlight=True)
        console.print(display_text)


def display_search_header(query: SearchQuery, result_count: int, execution_time: float) -> None:
    """
    Display search header with query and filters.

    Args:
        query: SearchQuery that was executed
        result_count: Number of results found
        execution_time: Execution time in milliseconds
    """
    console.print(f"\n🔍 [bold cyan]Search:[/bold cyan] {query.search_text}")

    # Display filters if any
    filters = []
    if query.date_after:
        filters.append(f"After: {query.date_after}")
    if query.date_before:
        filters.append(f"Before: {query.date_before}")
    if query.entry_types and len(query.entry_types) < len(EntryType):
        type_names = ", ".join(t.display_name() for t in query.entry_types)
        filters.append(f"Types: {type_names}")
    if query.case_sensitive:
        filters.append("Case-sensitive")
    if query.limit:
        filters.append(f"Limit: {query.limit}")

    if filters:
        console.print(f"[dim]Filters: {' | '.join(filters)}[/dim]")

    console.print(f"[bold green]Found {result_count} results[/bold green] [dim]({execution_time:.0f}ms)[/dim]\n")


def parse_entry_types(type_str: str) -> List[EntryType]:
    """
    Parse comma-separated entry types.

    Args:
        type_str: Comma-separated type string (e.g., "daily,project")

    Returns:
        List of EntryType enum values

    Raises:
        ValueError: If any type is invalid
    """
    types = []
    for type_part in type_str.split(","):
        type_part = type_part.strip()
        if type_part:
            try:
                types.append(EntryType.from_string(type_part))
            except ValueError as e:
                raise ValueError(f"Invalid entry type: '{type_part}'. {e}") from e

    if not types:
        raise ValueError("No entry types specified")

    return types


def validate_date_range(
    date_after: Optional[date], date_before: Optional[date]
) -> None:
    """
    Validate that date_after <= date_before.

    Args:
        date_after: After date filter
        date_before: Before date filter

    Raises:
        ValueError: If date_after > date_before
    """
    if date_after and date_before:
        if date_after > date_before:
            raise ValueError(
                f"Invalid date range: --after ({date_after}) cannot be later than --before ({date_before})"
            )


def confirm_file_overwrite(file_path: Path) -> bool:
    """
    Prompt user for confirmation before overwriting file.

    Args:
        file_path: Path to file that might be overwritten

    Returns:
        True if user confirms, False otherwise
    """
    if not file_path.exists():
        return True

    response = typer.confirm(f"File {file_path} already exists. Overwrite?")
    return response
