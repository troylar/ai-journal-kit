"""Integration tests for multi-journal setup."""

import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from ai_journal_kit.core.config import load_multi_journal_config
from tests.integration.fixtures import create_journal_fixture


@pytest.mark.integration
def test_setup_first_journal_defaults_to_default_name(temp_journal_dir, isolated_config):
    """Test that first journal setup defaults to 'default' name."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0

    # Load config and check
    multi_config = load_multi_journal_config()
    assert multi_config is not None
    assert "default" in multi_config.journals
    assert multi_config.active_journal == "default"


@pytest.mark.integration
def test_setup_second_journal_with_name(temp_journal_dir, isolated_config):
    """Test setting up a second journal with explicit name."""
    # Create first journal
    journal1 = temp_journal_dir / "journal1"
    create_journal_fixture(
        path=journal1, ide="cursor", config_dir=isolated_config, framework="default"
    )

    # Create second journal with name
    journal2 = temp_journal_dir / "journal2"
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "setup",
            "--name",
            "business",
            "--location",
            str(journal2),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0

    # Load config and check
    multi_config = load_multi_journal_config()
    assert "default" in multi_config.journals
    assert "business" in multi_config.journals
    assert len(multi_config.journals) == 2


@pytest.mark.integration
def test_setup_duplicate_name_fails(temp_journal_dir, isolated_config):
    """Test that setup with duplicate name fails."""
    # Create first journal
    create_journal_fixture(
        path=temp_journal_dir, ide="cursor", config_dir=isolated_config, framework="default"
    )

    # Try to create another journal with same name
    journal2 = temp_journal_dir / "journal2"
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "setup",
            "--name",
            "default",
            "--location",
            str(journal2),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code != 0
    assert "already exists" in result.output.lower()


@pytest.mark.integration
def test_setup_named_journal_creates_manifest(temp_journal_dir, isolated_config):
    """Test that setup creates manifest for named journal."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "setup",
            "--name",
            "test",
            "--location",
            str(temp_journal_dir),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0

    # Verify manifest exists
    manifest_path = temp_journal_dir / ".system-manifest.json"
    assert manifest_path.exists()


@pytest.mark.integration
def test_setup_first_journal_is_automatically_active(temp_journal_dir, isolated_config):
    """Test that first journal is automatically set as active."""
    runner = CliRunner()
    runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--framework",
            "default",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    multi_config = load_multi_journal_config()
    assert multi_config.active_journal == "default"


@pytest.mark.integration
def test_setup_second_journal_does_not_change_active(temp_journal_dir, isolated_config):
    """Test that setting up second journal doesn't change active journal."""
    # Create first journal
    journal1 = temp_journal_dir / "journal1"
    create_journal_fixture(
        path=journal1, ide="cursor", config_dir=isolated_config, framework="default"
    )

    # Verify default is active
    multi_config = load_multi_journal_config()
    assert multi_config.active_journal == "default"

    # Create second journal
    journal2 = temp_journal_dir / "journal2"
    runner = CliRunner()
    runner.invoke(
        app,
        [
            "setup",
            "--name",
            "business",
            "--location",
            str(journal2),
            "--framework",
            "gtd",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    # Default should still be active
    multi_config = load_multi_journal_config()
    assert multi_config.active_journal == "default"


@pytest.mark.integration
def test_setup_multiple_journals_all_independent(temp_journal_dir, isolated_config):
    """Test that multiple journals are independent."""
    runner = CliRunner()

    # Create personal journal with default framework
    journal1 = temp_journal_dir / "personal"
    runner.invoke(
        app,
        [
            "setup",
            "--name",
            "personal",
            "--location",
            str(journal1),
            "--framework",
            "default",
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    # Create business journal with GTD framework
    journal2 = temp_journal_dir / "business"
    runner.invoke(
        app,
        [
            "setup",
            "--name",
            "business",
            "--location",
            str(journal2),
            "--framework",
            "gtd",
            "--ide",
            "windsurf",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    # Create test journal with PARA framework
    journal3 = temp_journal_dir / "test"
    runner.invoke(
        app,
        [
            "setup",
            "--name",
            "test",
            "--location",
            str(journal3),
            "--framework",
            "para",
            "--ide",
            "claude-code",
            "--no-confirm",
        ],
        catch_exceptions=False,
    )

    # Verify all journals exist with correct settings
    multi_config = load_multi_journal_config()
    assert len(multi_config.journals) == 3

    assert multi_config.journals["personal"].framework == "default"
    assert multi_config.journals["personal"].ide == "cursor"

    assert multi_config.journals["business"].framework == "gtd"
    assert multi_config.journals["business"].ide == "windsurf"

    assert multi_config.journals["test"].framework == "para"
    assert multi_config.journals["test"].ide == "claude-code"


@pytest.mark.integration
def test_backward_compatibility_old_config_migrates(temp_journal_dir, isolated_config):
    """Test that old single-journal config migrates automatically."""
    import json

    from ai_journal_kit.core.config import get_config_path

    # Create old-style config
    config_path = get_config_path()
    old_config = {
        "journal_location": str(temp_journal_dir),
        "ide": "cursor",
        "framework": "gtd",
        "version": "1.0.0",
        "created_at": "2025-01-09T10:00:00",
        "last_updated": "2025-01-09T10:00:00",
        "use_symlink": False,
    }
    config_path.write_text(json.dumps(old_config))

    # Create journal structure
    (temp_journal_dir / "daily").mkdir(parents=True)
    (temp_journal_dir / "projects").mkdir()

    # Run list command (should trigger migration)
    runner = CliRunner()
    result = runner.invoke(app, ["list"], catch_exceptions=False)

    assert result.exit_code == 0

    # Verify migration happened
    multi_config = load_multi_journal_config()
    assert "default" in multi_config.journals
    assert multi_config.journals["default"].framework == "gtd"
    assert multi_config.journals["default"].ide == "cursor"

    # Verify new format was saved
    new_data = json.loads(config_path.read_text())
    assert "journals" in new_data
    assert "active_journal" in new_data
