# Quickstart: Integration & E2E Testing

**Feature**: Integration & E2E Test Suite  
**For**: Developers adding or running integration/e2e tests

## Running Tests

### Run All Tests

```bash
# Full test suite (unit + integration + e2e)
invoke test-all

# Or use pytest directly
pytest tests/
```

### Run Tests by Level

```bash
# Unit tests only (fast - ~3 seconds)
invoke test
pytest tests/unit/

# Integration tests only (medium - ~5-10 seconds)
invoke test-integration
pytest tests/integration/ -v

# E2E tests only (slow - ~30-60 seconds)
invoke test-e2e
pytest tests/e2e/ -v

# Specific test file
pytest tests/integration/test_setup_complete.py -v
```

### Run with Coverage

```bash
# Integration tests with coverage
pytest tests/integration/ --cov=ai_journal_kit --cov-report=term-missing

# E2E tests with coverage
pytest tests/e2e/ --cov=ai_journal_kit --cov-report=html
```

### Cross-Platform Testing

```bash
# Run on current platform
pytest tests/integration/ -v

# Skip platform-specific tests (when testing on single platform)
pytest tests/integration/ -v -m "not windows_only and not macos_only"

# Run only platform-specific tests
pytest tests/integration/ -v -m "windows_only"
```

## Writing Integration Tests

### Basic Structure

```python
"""
Integration tests for [command name].

Tests the complete flow of [command] with real file I/O.
"""

import pytest
from click.testing import CliRunner
from ai_journal_kit.cli.app import app

@pytest.mark.integration
def test_command_success_scenario(temp_journal_dir, isolated_config):
    """Test [command] completes successfully with valid inputs."""
    runner = CliRunner()
    
    # Execute command
    result = runner.invoke(app, ["command", "--option", "value"])
    
    # Assert success
    assert result.exit_code == 0
    assert "Success message" in result.output
    
    # Verify file system changes
    assert (temp_journal_dir / "expected_file.md").exists()
```

### Using Shared Fixtures

```python
@pytest.mark.integration
def test_with_fixtures(temp_journal_dir, mock_config, journal_factory):
    """Example using shared fixtures from conftest.py."""
    
    # Create a journal with specific configuration
    journal = journal_factory(
        path=temp_journal_dir,
        ide="cursor",
        has_content=True
    )
    
    # Test against the configured journal
    assert journal.config_path.exists()
    assert journal.daily_notes_count > 0
```

### Testing Error Scenarios

```python
@pytest.mark.integration
def test_command_handles_invalid_input(temp_journal_dir):
    """Test [command] handles invalid input gracefully."""
    runner = CliRunner()
    
    # Execute with invalid input
    result = runner.invoke(app, ["command", "--invalid", "value"])
    
    # Assert proper error handling
    assert result.exit_code != 0
    assert "Error:" in result.output
    assert "Suggestion:" in result.output  # Helpful error message
```

### Platform-Specific Tests

```python
import sys
import pytest

@pytest.mark.integration
@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_junction_creation_windows(temp_journal_dir):
    """Test junction creation on Windows (Windows only)."""
    # Test Windows junction logic
    pass

@pytest.mark.integration
@pytest.mark.skipif(sys.platform == "win32", reason="Unix-specific test")
def test_symlink_creation_unix(temp_journal_dir):
    """Test symlink creation on Unix (macOS/Linux only)."""
    # Test Unix symlink logic
    pass
```

## Writing E2E Tests

### Basic E2E Structure

```python
"""
End-to-end tests for [user workflow].

Tests the complete user experience with installed package.
"""

import subprocess
import pytest

@pytest.mark.e2e
def test_fresh_install_workflow(tmp_path, isolated_env):
    """Test complete fresh install from user perspective."""
    journal_path = tmp_path / "my_journal"
    
    # Run actual CLI command as user would
    result = subprocess.run(
        ["ai-journal-kit", "setup", "--location", str(journal_path), "--ide", "cursor", "--no-confirm"],
        capture_output=True,
        text=True,
        env=isolated_env
    )
    
    # Verify success
    assert result.returncode == 0
    assert "Setup complete!" in result.stdout
    
    # Verify journal structure
    assert journal_path.exists()
    assert (journal_path / "daily").exists()
    assert (journal_path / ".cursor" / "rules").exists()
```

### Testing Interactive Commands

```python
@pytest.mark.e2e
def test_interactive_setup(tmp_path, isolated_env):
    """Test interactive setup with simulated user input."""
    # Simulate user input with pexpect or mock stdin
    result = subprocess.run(
        ["ai-journal-kit", "setup"],
        input=f"{tmp_path / 'journal'}\ny\ncursor\ny\n",  # Simulated responses
        capture_output=True,
        text=True,
        env=isolated_env
    )
    
    assert result.returncode == 0
```

## Test Fixtures

### Common Fixtures (conftest.py)

```python
@pytest.fixture
def temp_journal_dir(tmp_path):
    """Provide isolated temporary directory for journal."""
    journal_dir = tmp_path / "test-journal"
    journal_dir.mkdir()
    return journal_dir

@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    """Isolate config file location for test."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(config_dir))
    return config_dir

@pytest.fixture
def journal_factory():
    """Factory for creating configured journal installations."""
    def _create_journal(path, ide="cursor", has_content=False):
        # Create journal structure
        # Install IDE configs
        # Optionally add sample content
        return JournalFixture(path, ide)
    return _create_journal
```

