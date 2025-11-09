"""
End-to-end tests for upgrade/update workflow.

These tests execute actual CLI commands via subprocess to test
the complete user experience of updating an existing journal.
"""

import subprocess
import sys

import pytest

from tests.integration.helpers import assert_journal_structure_valid


@pytest.mark.e2e
def test_e2e_upgrade_preserves_everything(temp_journal_dir, isolated_env):
    """Test complete upgrade workflow preserves user data."""
    # First, create a journal using setup
    result_setup = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_journal_kit",
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        capture_output=True,
        text=True,
        env=isolated_env,
    )
    assert result_setup.returncode == 0

    # Add custom content
    custom_file = temp_journal_dir / "daily" / "my-note.md"
    custom_file.write_text("# My Important Note\n\nDon't lose this!")

    # Run update
    result_update = subprocess.run(
        [sys.executable, "-m", "ai_journal_kit", "update", "--no-confirm"],
        capture_output=True,
        text=True,
        env=isolated_env,
    )

    # Update should succeed
    assert result_update.returncode == 0 or "up to date" in result_update.stdout.lower()

    # Custom file should still exist
    assert custom_file.exists()
    assert "My Important Note" in custom_file.read_text(encoding="utf-8")

    # Structure should remain valid
    assert_journal_structure_valid(temp_journal_dir)


@pytest.mark.e2e
def test_e2e_upgrade_multiple_versions(temp_journal_dir, isolated_env):
    """Test multiple sequential updates work correctly."""
    # Setup journal
    result_setup = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_journal_kit",
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "windsurf",
            "--no-confirm",
        ],
        capture_output=True,
        text=True,
        env=isolated_env,
    )
    assert result_setup.returncode == 0

    # First update
    result_update1 = subprocess.run(
        [sys.executable, "-m", "ai_journal_kit", "update", "--no-confirm"],
        capture_output=True,
        text=True,
        env=isolated_env,
    )

    # Second update (should handle already-updated state)
    result_update2 = subprocess.run(
        [sys.executable, "-m", "ai_journal_kit", "update", "--no-confirm"],
        capture_output=True,
        text=True,
        env=isolated_env,
    )

    # Both should succeed or indicate up-to-date
    assert result_update1.returncode == 0
    assert result_update2.returncode == 0 or "up to date" in result_update2.stdout.lower()

    # Structure should remain valid after multiple updates
    assert_journal_structure_valid(temp_journal_dir)
