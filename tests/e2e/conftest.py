"""
End-to-end test fixtures and configuration.

Provides shared fixtures for e2e tests that execute actual CLI commands
via subprocess to test the complete user experience.
"""

import os

import pytest


@pytest.fixture
def isolated_env(tmp_path):
    """
    Provide isolated environment variables for e2e subprocess tests.

    Args:
        tmp_path: pytest's built-in tmp_path fixture

    Returns:
        dict: Environment variables for subprocess calls
    """
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    env = os.environ.copy()
    env["AI_JOURNAL_CONFIG_DIR"] = str(config_dir)

    # Ensure Python path includes current project
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{os.getcwd()}:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = os.getcwd()

    return env


@pytest.fixture
def temp_journal_dir(tmp_path):
    """
    Provide isolated temporary directory for journal in e2e tests.

    Args:
        tmp_path: pytest's built-in tmp_path fixture

    Returns:
        Path: Temporary directory for journal installation
    """
    journal_dir = tmp_path / "test-journal"
    return journal_dir  # Don't create yet - let command create it
