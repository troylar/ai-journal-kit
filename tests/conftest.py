"""
Shared pytest fixtures for ai-journal-kit testing.

This module provides reusable fixtures for unit and integration tests.
"""

import json
import shutil
import subprocess
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def temp_journal_dir() -> Generator[Path, None, None]:
    """Create a temporary journal directory for testing.

    Yields:
        Path: Temporary directory that will be cleaned up after test
    """
    temp_dir = tempfile.mkdtemp(prefix="ai-journal-test-")
    yield Path(temp_dir)
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_config(temp_journal_dir: Path) -> Generator[Path, None, None]:
    """Create a mock configuration file for testing.

    Args:
        temp_journal_dir: Temporary journal directory fixture

    Yields:
        Path: Path to mock config file that will be cleaned up after test
    """
    config_dir = Path(tempfile.gettempdir()) / ".ai-journal-kit-test"
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.json"

    config_data = {"journal_location": str(temp_journal_dir), "ide": "cursor"}

    config_file.write_text(json.dumps(config_data, indent=2))
    yield config_file

    # Cleanup
    if config_file.exists():
        config_file.unlink()
    if config_dir.exists() and not any(config_dir.iterdir()):
        config_dir.rmdir()


@pytest.fixture
def isolated_config_dir() -> Generator[Path, None, None]:
    """Create an isolated configuration directory for testing.

    This fixture ensures tests don't interfere with the user's actual config.

    Yields:
        Path: Isolated config directory that will be cleaned up after test
    """
    config_dir = Path(tempfile.mkdtemp(prefix="ai-journal-config-test-"))
    yield config_dir
    # Cleanup
    shutil.rmtree(config_dir, ignore_errors=True)


def run_cli_command(*args, input_text: str = "", **kwargs) -> subprocess.CompletedProcess:
    """Helper function to run CLI commands in isolated subprocess for integration testing.

    Args:
        *args: Command arguments to pass to the CLI
        input_text: Optional stdin input for interactive commands
        **kwargs: Additional arguments to pass to subprocess.run

    Returns:
        subprocess.CompletedProcess: Result of the command execution

    Example:
        >>> result = run_cli_command("status")
        >>> assert result.returncode == 0
    """
    cmd = ["python", "-m", "ai_journal_kit"] + list(args)
    return subprocess.run(cmd, input=input_text, text=True, capture_output=True, **kwargs)
