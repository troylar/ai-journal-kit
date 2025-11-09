"""Integration tests for framework-specific template functionality.

Tests framework selection and template installation:
- Default framework
- GTD templates
- PARA templates
- Bullet Journal templates
- Zettelkasten templates
"""

import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from ai_journal_kit.core.config import load_config
from tests.integration.helpers import assert_journal_structure_valid


@pytest.mark.integration
def test_setup_with_default_framework(temp_journal_dir, isolated_config):
    """Test setup with default framework."""
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--framework",
            "default",
            "--no-confirm",
        ],
    )

    # Setup should succeed
    assert result.exit_code == 0, f"Setup failed: {result.output}"

    # Verify structure created
    assert_journal_structure_valid(temp_journal_dir)

    # Verify config has framework set
    config = load_config()
    assert config.framework == "default"

    # Default framework should have WELCOME.md but no framework-specific templates
    assert (temp_journal_dir / "WELCOME.md").exists()


@pytest.mark.integration
def test_setup_with_gtd_framework(temp_journal_dir, isolated_config):
    """Test setup with GTD framework creates GTD templates."""
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--framework",
            "gtd",
            "--no-confirm",
        ],
    )

    assert result.exit_code == 0, f"Setup failed: {result.output}"
    assert_journal_structure_valid(temp_journal_dir)

    # Verify config has GTD framework
    config = load_config()
    assert config.framework == "gtd"

    # Verify GTD templates were copied
    assert (temp_journal_dir / "daily-template.md").exists()
    assert (temp_journal_dir / "project-template.md").exists()
    assert (temp_journal_dir / "someday-maybe-template.md").exists()
    assert (temp_journal_dir / "waiting-for-template.md").exists()

    # Check GTD-specific content in daily template
    daily_content = (temp_journal_dir / "daily-template.md").read_text(encoding="utf-8")
    assert "Next Actions" in daily_content
    assert "@work" in daily_content or "@home" in daily_content


@pytest.mark.integration
def test_setup_with_para_framework(temp_journal_dir, isolated_config):
    """Test setup with PARA framework creates PARA templates."""
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--framework",
            "para",
            "--no-confirm",
        ],
    )

    assert result.exit_code == 0, f"Setup failed: {result.output}"
    assert_journal_structure_valid(temp_journal_dir)

    # Verify config has PARA framework
    config = load_config()
    assert config.framework == "para"

    # Verify PARA templates were copied
    assert (temp_journal_dir / "daily-template.md").exists()
    assert (temp_journal_dir / "project-template.md").exists()
    assert (temp_journal_dir / "area-template.md").exists()
    assert (temp_journal_dir / "resource-template.md").exists()

    # Check PARA-specific content in area template
    area_content = (temp_journal_dir / "area-template.md").read_text(encoding="utf-8")
    assert "Area:" in area_content or "responsibility" in area_content.lower()


@pytest.mark.integration
def test_setup_with_bullet_journal_framework(temp_journal_dir, isolated_config):
    """Test setup with Bullet Journal framework creates BuJo templates."""
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--framework",
            "bullet-journal",
            "--no-confirm",
        ],
    )

    assert result.exit_code == 0, f"Setup failed: {result.output}"
    assert_journal_structure_valid(temp_journal_dir)

    # Verify config has Bullet Journal framework
    config = load_config()
    assert config.framework == "bullet-journal"

    # Verify Bullet Journal templates were copied
    assert (temp_journal_dir / "daily-template.md").exists()
    assert (temp_journal_dir / "monthly-template.md").exists()
    assert (temp_journal_dir / "future-log-template.md").exists()
    assert (temp_journal_dir / "collection-template.md").exists()

    # Check Bullet Journal-specific content in daily template
    daily_content = (temp_journal_dir / "daily-template.md").read_text(encoding="utf-8")
    assert "rapid logging" in daily_content.lower() or "task" in daily_content.lower()


@pytest.mark.integration
def test_setup_with_zettelkasten_framework(temp_journal_dir, isolated_config):
    """Test setup with Zettelkasten framework creates Zettelkasten templates."""
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--framework",
            "zettelkasten",
            "--no-confirm",
        ],
    )

    assert result.exit_code == 0, f"Setup failed: {result.output}"
    assert_journal_structure_valid(temp_journal_dir)

    # Verify config has Zettelkasten framework
    config = load_config()
    assert config.framework == "zettelkasten"

    # Verify Zettelkasten templates were copied
    assert (temp_journal_dir / "daily-template.md").exists()
    assert (temp_journal_dir / "note-template.md").exists()
    assert (temp_journal_dir / "index-template.md").exists()

    # Check Zettelkasten-specific content in note template
    note_content = (temp_journal_dir / "note-template.md").read_text(encoding="utf-8")
    assert (
        "atomic" in note_content.lower()
        or "permanent" in note_content.lower()
        or "related notes" in note_content.lower()
    )


@pytest.mark.integration
def test_setup_with_invalid_framework(temp_journal_dir, isolated_config):
    """Test setup with invalid framework fails gracefully."""
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--framework",
            "invalid-framework",
            "--no-confirm",
        ],
    )

    # Should fail with error
    assert result.exit_code != 0
    assert "invalid" in result.output.lower() or "error" in result.output.lower()
