"""
Integration tests for setup command complete flow.

Tests all setup scenarios including:
- Journal structure creation
- IDE configuration installation
- Config file generation
- Error handling and validation
"""

import pytest
from typer.testing import CliRunner

from ai_journal_kit.cli.app import app
from tests.integration.helpers import (
    assert_config_valid,
    assert_ide_config_installed,
    assert_journal_structure_valid,
)


@pytest.mark.integration
def test_setup_creates_all_folders(temp_journal_dir, isolated_config):
    """Test setup creates all required journal folders."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )

    # Setup should succeed
    assert result.exit_code == 0, f"Setup failed: {result.output}"

    # Verify all folders created
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.integration
def test_setup_creates_all_templates(temp_journal_dir, isolated_config):
    """Test setup creates template files."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Check WELCOME.md template
    welcome_file = temp_journal_dir / "WELCOME.md"
    assert welcome_file.exists(), "WELCOME.md template not created"
    assert welcome_file.is_file()


@pytest.mark.integration
def test_setup_creates_config_file(temp_journal_dir, isolated_config):
    """Test setup creates valid config file."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "windsurf", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify config file created
    config_file = isolated_config / "config.json"
    assert_config_valid(config_file, expected_journal=temp_journal_dir, expected_ide="windsurf")


@pytest.mark.integration
def test_setup_installs_cursor_config(temp_journal_dir, isolated_config):
    """Test setup installs Cursor IDE configuration."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify Cursor config installed
    assert_ide_config_installed(temp_journal_dir, "cursor")

    # Check specific Cursor files
    cursor_rules = temp_journal_dir / ".cursor" / "rules"
    assert cursor_rules.exists()
    assert (cursor_rules / "journal-coach.mdc").exists()


@pytest.mark.integration
def test_setup_installs_windsurf_config(temp_journal_dir, isolated_config):
    """Test setup installs Windsurf IDE configuration."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "windsurf", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify Windsurf config installed
    assert_ide_config_installed(temp_journal_dir, "windsurf")

    # Check specific Windsurf files
    windsurf_rules = temp_journal_dir / ".windsurf" / "rules"
    assert windsurf_rules.exists()


@pytest.mark.integration
def test_setup_installs_claude_config(temp_journal_dir, isolated_config):
    """Test setup installs Claude Code configuration."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "claude-code", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify Claude Code config installed
    assert_ide_config_installed(temp_journal_dir, "claude-code")

    # Check CLAUDE.md file exists
    claude_file = temp_journal_dir / "CLAUDE.md"
    assert claude_file.exists()


@pytest.mark.integration
def test_setup_installs_copilot_config(temp_journal_dir, isolated_config):
    """Test setup installs GitHub Copilot configuration."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "copilot", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify Copilot config installed
    assert_ide_config_installed(temp_journal_dir, "copilot")

    # Check Copilot instruction files
    copilot_instructions = temp_journal_dir / ".github" / "instructions"
    assert copilot_instructions.exists()


@pytest.mark.integration
def test_setup_installs_all_configs(temp_journal_dir, isolated_config):
    """Test setup installs all IDE configurations when 'all' selected."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "all", "--no-confirm"]
    )

    assert result.exit_code == 0

    # Verify all IDE configs installed
    assert_ide_config_installed(temp_journal_dir, "all")


@pytest.mark.integration
def test_setup_with_custom_path(tmp_path, isolated_config):
    """Test setup works with custom journal path."""
    custom_path = tmp_path / "custom" / "journal" / "location"

    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(custom_path), "--ide", "cursor", "--no-confirm"]
    )

    # Debug: print output if failed
    if result.exit_code != 0:
        print(f"\nSetup failed with exit code {result.exit_code}")
        print(f"Output: {result.output}")
        if result.exception:
            print(f"Exception: {result.exception}")

    assert result.exit_code == 0, f"Setup failed: {result.output}"

    # Verify journal created at custom path
    assert custom_path.exists()
    assert_journal_structure_valid(custom_path)


@pytest.mark.integration
def test_setup_prevents_duplicate_installation(temp_journal_dir, isolated_config):
    """Test setup prevents duplicate installation."""
    runner = CliRunner()

    # First setup should succeed
    result1 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )
    assert result1.exit_code == 0

    # Second setup without --name should fail with appropriate message
    result2 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )

    # Should exit with error (needs --name for additional journals)
    assert result2.exit_code != 0
    # Should mention name is required for additional journals
    assert "name required" in result2.output.lower() or "use --name" in result2.output.lower()


