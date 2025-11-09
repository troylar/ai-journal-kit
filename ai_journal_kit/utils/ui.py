"""Rich UI helpers for beautiful CLI output."""

import sys
from collections.abc import Callable

import questionary
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table

# Ensure UTF-8 encoding for Windows compatibility with Unicode characters
# On Windows, force UTF-8 to handle emojis and special characters in templates
_console_kwargs = {}
if sys.platform == "win32":
    # Reconfigure stdout/stderr to use UTF-8 on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

console = Console(**_console_kwargs)
error_console = Console(stderr=True, **_console_kwargs)


def ask_path(prompt: str, default: str = "~/journal") -> str:
    """Ask user for filesystem path."""
    return Prompt.ask(f"[bold cyan]{prompt}[/bold cyan]", default=default)


def ask_ide(prompt: str = "Which AI editor do you use?") -> str:
    """Ask user for IDE preference with visual selector."""
    choices = [
        "Cursor",
        "Windsurf",
        "Claude Code (Cline)",
        "GitHub Copilot",
        "All of the above",
    ]

    answer = questionary.select(prompt, choices=choices, default="Cursor").ask()

    # Map display names back to internal names
    ide_map = {
        "Cursor": "cursor",
        "Windsurf": "windsurf",
        "Claude Code (Cline)": "claude-code",
        "GitHub Copilot": "copilot",
        "All of the above": "all",
    }

    return ide_map[answer]


def ask_framework(prompt: str = "Which journaling framework would you like to use?") -> str:
    """Ask user for framework preference with visual selector."""
    choices = [
        "Default (flexible)",
        "GTD (Getting Things Done)",
        "PARA (Projects, Areas, Resources, Archive)",
        "Bullet Journal",
        "Zettelkasten (knowledge management)",
    ]

    answer = questionary.select(prompt, choices=choices, default="Default (flexible)").ask()

    # Map display names back to internal names
    framework_map = {
        "Default (flexible)": "default",
        "GTD (Getting Things Done)": "gtd",
        "PARA (Projects, Areas, Resources, Archive)": "para",
        "Bullet Journal": "bullet-journal",
        "Zettelkasten (knowledge management)": "zettelkasten",
    }

    return framework_map[answer]


def confirm(prompt: str) -> bool:
    """Ask user for confirmation."""
    return Confirm.ask(f"[yellow]{prompt}[/yellow]")


def show_progress(tasks: list[tuple[str, Callable]]):
    """Execute tasks with progress bar."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        for description, func in tasks:
            task = progress.add_task(description, total=None)
            func()
            progress.update(task, completed=True)


def show_table(title: str, columns: list[tuple[str, str]], rows: list[list[str]]):
    """Display data as a Rich table.

    Args:
        title: Table title
        columns: List of (column_name, style) tuples
        rows: List of row data (each row is list of strings)
    """
    table = Table(title=title, show_header=True)
    for col_name, style in columns:
        table.add_column(col_name, style=style)

    for row in rows:
        table.add_row(*row)

    console.print(table)


def show_panel(content: str, title: str = "", border_style: str = "blue"):
    """Display content in a Rich panel."""
    panel = Panel(content, title=title, border_style=border_style)
    console.print(panel)


def show_error(message: str, suggestion: str = ""):
    """Display error message with optional suggestion."""
    error_console.print(f"\n[bold red]Error:[/bold red] [red]{message}[/red]")
    if suggestion:
        error_console.print(f"[yellow]💡 Suggestion: {suggestion}[/yellow]\n")


def show_success(message: str):
    """Display success message."""
    console.print(f"[green]✨ {message}[/green]")


def show_markdown(markdown_text: str):
    """Render markdown with Rich."""
    md = Markdown(markdown_text)
    console.print(md)
