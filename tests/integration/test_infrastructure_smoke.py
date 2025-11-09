"""
Smoke tests for integration test infrastructure.

These tests verify that the test infrastructure itself works correctly.
"""

import pytest

from tests.integration.fixtures.config_factory import create_config_fixture
from tests.integration.fixtures.journal_factory import create_journal_fixture
from tests.integration.helpers import (
    assert_config_valid,
    assert_ide_config_installed,
    assert_journal_structure_valid,
)


@pytest.mark.integration
def test_temp_journal_dir_fixture(temp_journal_dir):
    """Test that temp_journal_dir fixture creates isolated directory."""
    assert temp_journal_dir.exists()
    assert temp_journal_dir.is_dir()
    assert "test-journal" in str(temp_journal_dir)


@pytest.mark.integration
def test_isolated_config_fixture(isolated_config):
    """Test that isolated_config fixture isolates config location."""
    assert isolated_config.exists()
    assert isolated_config.is_dir()

    # Verify environment variable is set
    import os

    assert "AI_JOURNAL_CONFIG_DIR" in os.environ
    assert os.environ["AI_JOURNAL_CONFIG_DIR"] == str(isolated_config)


@pytest.mark.integration
def test_journal_factory_creates_structure(temp_journal_dir, isolated_config):
    """Test that journal_factory creates complete journal structure."""
    journal = create_journal_fixture(
        path=temp_journal_dir, ide="cursor", has_content=False, config_dir=isolated_config
    )

    # Verify journal created
    assert journal.path.exists()
    assert journal.ide == "cursor"

    # Verify structure
    assert_journal_structure_valid(journal.path)

    # Verify IDE config
    assert_ide_config_installed(journal.path, "cursor")


@pytest.mark.integration
def test_journal_factory_with_content(temp_journal_dir):
    """Test that journal_factory can create sample content."""
    journal = create_journal_fixture(path=temp_journal_dir, ide="cursor", has_content=True)

    # Verify content was created
    assert journal.daily_notes_count == 3
    assert (journal.daily_dir / "2025-01-01.md").exists()
    assert (journal.daily_dir / "2025-01-02.md").exists()
    assert (journal.daily_dir / "2025-01-03.md").exists()


@pytest.mark.integration
def test_config_factory_creates_config(temp_journal_dir, isolated_config):
    """Test that config_factory creates valid config."""
    config = create_config_fixture(
        journal_location=temp_journal_dir,
        ide="windsurf",
        version="1.0.0",
        config_dir=isolated_config,
    )

    # Verify config created
    assert config.journal_location == temp_journal_dir
    assert config.ide == "windsurf"

    # Verify config file saved
    config_file = isolated_config / "config.json"
    assert_config_valid(config_file, expected_journal=temp_journal_dir, expected_ide="windsurf")


@pytest.mark.integration
def test_assert_journal_structure_valid_detects_missing_folders(temp_journal_dir):
    """Test that assert_journal_structure_valid detects missing folders."""
    # Create incomplete journal (missing folders)
    temp_journal_dir.mkdir(exist_ok=True)
    (temp_journal_dir / "daily").mkdir()

    # Should fail because other folders are missing
    with pytest.raises(AssertionError, match="Required folder missing"):
        assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_assert_ide_config_installed_detects_missing_config(temp_journal_dir):
    """Test that assert_ide_config_installed detects missing IDE configs."""
    temp_journal_dir.mkdir(exist_ok=True)

    # Should fail because cursor config is not installed
    with pytest.raises(AssertionError, match="cursor config not installed"):
        assert_ide_config_installed(temp_journal_dir, "cursor")


@pytest.mark.integration
def test_helpers_module_imports():
    """Test that all helper functions are importable."""
    from tests.integration.helpers import (
        assert_config_valid,
        assert_ide_config_installed,
        assert_journal_structure_valid,
        assert_template_exists,
        count_markdown_files,
    )

    # All imports successful
    assert callable(assert_journal_structure_valid)
    assert callable(assert_ide_config_installed)
    assert callable(assert_config_valid)
    assert callable(assert_template_exists)
    assert callable(count_markdown_files)
