# Research: Integration & E2E Test Suite

**Feature**: Integration & E2E Test Suite  
**Branch**: `001-e2e-tests`  
**Date**: 2025-01-08

## Testing Framework Selection

### Decision: pytest with pytest-bdd for BDD-style tests

**Rationale**:
- Already used in project (see `tests/unit/` and `tests/integration/`)
- Excellent fixtures support for test isolation
- pytest-bdd enables Gherkin-style Given/When/Then acceptance tests
- Rich plugin ecosystem (pytest-xdist for parallelization, pytest-cov for coverage)
- Mature and well-documented

**Alternatives Considered**:
- **unittest**: Python stdlib, no dependencies, but less expressive fixtures
- **behave**: Pure BDD framework, but less integration with existing pytest infrastructure
- **Robot Framework**: Keyword-driven, but overkill for this project and learning curve too steep

**Best Practices**:
- Use fixtures for setup/teardown of temporary journal environments
- Isolate each test with unique temporary directories
- Use parametrize for cross-platform test variations
- Mark tests appropriately (`@pytest.mark.e2e`, `@pytest.mark.integration`)

---

## CLI Testing Approach

### Decision: Subprocess invocation with Click testing utilities

**Rationale**:
- Project uses Typer (built on Click) for CLI
- Click provides `CliRunner` for testing CLI commands in-process
- For true e2e tests, use subprocess to test actual installed command
- Combine both: unit tests with CliRunner, e2e tests with subprocess

**Alternatives Considered**:
- **Direct function calls**: Too unit-test-like, doesn't test CLI parsing
- **Pexpect**: Good for interactive testing, but overkill for our non-interactive commands
- **Subprocess only**: Slower, but more realistic for e2e scenarios

**Best Practices**:
- Integration tests: Use `CliRunner` for faster feedback
- E2E tests: Use subprocess with installed package for realistic scenarios
- Mock file I/O at unit level, real file I/O at integration/e2e level
- Capture and assert on stdout/stderr for user-facing messages

---

## Test Isolation Strategy

### Decision: Temporary directories with pytest tmpdir/tmp_path fixtures

**Rationale**:
- pytest provides `tmp_path` fixture (pathlib.Path) and `tmpdir` fixture (legacy py.path)
- Automatic cleanup after test completion
- Unique directory per test prevents cross-test contamination
- Can create realistic journal structures in isolation

**Alternatives Considered**:
- **tempfile.TemporaryDirectory**: Manual management, pytest fixtures cleaner
- **Shared test directories**: Risk of test interference, harder to debug
- **Docker containers**: Overkill for file system testing, slower

**Best Practices**:
- Create factory fixtures that return pre-configured journal environments
- Use `monkeypatch` to override config paths for test isolation
- Mock platform-specific operations (symlinks, junctions) when testing cross-platform

---

## Cross-Platform Testing

### Decision: GitHub Actions matrix with Windows, macOS, Linux runners

**Rationale**:
- Project already has CI/CD (`invoke ci`)
- GitHub Actions provides free runners for all three platforms
- Matrix strategy enables parallel execution across OS versions
- Can test actual platform-specific code (symlinks vs junctions)

**Alternatives Considered**:
- **Tox**: Good for Python version testing, but doesn't solve OS testing
- **Local VMs**: Expensive, slow, requires manual management
- **Docker**: Good for Linux variants, doesn't help with Windows/macOS

**Best Practices**:
- Use `sys.platform` checks to skip platform-specific tests
- Parametrize tests with platform-specific expectations
- Test symlink creation on Unix, junction creation on Windows
- Use `pytest.mark.skipif` for platform-specific test skipping

---

## Test Data Management

### Decision: Factory fixtures with realistic journal structures

**Rationale**:
- Need reproducible journal configurations for testing
- Fixtures provide reusable setup code
- Can create variations: empty journal, journal with content, corrupted journal

**Alternatives Considered**:
- **Fixtures from files**: Less flexible, harder to maintain
- **Database seeding**: Not applicable (no database)
- **Hand-crafted in each test**: Duplicate code, maintenance burden

**Best Practices**:
- Create `conftest.py` with shared fixtures
- Fixture factory pattern: `create_journal(path, config)` returns configured journal
- Use `@pytest.fixture(scope="function")` for isolation
- Provide fixtures for common scenarios: fresh install, existing journal, corrupted state

