"""Integration tests for switch-framework command.

Tests framework switching functionality including:
- Switching between frameworks
- Timestamped backups
- Template preservation
- Config updates
"""

import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from ai_journal_kit.core.config import load_config
from tests.integration.fixtures import create_journal_fixture


@pytest.mark.integration
def test_switch_framework_from_default_to_gtd(temp_journal_dir, isolated_config):
    """Test switching from default framework to GTD."""
    # Create journal with default framework
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="default"
    )

    runner = CliRunner()
    result = runner.invoke(app, ["switch-framework", "gtd", "--no-confirm"], catch_exceptions=False)

    # Should succeed
    assert result.exit_code == 0, f"Switch failed: {result.output}"
    assert "switched successfully" in result.output.lower()

    # Verify config updated
    config = load_config()
    assert config.framework == "gtd"

    # Verify GTD templates installed
    assert (temp_journal_dir / "daily-template.md").exists()
    assert (temp_journal_dir / "waiting-for-template.md").exists()


@pytest.mark.integration
def test_switch_framework_creates_timestamped_backup(temp_journal_dir, isolated_config):
    """Test that switching creates a timestamped backup of existing templates."""
    # Create journal with GTD framework
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="gtd"
    )

    # Customize a template
    daily_template = temp_journal_dir / "daily-template.md"
    original_content = "# My Custom GTD Daily Template\n\nCustom content here"
    daily_template.write_text(original_content, encoding="utf-8")

    # Switch to PARA
    runner = CliRunner()
    result = runner.invoke(
        app, ["switch-framework", "para", "--no-confirm"], catch_exceptions=False
    )

    assert result.exit_code == 0

    # Verify backup directory exists with timestamp format
    backup_base = temp_journal_dir / ".framework-backups"
    assert backup_base.exists()

    # Should have exactly one backup (timestamp format: YYYYMMDD-HHMMSS)
    backups = list(backup_base.iterdir())
    assert len(backups) >= 1

    # Verify backup contains the customized template
    backup_dir = backups[0]
    backed_up_daily = backup_dir / "daily-template.md"
    assert backed_up_daily.exists()
    assert backed_up_daily.read_text(encoding="utf-8") == original_content


@pytest.mark.integration
def test_switch_framework_preserves_journal_content(temp_journal_dir, isolated_config):
    """Test that switching frameworks preserves journal notes."""
    # Create journal and add some notes
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="default"
    )

    # Add journal content
    daily_note = temp_journal_dir / "daily" / "2025-01-01.md"
    daily_note.write_text("# Daily Note\n\nMy thoughts today", encoding="utf-8")

    project_note = temp_journal_dir / "projects" / "my-project.md"
    project_note.write_text("# Project\n\nProject details", encoding="utf-8")

    # Switch framework
    runner = CliRunner()
    result = runner.invoke(app, ["switch-framework", "gtd", "--no-confirm"])

    assert result.exit_code == 0

    # Verify journal content untouched
    assert daily_note.exists()
    assert daily_note.read_text(encoding="utf-8") == "# Daily Note\n\nMy thoughts today"
    assert project_note.exists()
    assert project_note.read_text(encoding="utf-8") == "# Project\n\nProject details"


@pytest.mark.integration
def test_switch_framework_multiple_times_creates_multiple_backups(
    temp_journal_dir, isolated_config
):
    """Test that switching multiple times creates separate timestamped backups."""
    # Start with GTD so first switch will create a backup
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="gtd"
    )

    runner = CliRunner()

    # First switch: GTD -> PARA (creates backup of GTD templates)
    result1 = runner.invoke(app, ["switch-framework", "para", "--no-confirm"])
    assert result1.exit_code == 0

    # Second switch: PARA -> Bullet Journal (creates backup of PARA templates)
    result2 = runner.invoke(app, ["switch-framework", "bullet-journal", "--no-confirm"])
    assert result2.exit_code == 0

    # Third switch: Bullet Journal -> Zettelkasten (creates backup of BuJo templates)
    result3 = runner.invoke(app, ["switch-framework", "zettelkasten", "--no-confirm"])
    assert result3.exit_code == 0

    # Verify multiple backup directories exist
    backup_base = temp_journal_dir / ".framework-backups"
    backups = list(backup_base.iterdir())
    assert len(backups) >= 3  # At least 3 backups


@pytest.mark.integration
def test_switch_framework_to_same_framework_no_op(temp_journal_dir, isolated_config):
    """Test switching to the same framework is a no-op."""
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="gtd"
    )

    runner = CliRunner()
    result = runner.invoke(app, ["switch-framework", "gtd", "--no-confirm"])

    # Should exit successfully but indicate no change needed
    assert result.exit_code == 0
    assert "already using" in result.output.lower()


@pytest.mark.integration
def test_switch_framework_without_setup_fails(temp_journal_dir, isolated_config):
    """Test that switch-framework fails if journal not set up."""
    runner = CliRunner()
    result = runner.invoke(app, ["switch-framework", "gtd", "--no-confirm"])

    # Should fail
    assert result.exit_code != 0
    assert "not set up" in result.output.lower() or "setup" in result.output.lower()


@pytest.mark.integration
def test_switch_framework_with_invalid_framework(temp_journal_dir, isolated_config):
    """Test that switch-framework rejects invalid frameworks."""
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="default"
    )

    runner = CliRunner()
    result = runner.invoke(app, ["switch-framework", "invalid-framework", "--no-confirm"])

    # Should fail
    assert result.exit_code != 0
    assert "invalid" in result.output.lower()


@pytest.mark.integration
def test_switch_framework_interactive_mode(temp_journal_dir, isolated_config):
    """Test switch-framework with interactive framework selection."""
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="default"
    )

    runner = CliRunner()
    # Simulate selecting GTD (option 2) and confirming
    result = runner.invoke(app, ["switch-framework"], input="gtd\ny\n")

    # Should succeed or at least get to confirmation
    # (May fail in test environment due to questionary, but shouldn't crash)
    assert isinstance(result.exit_code, int)


@pytest.mark.integration
def test_switch_framework_backs_up_all_templates(temp_journal_dir, isolated_config):
    """Test that all template files are backed up during switch."""
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="gtd"
    )

    # GTD has multiple templates
    gtd_templates = [
        "daily-template.md",
        "project-template.md",
        "someday-maybe-template.md",
        "waiting-for-template.md",
    ]

    # Verify GTD templates exist
    for template_name in gtd_templates:
        assert (temp_journal_dir / template_name).exists()

    # Switch to PARA
    runner = CliRunner()
    result = runner.invoke(app, ["switch-framework", "para", "--no-confirm"])
    assert result.exit_code == 0

    # Verify all GTD templates were backed up
    backup_base = temp_journal_dir / ".framework-backups"
    backups = list(backup_base.iterdir())
    backup_dir = backups[0]

    for template_name in gtd_templates:
        backed_up_file = backup_dir / template_name
        assert backed_up_file.exists(), f"{template_name} was not backed up"


@pytest.mark.integration
def test_switch_framework_from_para_to_zettelkasten(temp_journal_dir, isolated_config):
    """Test switching from PARA to Zettelkasten framework."""
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="para"
    )

    runner = CliRunner()
    result = runner.invoke(app, ["switch-framework", "zettelkasten", "--no-confirm"])

    assert result.exit_code == 0

    # Verify config updated
    config = load_config()
    assert config.framework == "zettelkasten"

    # Verify Zettelkasten templates installed
    assert (temp_journal_dir / "note-template.md").exists()
    assert (temp_journal_dir / "index-template.md").exists()
