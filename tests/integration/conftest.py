"""
Integration test fixtures and configuration.

Provides shared fixtures for integration tests that test CLI commands
with real file I/O in isolated temporary directories.
"""

import os

import pytest


@pytest.fixture
def temp_journal_dir(tmp_path):
    """
    Provide isolated temporary directory for journal.

    Args:
        tmp_path: pytest's built-in tmp_path fixture

    Returns:
        Path: Temporary directory for journal installation
    """
    journal_dir = tmp_path / "test-journal"
    journal_dir.mkdir()
    return journal_dir


@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    """
    Isolate config file location for test.

    Sets AI_JOURNAL_CONFIG_DIR environment variable to temporary location
    to prevent tests from interfering with user's actual configuration.

    Args:
        tmp_path: pytest's built-in tmp_path fixture
        monkeypatch: pytest's monkeypatch fixture

    Returns:
        Path: Temporary config directory
    """
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(config_dir))

    # Force reload of config module to pick up environment variable
    from importlib import reload

    from ai_journal_kit.core import config as config_module

    reload(config_module)

    return config_dir


@pytest.fixture
def isolated_env(tmp_path, monkeypatch):
    """
    Provide isolated environment variables for e2e tests.

    Args:
        tmp_path: pytest's built-in tmp_path fixture
        monkeypatch: pytest's monkeypatch fixture

    Returns:
        dict: Environment variables for subprocess calls
    """
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    env = os.environ.copy()
    env["AI_JOURNAL_CONFIG_DIR"] = str(config_dir)

    return env


@pytest.fixture(autouse=True)
def reset_config_after_test():
    """
    Ensure config module is reset after each test.

    This prevents config state from leaking between tests.
    """
    yield

    # Reload config module to reset any cached state
    from importlib import reload

    from ai_journal_kit.core import config as config_module

    reload(config_module)
