# Testing Guide

This document describes the testing strategy, structure, and best practices for AI Journal Kit.

## 📊 Test Statistics

- **Total Tests**: 141
- **Unit Tests**: 41  
- **Integration Tests**: 78
- **E2E Tests**: 22
- **Code Coverage**: ~75% on core business logic
- **Platforms Tested**: Ubuntu, macOS, Windows

## 🏗️ Test Structure

```
tests/
├── unit/                      # Fast, isolated unit tests
│   ├── test_config.py         # Config management
│   ├── test_templates.py      # Template operations
│   ├── test_validation.py     # Path/input validation
│   ├── test_journal.py        # Journal structure
│   ├── test_platform.py       # Platform detection
│   └── test_ui.py             # UI helpers
│
├── integration/               # Real filesystem, no network
│   ├── conftest.py            # Shared fixtures
│   ├── fixtures/              # Test data factories
│   │   ├── journal_factory.py # Create test journals
│   │   └── config_factory.py  # Create test configs
│   ├── helpers.py             # Assertion helpers
│   ├── test_setup_complete.py # Setup command tests
│   ├── test_update_flow.py    # Update command tests
│   ├── test_status_diagnostics.py  # Status command
│   ├── test_doctor_repairs.py # Doctor command
│   └── test_move_journal.py   # Move command
│
└── e2e/                       # Complete user workflows
    ├── conftest.py            # E2E fixtures
    ├── test_fresh_install.py  # Fresh installation
    └── test_upgrade_workflow.py # Upgrade scenarios
```

## 🎯 Test Types

### Unit Tests

**Purpose**: Test individual functions/classes in isolation

**Characteristics**:
- ⚡ **Fast**: < 1ms per test
- 🔒 **Isolated**: No I/O, mocked dependencies
- 🎯 **Focused**: One function/class at a time
- 📝 **Coverage**: Aim for 80%+ on business logic

**When to write**:
- Pure functions (config parsing, validation)
- Business logic (template matching, IDE detection)
- Utility functions (path normalization, platform checks)

**Example**:
```python
def test_validate_ide_accepts_valid_ides():
    """Test that validate_ide accepts all valid IDE names."""
    for ide in ["cursor", "windsurf", "claude-code", "copilot", "all"]:
        validate_ide(ide)  # Should not raise
```

### Integration Tests

**Purpose**: Test components working together with real filesystem

**Characteristics**:
- 🏃 **Moderate speed**: 10-100ms per test
- 📂 **Real I/O**: Actual file operations
- 🔌 **Multi-component**: Multiple modules interact
- 🌐 **No network**: Offline only

**When to write**:
- CLI command workflows
- File system operations (create, copy, move)
- Config file management
- Template installation

**Example**:
```python
def test_setup_creates_all_folders(temp_journal_dir, isolated_config):
    """Test setup creates complete journal structure."""
    runner = CliRunner()
    result = runner.invoke(app, [
        "setup",
        str(temp_journal_dir),
        "--ide", "cursor",
        "--no-confirm"
    ])
    
    assert result.exit_code == 0
    assert_journal_structure_valid(temp_journal_dir)
```

### E2E Tests

**Purpose**: Test complete user journeys from start to finish

**Characteristics**:
- 🐌 **Slower**: 100-1000ms per test
- 🔄 **Full workflows**: Multiple commands chained
- 🎭 **User perspective**: Real-world scenarios
- 📦 **Comprehensive**: Setup → Use → Update → Move

**When to write**:
- Fresh installation workflows
- Upgrade scenarios (v1 → v2)
- Migration paths
- Cross-IDE workflows

**Example**:
```python
def test_e2e_fresh_install_cursor(tmp_path, isolated_config):
    """Test complete fresh installation with Cursor."""
    journal_path = tmp_path / "my-journal"
    
    # Setup
    result_setup = runner.invoke(app, ["setup", str(journal_path), "--ide", "cursor", "--no-confirm"])
    assert result_setup.exit_code == 0
    
    # Verify structure
    assert_journal_structure_valid(journal_path)
    assert_ide_config_installed(journal_path, "cursor")
    
    # Status check
    result_status = runner.invoke(app, ["status"])
    assert result_status.exit_code == 0
```

## 🛠️ Running Tests

### Quick Commands

```bash
# Run all tests
pytest

# Run specific test type
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run specific test file
pytest tests/integration/test_setup_complete.py

# Run specific test
pytest tests/unit/test_config.py::test_load_config_from_valid_json

# Run tests matching pattern
pytest -k "setup and cursor"
```

### Using Invoke Tasks

```bash
# All tests with coverage
invoke test

# Specific test types
invoke test.unit
invoke test.integration
invoke test.e2e

# Fast run (no coverage)
invoke test.quick

# Watch mode (auto-run on changes)
invoke test.watch

# Coverage report
invoke test.coverage
```

### Parallel Execution

```bash
# Auto-detect CPU cores
pytest -n auto

# Specific number of workers
pytest -n 4

# Distribute by file (default)
pytest -n auto --dist loadfile
```

## 🏭 Test Fixtures

### Shared Fixtures

**`temp_journal_dir`** - Temporary directory for test journals
```python
@pytest.fixture
def temp_journal_dir(tmp_path):
    """Provide a clean temporary directory for journal tests."""
    return tmp_path / "test-journal"
```

**`isolated_config`** - Isolated config directory
```python
@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    """Provide isolated config directory for testing."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    monkeypatch.setenv("AI_JOURNAL_CONFIG_DIR", str(config_dir))
    return config_dir
```

### Factory Fixtures