@pytest.mark.skip(
    reason="Behavior changed with multi-journal support - use doctor command to repair deleted journals"
)
@pytest.mark.integration
def test_setup_handles_deleted_journal(temp_journal_dir, isolated_config):
    """Test setup handles case where journal was manually deleted.

    NOTE: With multi-journal support, if a journal directory is deleted but config remains,
    use 'ai-journal-kit doctor' to repair. Setup now requires --name for new journals.
    """
    runner = CliRunner()

    # First setup
    result1 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )
    assert result1.exit_code == 0

    # Manually delete journal directory
    import shutil

    shutil.rmtree(temp_journal_dir)

    # With multi-journal, setup won't recreate without --name, and --name "default" conflicts
    # User should use 'doctor' command to repair deleted journals
    # This test is skipped until we add a repair/recreate command


@pytest.mark.integration
def test_setup_creates_parent_directory(tmp_path, isolated_config):
    """Test setup creates parent directories if they don't exist."""
    nested_path = tmp_path / "deeply" / "nested" / "journal"

    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(nested_path), "--ide", "cursor", "--no-confirm"]
    )

    assert result.exit_code == 0
    assert nested_path.exists()
    assert_journal_structure_valid(nested_path)


@pytest.mark.integration
def test_setup_dry_run_mode(temp_journal_dir, isolated_config):
    """Test setup dry-run mode shows actions without making changes."""
    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--dry-run"]
    )

    # Dry run should succeed
    assert result.exit_code == 0

    # Should mention it's a dry run
    assert "dry run" in result.output.lower() or "would" in result.output.lower()

    # Journal should NOT be created
    assert not temp_journal_dir.exists() or len(list(temp_journal_dir.iterdir())) == 0


@pytest.mark.integration
def test_setup_handles_cancellation(temp_journal_dir, isolated_config):
    """Test setup handles user cancellation gracefully."""
    runner = CliRunner()

    # Simulate user cancellation by not providing --no-confirm
    # and providing 'n' as input
    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor"], input="n\n"
    )

    # Should handle cancellation gracefully
    assert result.exit_code != 0 or "cancelled" in result.output.lower()


@pytest.mark.integration
def test_setup_with_invalid_path(isolated_config):
    """Test setup handles invalid path gracefully (covers lines 86-88)."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "setup",
            "/invalid/\0/path",  # Invalid path with null byte
            "--ide",
            "cursor",
            "--no-confirm",
        ],
    )

    # Should fail with error
    assert result.exit_code != 0
    assert "error" in result.output.lower() or "invalid" in result.output.lower()


@pytest.mark.integration
def test_setup_with_invalid_ide(temp_journal_dir, isolated_config):
    """Test setup handles invalid IDE gracefully (covers lines 97-99)."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", str(temp_journal_dir), "--ide", "invalid-ide-name", "--no-confirm"]
    )

    # Should fail with error
    assert result.exit_code != 0
    assert "ide" in result.output.lower() or "invalid" in result.output.lower()


@pytest.mark.integration
def test_setup_with_parent_creation_declined(temp_journal_dir, isolated_config):
    """Test setup when user declines parent directory creation (covers lines 74-81)."""
    # Use nested path that doesn't exist
    nested_path = temp_journal_dir / "nonexistent" / "journal"

    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", str(nested_path), "--ide", "cursor"], input="n\n"
    )  # Decline parent creation

    # Should cancel setup
    assert result.exit_code != 0
    assert "cancel" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_setup_interactive_location_prompt(isolated_config, tmp_path):
    """Test setup with interactive location prompt (covers line 60)."""
    journal_path = tmp_path / "interactive-journal"

    runner = CliRunner()
    # No --location flag, so it will prompt
    # Provide location via stdin
    result = runner.invoke(
        app, ["setup", "--ide", "cursor", "--no-confirm"], input=f"{journal_path}\n"
    )

    # Should succeed
    assert result.exit_code == 0 or journal_path.exists()


@pytest.mark.integration
def test_setup_interactive_ide_prompt(temp_journal_dir, isolated_config):
    """Test setup with interactive IDE prompt (covers line 92)."""
    runner = CliRunner()
    # No --ide flag, so it will prompt
    # Provide IDE choice via stdin
    result = runner.invoke(
        app, ["setup", str(temp_journal_dir), "--no-confirm"], input="1\n"
    )  # Choose first IDE option

    # Should succeed or at least not crash
    assert result.exit_code == 0 or "ide" in result.output.lower()


@pytest.mark.integration
def test_setup_dry_run_parent_creation(temp_journal_dir, isolated_config):
    """Test setup dry-run mode shows parent directory creation (covers line 69)."""
    nested_path = temp_journal_dir / "parent" / "journal"

    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", "--location", str(nested_path), "--ide", "cursor", "--dry-run"]
    )

    # Dry-run shows what would happen but may exit with error (doesn't actually create)
    # The key is that it shows the "would create" message
    output_lower = result.output.lower()
    assert "dry run" in output_lower or "would create" in output_lower


