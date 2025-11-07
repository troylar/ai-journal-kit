"""Shared pytest fixtures for all tests."""

from pathlib import Path

import pytest
from typer.testing import CliRunner


@pytest.fixture
def temp_journal(tmp_path: Path) -> Path:
    """Create temporary journal directory."""
    journal = tmp_path / "journal"
    journal.mkdir()
    return journal


@pytest.fixture
def mock_config(temp_journal: Path):
    """Create mock configuration."""
    from ai_journal_kit.core.config import Config

    return Config(journal_location=temp_journal, ide="cursor")


@pytest.fixture
def cli_runner():
    """Create Typer CLI test runner."""
    return CliRunner()
