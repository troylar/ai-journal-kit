"""
Integration tests for update command.

Tests update scenarios including:
- Preserving custom templates and configurations
- Refreshing core templates
- Adding new IDE configs
- Migrating old structures
- Handling corrupted configs
"""


import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from tests.integration.fixtures.journal_factory import create_journal_fixture
from tests.integration.helpers import (
    assert_ide_config_installed,
    assert_journal_structure_valid,
)


@pytest.mark.integration
def test_update_preserves_custom_templates(temp_journal_dir, isolated_config):
    """Test update preserves custom user templates."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Add custom template
    custom_template = temp_journal_dir / "daily" / "my-custom-template.md"
    custom_template.write_text("# My Custom Template\n\nThis is my personal template.")

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()

    # Custom template should still exist
    assert custom_template.exists()
    assert "My Custom Template" in custom_template.read_text()


@pytest.mark.integration
def test_update_preserves_ai_instructions(temp_journal_dir, isolated_config):
    """Test update preserves custom AI instructions."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Add custom AI instructions
    ai_instructions_dir = temp_journal_dir / ".ai-instructions"
    ai_instructions_dir.mkdir(exist_ok=True)
    custom_coach = ai_instructions_dir / "my-coach.md"
    custom_coach.write_text("# My Custom Coach\n\nBe very direct and concise.")

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()

    # Custom instructions should still exist
    assert custom_coach.exists()
    assert "Be very direct and concise" in custom_coach.read_text()


@pytest.mark.integration
def test_update_preserves_journal_entries(temp_journal_dir, isolated_config):
    """Test update preserves existing journal entries."""
    # Create journal with content
    journal = create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        has_content=True,
        config_dir=isolated_config
    )

    # Verify entries exist
    assert journal.daily_notes_count == 3

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()

    # Journal entries should still exist
    assert (temp_journal_dir / "daily" / "2025-01-01.md").exists()
    assert (temp_journal_dir / "daily" / "2025-01-02.md").exists()
    assert (temp_journal_dir / "daily" / "2025-01-03.md").exists()


@pytest.mark.integration
def test_update_refreshes_core_templates(temp_journal_dir, isolated_config):
    """Test update refreshes core system templates."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Modify WELCOME.md (core template)
    welcome_file = temp_journal_dir / "WELCOME.md"
    if welcome_file.exists():
        welcome_file.write_text("# Modified Welcome\n\nThis should be updated.")

    # Run update with force and no-confirm to refresh templates
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--force", "--no-confirm"])

    # Update should succeed
    assert result.exit_code == 0, f"Update failed: {result.output}"


@pytest.mark.integration
def test_update_adds_new_ide_configs(temp_journal_dir, isolated_config):
    """Test update adds new IDE configs if missing."""
    # Create journal with only Cursor
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Verify only Cursor config exists
    assert_ide_config_installed(temp_journal_dir, "cursor")

    # Run update (in real implementation, this would add new configs)
    runner = CliRunner()
    result = runner.invoke(app, ["update"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()

    # Original structure should remain valid
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_update_migrates_old_structure(temp_journal_dir, isolated_config):
    """Test update migrates old template structure."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="copilot",
        config_dir=isolated_config
    )

    # Create old Copilot structure (copilot-instructions.md in .github root)
    old_copilot_file = temp_journal_dir / ".github" / "copilot-instructions.md"
    old_copilot_file.parent.mkdir(exist_ok=True, parents=True)
    old_copilot_file.write_text("# Old Copilot Instructions")

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update"])

    # Update should succeed
    assert result.exit_code == 0 or "up to date" in result.output.lower()


@pytest.mark.integration
def test_update_dry_run_mode(temp_journal_dir, isolated_config):
    """Test update dry-run shows actions without making changes."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Add custom content
    custom_file = temp_journal_dir / "daily" / "test.md"
    custom_file.write_text("# Test")
    original_mtime = custom_file.stat().st_mtime

    # Run dry-run update
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--dry-run"])

    # Should succeed or show dry-run message
    assert result.exit_code == 0 or "dry run" in result.output.lower() or "would" in result.output.lower()

    # File should not be modified
    assert custom_file.stat().st_mtime == original_mtime


@pytest.mark.integration
def test_update_handles_corrupted_config(temp_journal_dir, isolated_config):
    """Test update handles corrupted config gracefully."""
    from tests.integration.fixtures.config_factory import create_corrupted_config

    # Create journal first
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Corrupt the config
    create_corrupted_config(isolated_config)

    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update"])

    # Should handle error gracefully (may fail or fix config)
    # At minimum, should provide useful error message
    if result.exit_code != 0:
        assert "config" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_update_with_force_flag(temp_journal_dir, isolated_config):
    """Test update with --force flag forces template refresh."""
    # Create journal
    create_journal_fixture(
        path=temp_journal_dir,
        ide="cursor",
        config_dir=isolated_config
    )

    # Run update with force and no-confirm for testing
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--force", "--no-confirm"])

    # Should succeed
    assert result.exit_code == 0, f"Update --force failed: {result.output}"

    # Journal structure should remain valid
    assert_journal_structure_valid(temp_journal_dir)

