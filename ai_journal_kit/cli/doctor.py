"""Doctor command for diagnosing and fixing common issues."""

from pathlib import Path

import typer

from ai_journal_kit.core.config import load_config
from ai_journal_kit.core.journal import create_structure, validate_structure
from ai_journal_kit.core.symlinks import create_link, is_broken
from ai_journal_kit.core.templates import copy_ide_configs
from ai_journal_kit.utils.ui import console, show_error, show_success


def doctor(
    fix: bool = typer.Option(False, "--fix", help="Automatically fix issues"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed diagnostics"),
):
    """Diagnose and fix common journal issues.

    Checks:
    - Config file validity
    - Journal structure completeness
    - IDE configurations
    - Symlinks (if used)
    - Permissions
    """
    console.print("[bold]Running diagnostics...[/bold]\n")

    config = load_config()
    if not config:
        show_error("No configuration found", "Run 'ai-journal-kit setup' first")
        raise typer.Exit(1)

    issues = []

    # Check 1: Config file
    _print_check("Config file valid", True, verbose)

    # Check 2: Journal location exists
    journal_exists = config.journal_location.exists()
    _print_check("Journal location exists", journal_exists, verbose)
    if not journal_exists:
        issues.append(("journal_missing", "Journal location does not exist"))

    # Check 3: Journal structure
    structure_valid, missing = validate_structure(config.journal_location)
    _print_check("Journal structure complete", structure_valid, verbose)
    if not structure_valid:
        issues.append(("missing_folders", f"Missing folders: {', '.join(missing)}"))
        if verbose:
            console.print(f"  [dim]Missing: {', '.join(missing)}[/dim]")

    # Check 4: IDE configs
    ide_configs_exist = _check_ide_configs(config)
    _print_check("IDE configurations installed", ide_configs_exist, verbose)
    if not ide_configs_exist:
        issues.append(("missing_ide_configs", f"IDE configs missing for {config.ide}"))

    # Check 5: Symlinks (if applicable)
    if config.use_symlink and config.symlink_source:
        symlink_ok = not is_broken(config.symlink_source)
        _print_check("Symlink valid", symlink_ok, verbose)
        if not symlink_ok:
            issues.append(("broken_symlink", f"Symlink broken: {config.symlink_source}"))

    # Check 6: Permissions
    writable = config.journal_location.exists() and _is_writable(config.journal_location)
    _print_check("Permissions OK", writable, verbose)
    if not writable:
        issues.append(("permissions", "Journal location not writable"))

    console.print()

    # Report results
    if not issues:
        show_success("No issues found! Your journal is healthy.")
        raise typer.Exit(0)

    # Issues found
    console.print(f"[yellow]Found {len(issues)} issue(s).[/yellow]\n")

    if not fix:
        console.print("To automatically fix these issues, run:")
        console.print("  [cyan]ai-journal-kit doctor --fix[/cyan]\n")
        raise typer.Exit(1)

    # Fix mode
    console.print("[bold]Fixing issues...[/bold]\n")
    fixed_count = 0

    for issue_type, description in issues:
        if issue_type == "missing_folders":
            try:
                create_structure(config.journal_location)
                console.print("  [green]✓[/green] Created missing folders")
                fixed_count += 1
            except Exception as e:
                console.print(f"  [red]✗[/red] Failed to create folders: {e}")

        elif issue_type == "missing_ide_configs":
            try:
                copy_ide_configs(config.ide, config.journal_location, framework=config.framework)
                console.print(f"  [green]✓[/green] Installed {config.ide} configurations")
                fixed_count += 1
            except Exception as e:
                console.print(f"  [red]✗[/red] Failed to install IDE configs: {e}")

        elif issue_type == "broken_symlink":
            try:
                create_link(config.journal_location, config.symlink_source)
                console.print("  [green]✓[/green] Recreated symlink")
                fixed_count += 1
            except Exception as e:
                console.print(f"  [red]✗[/red] Failed to recreate symlink: {e}")

        elif issue_type == "journal_missing":
            console.print("  [red]✗[/red] Cannot fix: Journal location doesn't exist")
            console.print("    [dim]Suggestion: Run 'ai-journal-kit move' to relocate[/dim]")

        elif issue_type == "permissions":
            console.print("  [red]✗[/red] Cannot fix: Permission denied")
            console.print(
                "    [dim]Suggestion: Check file permissions or choose different location[/dim]"
            )

    console.print()
    if fixed_count > 0:
        show_success(f"Fixed {fixed_count} issue(s).")
        console.print("\nRun [cyan]'ai-journal-kit doctor'[/cyan] again to verify.\n")
    else:
        console.print("[yellow]Could not automatically fix the issues.[/yellow]")
        console.print("See suggestions above for manual fixes.\n")


def _check_ide_configs(config) -> bool:
    """Check if IDE configs are installed."""
    if config.ide == "cursor":
        return (config.journal_location / ".cursor" / "rules").exists()
    elif config.ide == "windsurf":
        return (config.journal_location / ".windsurf" / "rules").exists()
    elif config.ide == "claude-code":
        return (config.journal_location / "CLAUDE.md").exists()
    elif config.ide == "copilot":
        return (config.journal_location / ".github" / "copilot-instructions.md").exists()
    elif config.ide == "all":
        return True
    return False


def _is_writable(path: Path) -> bool:
    """Check if path is writable."""
    try:
        test_file = path / ".write_test"
        test_file.touch()
        test_file.unlink()
        return True
    except (OSError, PermissionError):
        return False


def _print_check(label: str, passed: bool, verbose: bool):
    """Print a check result."""
    if verbose or not passed:
        icon = "✓" if passed else "✗"
        color = "green" if passed else "red"
        console.print(f"  [{color}]{icon}[/{color}] {label}")
