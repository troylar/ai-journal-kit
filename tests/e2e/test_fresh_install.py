"""
End-to-end tests for fresh installation workflow.

These tests execute the actual CLI command via subprocess to test
the complete user experience of installing ai-journal-kit.
"""

import subprocess
import sys

import pytest

from tests.integration.helpers import (
    assert_ide_config_installed,
    assert_journal_structure_valid,
)


@pytest.mark.e2e
def test_e2e_fresh_install_cursor(temp_journal_dir, isolated_env):
    """Test complete fresh install with Cursor IDE via actual CLI."""
    # Run actual CLI command
    result = subprocess.run(
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

    # Verify success
    assert result.returncode == 0, f"Setup failed: {result.stderr}"
    # On Windows, Rich output may not be captured in stdout, so we rely on returncode
    # and structural verification below

    # Verify journal structure created
    assert temp_journal_dir.exists()
    assert_journal_structure_valid(temp_journal_dir)

    # Verify Cursor config installed
    assert_ide_config_installed(temp_journal_dir, "cursor")


@pytest.mark.e2e
def test_e2e_fresh_install_all_ides(temp_journal_dir, isolated_env):
    """Test fresh install with all IDE configurations."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_journal_kit",
            "setup",
            "--location",
            str(temp_journal_dir),
            "--ide",
            "all",
            "--no-confirm",
        ],
        capture_output=True,
        text=True,
        env=isolated_env,
    )

    assert result.returncode == 0, f"Setup failed: {result.stderr}"

    # Verify all IDE configs installed
    assert_ide_config_installed(temp_journal_dir, "all")

    # Verify specific IDE directories exist
    assert (temp_journal_dir / ".cursor" / "rules").exists()
    assert (temp_journal_dir / ".windsurf" / "rules").exists()
    assert (temp_journal_dir / "CLAUDE.md").exists()
    assert (temp_journal_dir / ".github" / "instructions").exists()


@pytest.mark.e2e
def test_e2e_setup_with_cloud_path(tmp_path, isolated_env):
    """Test setup with cloud-style path (simulating Dropbox/Google Drive)."""
    # Simulate cloud sync folder structure
    cloud_path = tmp_path / "Dropbox" / "Documents" / "Journal"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_journal_kit",
            "setup",
            "--location",
            str(cloud_path),
            "--ide",
            "cursor",
            "--no-confirm",
        ],
        capture_output=True,
        text=True,
        env=isolated_env,
    )

    assert result.returncode == 0, f"Setup failed: {result.stderr}"

    # Verify journal created at cloud path
    assert cloud_path.exists()
    assert_journal_structure_valid(cloud_path)
