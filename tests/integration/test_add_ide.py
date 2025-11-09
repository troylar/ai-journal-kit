"""
Integration tests for add-ide command.

Tests adding IDE configurations to existing journals.
"""

import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from tests.integration.fixtures.journal_factory import create_journal_fixture


@pytest.mark.integration
def test_add_ide_cursor_to_existing_journal(temp_journal_dir, isolated_config):
    """Test adding Cursor IDE config to existing journal."""
    # Create journal with Windsurf initially
    create_journal_fixture(path=temp_journal_dir, ide="windsurf", config_dir=isolated_config)

    # Add Cursor IDE
    runner = CliRunner()
    result = runner.invoke(app, ["add-ide", "cursor"])

    # Should succeed
    assert result.exit_code == 0
    assert "cursor" in result.output.lower()

    # Verify Cursor config was added
    cursor_dir = temp_journal_dir / ".cursor" / "rules"
    assert cursor_dir.exists()
    assert len(list(cursor_dir.glob("*.mdc"))) > 0

    # Verify original Windsurf config still exists
    windsurf_dir = temp_journal_dir / ".windsurf" / "rules"
    assert windsurf_dir.exists()


@pytest.mark.integration
def test_add_ide_windsurf_to_existing_journal(temp_journal_dir, isolated_config):
    """Test adding Windsurf IDE config to existing journal."""
    # Create journal with Cursor initially
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Add Windsurf IDE
    runner = CliRunner()
    result = runner.invoke(app, ["add-ide", "windsurf"])

    # Should succeed
    assert result.exit_code == 0
    assert "windsurf" in result.output.lower()

    # Verify Windsurf config was added
    windsurf_dir = temp_journal_dir / ".windsurf" / "rules"
    assert windsurf_dir.exists()
    assert len(list(windsurf_dir.glob("*.md"))) > 0


@pytest.mark.integration
def test_add_ide_claude_code_to_existing_journal(temp_journal_dir, isolated_config):
    """Test adding Claude Code IDE config to existing journal."""
    # Create journal with Cursor initially
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Add Claude Code IDE
    runner = CliRunner()
    result = runner.invoke(app, ["add-ide", "claude-code"])

    # Should succeed
    assert result.exit_code == 0
    assert "claude code" in result.output.lower()

    # Verify Claude Code config was added
    claude_file = temp_journal_dir / "CLAUDE.md"
    assert claude_file.exists()


@pytest.mark.integration
def test_add_ide_copilot_to_existing_journal(temp_journal_dir, isolated_config):
    """Test adding GitHub Copilot IDE config to existing journal."""
    # Create journal with Cursor initially
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Add Copilot IDE
    runner = CliRunner()
    result = runner.invoke(app, ["add-ide", "copilot"])

    # Should succeed
    assert result.exit_code == 0
    assert "copilot" in result.output.lower()

    # Verify Copilot config was added
    github_dir = temp_journal_dir / ".github" / "instructions"
    assert github_dir.exists()
    assert len(list(github_dir.glob("*.md"))) > 0


@pytest.mark.integration
def test_add_ide_all_to_existing_journal(temp_journal_dir, isolated_config):
    """Test adding all IDE configs to existing journal."""
    # Create journal with just Cursor initially
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Add all IDEs
    runner = CliRunner()
    result = runner.invoke(app, ["add-ide", "all"])

    # Should succeed
    assert result.exit_code == 0

    # Verify all IDE configs were added
    assert (temp_journal_dir / ".cursor" / "rules").exists()
    assert (temp_journal_dir / ".windsurf" / "rules").exists()
    assert (temp_journal_dir / "CLAUDE.md").exists()
    assert (temp_journal_dir / ".github" / "instructions").exists()


@pytest.mark.integration
def test_add_ide_fails_without_journal_setup(temp_journal_dir, isolated_config):
    """Test add-ide fails when journal not set up."""
    # Don't create journal
    runner = CliRunner()
    result = runner.invoke(app, ["add-ide", "cursor"])

    # Should fail with exit code 1
    assert result.exit_code == 1
    assert "not set up" in result.output.lower()


@pytest.mark.integration
def test_add_ide_fails_with_invalid_ide(temp_journal_dir, isolated_config):
    """Test add-ide fails with invalid IDE name."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Try to add invalid IDE
    runner = CliRunner()
    result = runner.invoke(app, ["add-ide", "invalid-ide"])

    # Should fail
    assert result.exit_code == 1
    assert "invalid" in result.output.lower()


@pytest.mark.integration
def test_add_ide_idempotent(temp_journal_dir, isolated_config):
    """Test add-ide is idempotent (can run multiple times safely)."""
    # Create journal with Cursor
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Add Cursor again
    runner = CliRunner()
    result1 = runner.invoke(app, ["add-ide", "cursor"])
    assert result1.exit_code == 0

    # Add Cursor a third time - should still succeed
    result2 = runner.invoke(app, ["add-ide", "cursor"])
    assert result2.exit_code == 0

    # Config should still exist and be valid
    cursor_dir = temp_journal_dir / ".cursor" / "rules"
    assert cursor_dir.exists()


@pytest.mark.integration
def test_add_ide_preserves_journal_content(temp_journal_dir, isolated_config):
    """Test add-ide doesn't modify journal content."""
    # Create journal
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)

    # Add some journal content
    daily_entry = temp_journal_dir / "daily" / "2025-01-15-wednesday.md"
    daily_entry.write_text("# My Journal Entry\n\nToday was great!")

    # Add new IDE
    runner = CliRunner()
    result = runner.invoke(app, ["add-ide", "windsurf"])
    assert result.exit_code == 0

    # Verify journal content unchanged
    assert daily_entry.exists()
    assert "My Journal Entry" in daily_entry.read_text(encoding="utf-8")
    assert "Today was great!" in daily_entry.read_text(encoding="utf-8")