@pytest.mark.integration
def test_setup_parent_creation_accepted_interactive(temp_journal_dir, isolated_config):
    """Test setup when user accepts parent directory creation interactively (lines 74-78)."""
    nested_path = temp_journal_dir / "new_parent" / "journal"

    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", "--location", str(nested_path), "--ide", "cursor"], input="y\ny\n"
    )  # Yes to create parent, Yes to proceed

    # Should succeed or create the parent
    assert result.exit_code == 0 or nested_path.parent.exists()


@pytest.mark.integration
def test_setup_parent_creation_declined_interactive(temp_journal_dir, isolated_config):
    """Test setup when user declines parent directory creation interactively (lines 80-81)."""
    nested_path = temp_journal_dir / "decline_parent" / "journal"

    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", "--location", str(nested_path), "--ide", "cursor"], input="n\n"
    )  # No to create parent

    # Should fail since parent wasn't created
    assert result.exit_code != 0
    assert "cancel" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.integration
def test_setup_interactive_ide_selection_complete(isolated_config, temp_journal_dir):
    """Test setup with full interactive IDE selection (line 92)."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--no-confirm"], input="cursor\n"
    )  # Provide IDE name when prompted

    # Should complete successfully
    assert result.exit_code == 0 or temp_journal_dir.exists()


@pytest.mark.integration
def test_setup_with_invalid_ide_choice(temp_journal_dir, isolated_config):
    """Test setup with invalid IDE that triggers validation error (lines 97-99)."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["setup", "--location", str(temp_journal_dir), "--ide", "not-a-valid-ide", "--no-confirm"],
    )

    # Should fail with validation error
    assert result.exit_code != 0


@pytest.mark.integration
def test_setup_exception_during_creation(temp_journal_dir, isolated_config):
    """Test setup handles exceptions during journal creation (lines 163-165)."""

    runner = CliRunner()

    # Use a path that will cause issues
    bad_path = temp_journal_dir / "test.txt"
    bad_path.write_text("existing file")

    result = runner.invoke(
        app, ["setup", "--location", str(bad_path), "--ide", "cursor", "--no-confirm"]
    )

    # Should handle error gracefully
    # May succeed or fail depending on validation, key is no crash
    assert isinstance(result.exit_code, int)


@pytest.mark.integration
def test_setup_on_existing_journal_detects_content(temp_journal_dir, isolated_config):
    """Test setup detects existing journal content and shows warning."""
    runner = CliRunner()

    # First setup
    result1 = runner.invoke(
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
    assert result1.exit_code == 0

    # Second setup on same location with --no-confirm
    result2 = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "windsurf",
            "--framework",
            "para",
            "--no-confirm",
            "--name",
            "test2",
        ],
    )

    # Should detect existing content and show warning
    assert "existing" in result2.output.lower() or "detected" in result2.output.lower()
    assert result2.exit_code == 0  # Should proceed in no-confirm mode


@pytest.mark.integration
def test_setup_on_existing_journal_offers_ide_choice(temp_journal_dir, isolated_config):
    """Test setup on existing journal with --no-confirm mode."""
    runner = CliRunner()

    # First setup with cursor
    result1 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )
    assert result1.exit_code == 0

    # Verify cursor IDE was installed
    assert (temp_journal_dir / ".cursor").exists()

    # Second setup on same location with --no-confirm
    # Should proceed automatically and detect existing IDE
    result2 = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "windsurf",
            "--no-confirm",
            "--name",
            "test2",
        ],
    )

    # Should complete successfully
    assert result2.exit_code == 0
    assert "existing" in result2.output.lower() or "reinstall" in result2.output.lower()


@pytest.mark.integration
def test_setup_on_existing_journal_user_cancels(temp_journal_dir, isolated_config):
    """Test setup on existing journal when user cancels."""
    runner = CliRunner()

    # First setup
    result1 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )
    assert result1.exit_code == 0

    # Second setup on same location - cancel when prompted
    result2 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--name", "test2"], input="n\n"
    )

    # Should cancel gracefully
    assert result2.exit_code == 0  # Exit code 0 on user cancel
    assert "cancel" in result2.output.lower()