## CI/CD Integration

### Invoke Tasks

```bash
# tasks.py additions
@task
def test_integration(c):
    """Run integration tests."""
    c.run("pytest tests/integration/ -v")

@task
def test_e2e(c):
    """Run end-to-end tests."""
    c.run("pytest tests/e2e/ -v")

@task
def test_all(c):
    """Run all test levels."""
    c.run("pytest tests/ -v")
```

### GitHub Actions

```yaml
# .github/workflows/ci.yml additions
- name: Integration Tests
  run: invoke test-integration

- name: E2E Tests
  run: invoke test-e2e
```

## Test Markers

```python
# Use markers to organize tests
@pytest.mark.unit          # Fast unit tests
@pytest.mark.integration   # Medium-speed integration tests
@pytest.mark.e2e           # Slow end-to-end tests
@pytest.mark.windows_only  # Windows-specific tests
@pytest.mark.macos_only    # macOS-specific tests
@pytest.mark.linux_only    # Linux-specific tests
```

Run specific markers:
```bash
pytest -m integration
pytest -m "e2e and not windows_only"
```

## Debugging Tests

### Run Single Test

```bash
pytest tests/integration/test_setup_complete.py::test_setup_creates_structure -v -s
```

### Debug with PDB

```bash
pytest tests/integration/test_setup_complete.py --pdb
```

### Verbose Output

```bash
pytest tests/integration/ -vv -s --tb=long
```

## Best Practices

### DO

- ✅ Use `tmp_path` fixture for test isolation
- ✅ Use `monkeypatch` for environment variables
- ✅ Test both success and error scenarios
- ✅ Assert on user-facing messages (stdout/stderr)
- ✅ Verify file system state after operations
- ✅ Use descriptive test names
- ✅ Add docstrings explaining what's being tested

### DON'T

- ❌ Share state between tests
- ❌ Test against developer's actual journal
- ❌ Mock file I/O in integration tests
- ❌ Skip error scenario testing
- ❌ Forget to clean up resources
- ❌ Make tests depend on execution order
- ❌ Use sleep() for timing - use proper fixtures

## Common Patterns

### Testing Setup Command

```python
@pytest.mark.integration
def test_setup_with_cursor(temp_journal_dir, isolated_config):
    """Test setup installs Cursor configuration."""
    runner = CliRunner()
    result = runner.invoke(app, [
        "setup",
        "--location", str(temp_journal_dir),
        "--ide", "cursor",
        "--no-confirm"
    ])
    
    assert result.exit_code == 0
    assert (temp_journal_dir / ".cursor" / "rules").exists()
```

### Testing Update Preservation

```python
@pytest.mark.integration
def test_update_preserves_customizations(configured_journal):
    """Test update doesn't overwrite user customizations."""
    # Add custom instruction
    custom_file = configured_journal.path / ".ai-instructions" / "my-coach.md"
    custom_file.parent.mkdir(exist_ok=True)
    custom_file.write_text("# My custom coaching style")
    
    # Run update
    runner = CliRunner()
    result = runner.invoke(app, ["update", "--force"])
    
    # Custom file should still exist with original content
    assert custom_file.exists()
    assert "My custom coaching style" in custom_file.read_text()
```

### Testing Cross-Platform

```python
@pytest.mark.integration
@pytest.mark.parametrize("platform", ["win32", "darwin", "linux"])
def test_platform_specific_behavior(platform, temp_journal_dir, monkeypatch):
    """Test platform-specific features."""
    monkeypatch.setattr("sys.platform", platform)
    
    # Test platform detection and handling
    # ...
```

## Performance Tips

- Use `pytest -n auto` for parallel execution
- Run unit tests first for fast feedback
- Use `pytest --lf` to run last failed tests
- Use `pytest --sw` to stop on first failure
- Cache fixtures when appropriate with `scope="session"`

## Troubleshooting

### Tests Failing on CI but Passing Locally

- Check platform differences (Windows vs Unix paths)
- Verify environment isolation (config paths, temp dirs)
- Check file permissions
- Review GitHub Actions logs for platform-specific errors

### Slow Test Execution

- Use `pytest -n auto` for parallelization
- Check for accidental `time.sleep()` calls
- Verify proper use of fixtures (not recreating unnecessarily)
- Consider moving slow tests to `@pytest.mark.slow`

### Test Flakiness

- Ensure proper test isolation (no shared state)
- Check for timing issues (prefer fixtures over sleep)
- Verify cleanup is happening (use fixtures, not manual cleanup)
- Check for platform-specific path issues

---

## Quick Reference

| Task | Command |
|------|---------|
| Run unit tests | `invoke test` or `pytest tests/unit/` |
| Run integration tests | `invoke test-integration` |
| Run e2e tests | `invoke test-e2e` |
| Run all tests | `invoke test-all` |
| Run with coverage | `pytest --cov=ai_journal_kit` |
| Run last failed | `pytest --lf` |
| Run in parallel | `pytest -n auto` |
| Debug single test | `pytest path/to/test.py::test_name -vv -s` |
| Full CI simulation | `invoke ci` |

---

**Ready to implement!** Start with `/speckit.tasks` to generate the implementation task list.

