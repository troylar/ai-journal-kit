"""
Helper functions for journal validation in integration tests.

Provides assertion helpers to validate journal structure, IDE configs,
and configuration files.
"""

from pathlib import Path

from ai_journal_kit.core.journal import REQUIRED_FOLDERS


def assert_journal_structure_valid(journal_path: Path) -> None:
    """
    Assert that journal has all required folders.

    Args:
        journal_path: Path to journal directory

    Raises:
        AssertionError: If any required folder is missing
    """
    assert journal_path.exists(), f"Journal path does not exist: {journal_path}"
    assert journal_path.is_dir(), f"Journal path is not a directory: {journal_path}"

    for folder in REQUIRED_FOLDERS:
        folder_path = journal_path / folder
        assert folder_path.exists(), f"Required folder missing: {folder}"
        assert folder_path.is_dir(), f"Required folder is not a directory: {folder}"


def assert_ide_config_installed(journal_path: Path, ide: str) -> None:
    """
    Assert that IDE configuration is installed correctly.

    Args:
        journal_path: Path to journal directory
        ide: IDE name (cursor, windsurf, claude-code, copilot, all)

    Raises:
        AssertionError: If IDE config is not installed correctly
    """
    ide_checks = {
        "cursor": journal_path / ".cursor" / "rules",
        "windsurf": journal_path / ".windsurf" / "rules",
        "claude-code": journal_path / "SYSTEM-PROTECTION.md",  # Claude Code uses this file
        "copilot": journal_path / ".github" / "instructions",
    }

    if ide == "all":
        # Check all IDEs are installed
        for ide_name, check_path in ide_checks.items():
            assert check_path.exists(), f"{ide_name} config not installed: {check_path}"
    else:
        # Check specific IDE
        check_path = ide_checks.get(ide)
        assert check_path is not None, f"Unknown IDE: {ide}"
        assert check_path.exists(), f"{ide} config not installed: {check_path}"


def assert_config_valid(
    config_path: Path, expected_journal: Path = None, expected_ide: str = None
) -> None:
    """
    Assert that config file exists and contains valid configuration.

    Args:
        config_path: Path to config file
        expected_journal: Optional expected journal location
        expected_ide: Optional expected IDE value

    Raises:
        AssertionError: If config is invalid or doesn't match expected values
    """
    assert config_path.exists(), f"Config file does not exist: {config_path}"

    # Try to load config
    import json

    try:
        with open(config_path) as f:
            config_data = json.load(f)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Config file contains invalid JSON: {e}")

    # Validate required fields
    assert "journal_location" in config_data, "Config missing 'journal_location' field"
    assert "ide" in config_data, "Config missing 'ide' field"

    # Check expected values if provided
    if expected_journal:
        config_journal = Path(config_data["journal_location"])
        assert config_journal == expected_journal, (
            f"Config journal location mismatch: {config_journal} != {expected_journal}"
        )

    if expected_ide:
        assert config_data["ide"] == expected_ide, (
            f"Config IDE mismatch: {config_data['ide']} != {expected_ide}"
        )


def assert_template_exists(journal_path: Path, template_name: str) -> None:
    """
    Assert that a specific template file exists in journal.

    Args:
        journal_path: Path to journal directory
        template_name: Name of template file to check

    Raises:
        AssertionError: If template does not exist
    """
    template_path = journal_path / template_name
    assert template_path.exists(), f"Template does not exist: {template_name}"
    assert template_path.is_file(), f"Template is not a file: {template_name}"


def count_markdown_files(directory: Path) -> int:
    """
    Count markdown files in a directory.

    Args:
        directory: Path to directory

    Returns:
        int: Number of .md files in directory
    """
    if not directory.exists():
        return 0

    return len(list(directory.glob("*.md")))