**`journal_factory`** - Create configured journal installations
```python
def create_journal_fixture(
    path: Path,
    ide: str = "cursor",
    has_content: bool = False,
    config_dir: Optional[Path] = None
) -> JournalInfo:
    """Create a fully configured test journal."""
    # Creates journal structure + IDE configs + sample content
```

**`config_factory`** - Create config objects
```python
def create_config_fixture(
    journal_location: Path,
    ide: str = "cursor",
    config_dir: Optional[Path] = None
) -> Config:
    """Create and save a test config."""
```

### Assertion Helpers

**`assert_journal_structure_valid(path)`** - Verify complete journal structure
**`assert_ide_config_installed(path, ide)`** - Verify IDE configs present
**`assert_config_valid(config_path)`** - Verify config file valid

## 🔬 Writing Good Tests

### Test Naming

Use descriptive names that explain the scenario:

```python
# ✅ Good
def test_setup_creates_parent_directory_when_no_confirm_is_set():
    """Test setup auto-creates parent directories with --no-confirm flag."""

# ❌ Bad
def test_setup_1():
    """Test setup."""
```

### AAA Pattern

Structure tests with Arrange-Act-Assert:

```python
def test_move_updates_config(temp_journal_dir, isolated_config):
    # Arrange: Set up test conditions
    create_journal_fixture(path=temp_journal_dir, ide="cursor", config_dir=isolated_config)
    new_location = tmp_path / "new-journal"
    
    # Act: Execute the operation
    runner = CliRunner()
    result = runner.invoke(app, ["move", str(new_location), "--no-confirm"])
    
    # Assert: Verify the outcome
    assert result.exit_code == 0
    config = load_config()
    assert config.journal_location == str(new_location)
```

### Isolation

Each test should be independent:

```python
# ✅ Good - Each test creates its own data
def test_setup_with_cursor(temp_journal_dir):
    create_journal_fixture(path=temp_journal_dir, ide="cursor")
    assert_ide_config_installed(temp_journal_dir, "cursor")

def test_setup_with_windsurf(temp_journal_dir):
    create_journal_fixture(path=temp_journal_dir, ide="windsurf")
    assert_ide_config_installed(temp_journal_dir, "windsurf")

# ❌ Bad - Tests depend on each other
def test_setup():
    create_journal_fixture(path=journal_path, ide="cursor")
    
def test_update():  # Assumes setup() ran first!
    result = runner.invoke(app, ["update"])
```

### Error Cases

Test both success and failure paths:

```python
def test_setup_succeeds_with_valid_path(temp_journal_dir):
    """Test setup succeeds with valid path."""
    result = runner.invoke(app, ["setup", str(temp_journal_dir), "--no-confirm"])
    assert result.exit_code == 0

def test_setup_fails_with_invalid_path():
    """Test setup fails gracefully with invalid path."""
    result = runner.invoke(app, ["setup", "/invalid/\0/path", "--no-confirm"])
    assert result.exit_code != 0
    assert "error" in result.output.lower()
```

## 🚀 CI/CD Integration

### GitHub Actions Matrix

Tests run on:
- **Python**: 3.10, 3.11, 3.12, 3.13
- **OS**: Ubuntu, macOS, Windows
- **Total**: 12 combinations

### CI Workflow

```yaml
- name: Run tests
  run: |
    pytest --cov=ai_journal_kit --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
```

### Local CI Simulation

Before pushing:

```bash
# Simulate full CI pipeline
invoke ci.local

# This runs:
# 1. Linting (ruff)
# 2. Security scan (bandit)
# 3. All tests with coverage
```

## 📈 Coverage Goals

- **Core business logic**: 80%+ (config, templates, validation)
- **CLI commands**: 60-80% (some paths hard to test)
- **Platform-specific**: Best effort (Windows junctions, etc.)
- **Overall**: 70%+

### Checking Coverage

```bash
# Generate HTML coverage report
invoke test.coverage

# Opens htmlcov/index.html in browser
# Shows line-by-line coverage
```

## 🐛 Debugging Tests

### Verbose Output

```bash
# Show print() statements
pytest -s

# Verbose test names
pytest -v

# Very verbose
pytest -vv

# Show local variables on failure
pytest -l
```

### Running Specific Tests

```bash
# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run all tests that failed last time
pytest --failed-first
```

### Debugging Fixtures

```python
# Print fixture value
def test_debug(temp_journal_dir):
    print(f"Journal dir: {temp_journal_dir}")
    print(f"Contents: {list(temp_journal_dir.iterdir())}")
    assert False  # Force failure to see output
```

## 🎯 Best Practices

1. **Fast Tests Win**: Unit > Integration > E2E for speed
2. **Test Behavior, Not Implementation**: Focus on what, not how
3. **Clear Error Messages**: Use descriptive assertions
4. **Fixtures Over Duplication**: Reuse setup code
5. **Mark Slow Tests**: Use `@pytest.mark.slow` for expensive tests
6. **Cross-Platform**: Test path handling, line endings, permissions
7. **Mock External Dependencies**: No real network, no real PyPI
8. **Cleanup**: Use fixtures for automatic cleanup
9. **Readable Tests**: Code should be obvious
10. **Update Tests**: When behavior changes, update tests

## 📚 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-xdist](https://pytest-xdist.readthedocs.io/) - Parallel execution
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Coverage reporting
- [pytest-bdd](https://pytest-bdd.readthedocs.io/) - BDD testing
- [Typer Testing](https://typer.tiangolo.com/tutorial/testing/) - CLI testing

## 🤝 Contributing Tests

When adding new features:

1. **Write tests first** (TDD) or alongside the code
2. **Cover happy path** and error cases
3. **Add integration test** if touching CLI/filesystem
4. **Update this guide** if introducing new patterns
5. **Run full suite** before submitting PR

---

**Questions?** Open an issue or discussion on GitHub!