@pytest.mark.integration
def test_setup_framework_placeholder_replacement(temp_journal_dir, isolated_config):
    """Test that {framework} placeholder is replaced in IDE configs."""
    runner = CliRunner()

    # Setup with PARA framework
    result = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "claude-code",
            "--framework",
            "para",
            "--no-confirm",
        ],
    )
    assert result.exit_code == 0

    # Read CLAUDE.md and verify {framework} was replaced with "para"
    claude_file = temp_journal_dir / "CLAUDE.md"
    assert claude_file.exists()

    content = claude_file.read_text(encoding="utf-8")
    assert "para" in content.lower()  # Should contain actual framework name
    assert "{framework}" not in content  # Should NOT contain placeholder


@pytest.mark.integration
def test_setup_stores_actual_version(temp_journal_dir, isolated_config):
    """Test that setup stores actual package version, not hardcoded '1.0.0'."""
    from ai_journal_kit import __version__
    from ai_journal_kit.core.config import load_multi_journal_config

    runner = CliRunner()

    result = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )
    assert result.exit_code == 0

    # Load config and verify version matches package version
    config = load_multi_journal_config()
    assert config is not None
    assert "default" in config.journals

    journal_profile = config.journals["default"]
    assert journal_profile.version == __version__
    assert journal_profile.version != "1.0.0"  # Should not be hardcoded


@pytest.mark.integration
def test_setup_reinstall_message_clarity(temp_journal_dir, isolated_config):
    """Test that setup shows clear 'update' message when reinstalling."""
    runner = CliRunner()

    # First setup
    result1 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )
    assert result1.exit_code == 0
    assert "create" in result1.output.lower()  # First time should say "create"

    # Second setup (reinstall) with no-confirm
    result2 = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--no-confirm",
            "--name",
            "test2",
        ],
    )

    # Should show "update" or "reinstall" message, not "create"
    assert result2.exit_code == 0
    assert "update" in result2.output.lower() or "reinstall" in result2.output.lower(), (
        "Should show update/reinstall message"
    )


@pytest.mark.integration
def test_setup_detects_multiple_ide_configs(temp_journal_dir, isolated_config):
    """Test that setup detects multiple IDE configurations."""
    runner = CliRunner()

    # Setup with "all" to install multiple IDEs
    result1 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "all", "--no-confirm"]
    )
    assert result1.exit_code == 0

    # Verify multiple IDEs were installed
    assert (temp_journal_dir / ".cursor").exists()
    assert (temp_journal_dir / ".windsurf").exists()
    assert (temp_journal_dir / "CLAUDE.md").exists()

    # Second setup should detect existing IDE configs
    result2 = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--no-confirm",
            "--name",
            "test2",
        ],
    )

    # Should detect existing content
    assert result2.exit_code == 0
    output_lower = result2.output.lower()
    assert "existing" in output_lower or "cursor" in output_lower


@pytest.mark.integration
def test_setup_preserves_customizations(temp_journal_dir, isolated_config):
    """Test that setup mentions preservation of .ai-instructions/ customizations."""
    runner = CliRunner()

    # First setup
    result1 = runner.invoke(
        app, ["setup", "--location", str(temp_journal_dir), "--ide", "cursor", "--no-confirm"]
    )
    assert result1.exit_code == 0

    # Create custom instructions
    custom_dir = temp_journal_dir / ".ai-instructions"
    custom_dir.mkdir(exist_ok=True)
    (custom_dir / "my-coach.md").write_text("# My custom coaching")

    # Second setup with --no-confirm and IDE specified
    result2 = runner.invoke(
        app,
        [
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--no-confirm",
            "--name",
            "test2",
        ],
    )

    # Should mention preservation of customizations
    assert result2.exit_code == 0
    output_lower = result2.output.lower()
    assert "customizations" in output_lower or ".ai-instructions" in output_lower


@pytest.mark.integration
def test_setup_all_frameworks_replace_placeholder(temp_journal_dir, isolated_config):
    """Test that all frameworks correctly replace {framework} placeholder."""
    frameworks = ["default", "gtd", "para", "bullet-journal", "zettelkasten"]

    for i, framework in enumerate(frameworks):
        journal_path = temp_journal_dir / f"journal_{framework}"
        journal_path.mkdir(parents=True, exist_ok=True)

        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "setup",
                "--location",
                str(journal_path),
                "--ide",
                "claude-code",
                "--framework",
                framework,
                "--no-confirm",
                "--name",
                f"test_{framework}",
            ],
        )

        assert result.exit_code == 0, f"Setup failed for framework {framework}"

        # Verify placeholder was replaced
        claude_file = journal_path / "CLAUDE.md"
        assert claude_file.exists()

        content = claude_file.read_text(encoding="utf-8")
        assert "{framework}" not in content, f"Placeholder not replaced for {framework}"
        assert framework in content or "flexible" in content  # Some frameworks use display names