---

## Assertion Strategy

### Decision: Pytest assertions with custom helpers for journal validation

**Rationale**:
- Pytest rewrites assertions for rich failure messages
- Can create domain-specific assertion helpers
- Clear, readable test code

**Best Practices**:
- Create helpers: `assert_journal_structure_valid(path)`, `assert_ide_config_installed(path, ide)`
- Use `assert` with descriptive messages
- Leverage pytest's introspection for clear failure output

---

## Mocking Strategy

### Decision: Minimal mocking - prefer real file I/O for integration tests

**Rationale**:
- Integration/e2e tests should exercise real code paths
- Use `unittest.mock` only for external dependencies (network, user input)
- Real file operations in tmpdir are fast enough

**Alternatives Considered**:
- **Heavy mocking**: Defeats purpose of integration testing
- **No mocking**: Can't test user interaction, external services

**Best Practices**:
- Mock user input with `mock.patch` on `input()`, `confirm()`, `ask_path()`
- Mock network calls (if update checks remote version)
- Don't mock file system operations in integration tests
- Use `monkeypatch` for environment variables, config paths

---

## Test Organization

### Decision: Mirror existing structure - `tests/integration/` and `tests/e2e/`

**Rationale**:
- Project already has `tests/unit/` and `tests/integration/`
- Add `tests/e2e/` for true end-to-end scenarios
- Clear separation of concerns

**Structure**:
```
tests/
├── unit/               # Existing unit tests
├── integration/        # Expand with new integration tests
│   ├── test_setup_flow.py
│   ├── test_update_flow.py
│   ├── test_move_flow.py
│   └── conftest.py    # Shared fixtures
└── e2e/                # NEW: True end-to-end tests
    ├── test_complete_setup.py
    ├── test_update_preserves_data.py
    └── conftest.py
```

**Best Practices**:
- Integration tests: Use CliRunner, test command logic
- E2E tests: Use subprocess, test installed package
- Share fixtures via `conftest.py` at appropriate levels

---

## CI/CD Integration

### Decision: Extend existing `invoke ci` with integration/e2e test stages

**Rationale**:
- Project uses `invoke` for task automation
- Already has `invoke test`, `invoke lint`, `invoke ci`
- Add new targets: `invoke test-integration`, `invoke test-e2e`, `invoke test-all`

**Best Practices**:
- Run unit tests first (fast feedback)
- Run integration tests next (medium speed)
- Run e2e tests last (slowest, most comprehensive)
- Allow running subsets: `invoke test-integration` for faster iteration
- Full `invoke ci` runs everything

---

## Performance Considerations

### Decision: Parallel test execution with pytest-xdist

**Rationale**:
- Integration/e2e tests are slower (real file I/O)
- pytest-xdist enables parallel execution across CPU cores
- Already used in project (see `pytest -n auto`)

**Best Practices**:
- Use `-n auto` to detect CPU cores
- Ensure test isolation (no shared state)
- Add `@pytest.mark.serial` for tests that must run sequentially

---

## Documentation

### Decision: Add testing guide to repository documentation

**Rationale**:
- Developers need to understand how to run and write tests
- Contributors need examples for adding new test coverage

**Content**:
- How to run different test levels (unit, integration, e2e)
- How to write new integration tests
- Fixture patterns and examples
- Cross-platform testing considerations
- CI/CD integration

---

## Summary of Technical Decisions

| Decision Point | Choice | Key Rationale |
|----------------|--------|---------------|
| Test Framework | pytest + pytest-bdd | Already used, great fixtures, BDD support |
| CLI Testing | CliRunner + subprocess | Balance between speed and realism |
| Test Isolation | pytest tmp_path fixtures | Automatic cleanup, unique per test |
| Cross-Platform | GitHub Actions matrix | Free runners, parallel execution |
| Mocking | Minimal - real file I/O | Integration tests should be realistic |
| Test Organization | tests/integration/ + tests/e2e/ | Clear separation, mirrors existing structure |
| CI/CD | Extend invoke tasks | Consistent with project patterns |
| Parallelization | pytest-xdist | Speed up slow integration/e2e tests |

