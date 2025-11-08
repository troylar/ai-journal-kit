# Invoke Tasks Reference

Quick reference for all available `invoke` tasks for development, testing, and CI/CD.

## 📋 Quick Commands

```bash
# Most common workflows
invoke pre-commit      # Before committing (format + lint + security + quick tests)
invoke pre-push        # Before pushing (full checks + all tests)
invoke ci              # Simulate full CI pipeline locally
invoke test            # Run all tests with coverage
invoke test.quick      # Fast tests without coverage
```

---

## 🧪 Testing Tasks

### `invoke test` (default)
Run all tests with coverage reporting.
```bash
invoke test                    # All tests with coverage
invoke test --verbose          # Verbose output
invoke test --no-parallel      # Sequential execution (for debugging)
```

### `invoke test.unit`
Run only unit tests (fast, isolated tests).
```bash
invoke test.unit               # Run unit tests
invoke test.unit --verbose     # With verbose output
```

### `invoke test.integration`
Run integration tests (end-to-end workflows).
```bash
invoke test.integration        # Run integration tests
invoke test.integration -v     # With verbose output
```

### `invoke test.quick`
Fast test run without coverage (stops on first failure).
```bash
invoke test.quick              # Quick feedback loop
```

### `invoke test.coverage`
Generate HTML coverage report and open in browser.
```bash
invoke test.coverage           # Generate and open report
```

### `invoke test.watch`
Watch for file changes and auto-run tests.
```bash
invoke test.watch              # Continuous testing
```

---

## 🎨 Code Quality Tasks

### `invoke format`
Auto-format code with ruff.
```bash
invoke format                  # Format all code
```

### `invoke lint`
Check code style with ruff (doesn't modify files).
```bash
invoke lint                    # Check linting
```

### `invoke lint-fix`
Check and auto-fix linting issues.
```bash
invoke lint-fix                # Fix linting issues
```

---

## 🔒 Security Tasks

### `invoke security`
Run Bandit security scan.
```bash
invoke security                # Security scan with console output
```

### `invoke security-report`
Generate detailed JSON security report.
```bash
invoke security-report         # Creates bandit-report.json
```

---

## ✅ Pre-Commit/Push Checks

### `invoke pre-commit`
Run all checks before committing.
```bash
invoke pre-commit              # Format + lint + security + quick tests
```

**Runs:**
1. Format code
2. Lint check
3. Security scan
4. Quick tests (fast, stops on first failure)

**Use before:** `git commit`

### `invoke pre-push`
Run all checks before pushing.
```bash
invoke pre-push                # Format + lint + security + full tests
```

**Runs:**
1. Format code
2. Lint check
3. Security scan
4. Full test suite with coverage

**Use before:** `git push`

---

## 🚀 CI/CD Simulation

### `invoke ci` (default)
Simulate the full CI pipeline locally.
```bash
invoke ci                      # Run local CI simulation
invoke ci.local                # Same as above
```

**Simulates GitHub Actions:**
1. Linting
2. Security scan
3. Full test suite

### `invoke ci.matrix`
Show test matrix configuration.
```bash
invoke ci.matrix               # Display matrix info
```

Shows what runs in CI:
- Python versions: 3.10, 3.11, 3.12, 3.13
- OS platforms: Ubuntu, macOS, Windows
- Total: 12 combinations

### `invoke ci.check-workflows`
Validate GitHub Actions workflow YAML syntax.
```bash
invoke ci.check-workflows      # Validate workflow files
```

---

## 🏗️ Build & Publish

### `invoke check`
Run all quality checks (lint + security).
```bash
invoke check                   # Full quality check
```

### `invoke build`
Build the package (runs checks first).
```bash
invoke build                   # Build wheel and sdist
```

### `invoke publish`
Publish to PyPI.
```bash
# Set token first
export PYPI_TOKEN='pypi-...'

# Publish to PyPI
invoke publish

# Or publish to Test PyPI
export TEST_PYPI_TOKEN='pypi-...'
invoke publish --test-pypi
```

---

## 🧹 Maintenance

### `invoke clean`
Remove build artifacts and caches.
```bash
invoke clean                   # Clean all artifacts
```

Removes:
- `dist/`, `build/`, `*.egg-info/`
- `__pycache__/`, `*.pyc`
- `.coverage`, `coverage.xml`, `htmlcov/`
- `.pytest_cache/`
- `bandit-report.json`

---

## 🔄 Recommended Workflows

### Before Committing
```bash
invoke pre-commit
git add .
git commit -m "feat: your changes"
```

### Before Pushing
```bash
invoke pre-push
git push
```

### Daily Development
```bash
# Terminal 1: Watch mode for continuous feedback
invoke test.watch

# Terminal 2: Make changes
# Tests run automatically on save
```

### Before Creating PR
```bash
# Full local CI simulation
invoke ci

# If all passes, push and create PR
git push
```

### Debugging Failing Tests
```bash
# Quick tests with verbose output
invoke test.quick --verbose

# Or run specific test file
pytest tests/unit/test_cli_setup.py -v

# Or run with debugger
pytest tests/unit/test_cli_setup.py --pdb
```

---

## 📊 Coverage Analysis

```bash
# Generate and view coverage
invoke test.coverage

# Or manually
pytest --cov=ai_journal_kit --cov-report=html
open htmlcov/index.html  # macOS
# Or: xdg-open htmlcov/index.html  # Linux
# Or: start htmlcov/index.html     # Windows
```

---

## 🎯 Task Chaining

Tasks automatically run dependencies:

```bash
invoke check          # Runs: lint + security
invoke build          # Runs: check + build
invoke publish        # Runs: check + build + publish
```

---

## 💡 Tips & Tricks

### Stop on First Failure
```bash
pytest -x                      # Stop on first failure
invoke test.quick              # Already includes -x
```

### Parallel vs Sequential
```bash
pytest                         # Parallel (default, -n auto)
pytest --no-cov               # Sequential, no coverage
invoke test --no-parallel     # Sequential via invoke
```

### Verbose Output
```bash
invoke test --verbose          # Verbose test output
pytest -v                      # Direct pytest verbose
pytest -vv                     # Extra verbose
```

### Run Specific Tests
```bash
# By marker
pytest -m unit                 # Unit tests only
pytest -m integration          # Integration tests only

# By path
pytest tests/unit/            # All unit tests
pytest tests/unit/test_cli_setup.py  # Single file

# By name
pytest -k "test_validate"     # Tests matching name
```

---

## 🚨 Troubleshooting

### Linting Failures
```bash
# See what's wrong
invoke lint

# Auto-fix most issues
invoke lint-fix

# Check again
invoke lint
```

### Security Scan Failures
```bash
# See detailed report
invoke security-report
cat bandit-report.json

# Check specific severity levels
bandit -r ai_journal_kit/ -ll  # Low severity
bandit -r ai_journal_kit/ -lll # All issues
```

### Test Failures
```bash
# Run failing test with verbose output
pytest tests/unit/test_name.py -vv

# Run with print statements visible
pytest tests/unit/test_name.py -s

# Run with debugger
pytest tests/unit/test_name.py --pdb

# Show local variables on failure
pytest tests/unit/test_name.py --showlocals
```

---

## 📝 Task Summary Table

| Task | Speed | Use Case |
|------|-------|----------|
| `invoke test.quick` | ⚡ Fastest | Quick feedback during development |
| `invoke test.unit` | 🚀 Fast | Test specific components |
| `invoke pre-commit` | ⚡ Fast | Before every commit |
| `invoke test` | 🐢 Slow | Full test suite with coverage |
| `invoke pre-push` | 🐢 Slow | Before pushing to remote |
| `invoke ci` | 🐢 Slowest | Simulate full CI pipeline |

---

**Generated**: 2025-11-08  
**For**: ai-journal-kit development  
**See also**: `specs/002-testing-cicd-setup/quickstart.md`

