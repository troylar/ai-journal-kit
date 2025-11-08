# Local/CI Parity Guide

This guide explains how **local development commands exactly match CI/CD workflows**, giving you confidence that local tests will behave the same way in GitHub Actions.

---

## 🎯 The Goal: Perfect Parity

**Every CI/CD workflow uses `invoke` commands** - the same commands you run locally. This means:

✅ **No surprises** - If it passes locally, it passes in CI  
✅ **Faster debugging** - Reproduce CI failures locally  
✅ **Consistent behavior** - Same tools, same flags, same results

---

## 🔄 Workflow Mapping

### CI Lint Job → `invoke lint`

**GitHub Actions:**
```yaml
- run: invoke lint
- run: invoke format
```

**Local:**
```bash
invoke lint    # Exactly what CI runs
invoke format  # Exactly what CI runs
```

---

### CI Security Job → `invoke security`

**GitHub Actions:**
```yaml
- run: invoke security
- run: invoke security-report
```

**Local:**
```bash
invoke security         # Exactly what CI runs
invoke security-report  # Exactly what CI runs
```

---

### CI Test Job → `invoke test`

**GitHub Actions:**
```yaml
- run: invoke test --verbose
```

**Local:**
```bash
invoke test --verbose  # Exactly what CI runs
invoke test            # Same, without verbose
```

---

## 🚀 Simulate Full CI Pipeline Locally

### Option 1: One Command (Recommended)

```bash
invoke ci
```

This runs the **exact same sequence** as GitHub Actions:
1. Linting
2. Security scan
3. Full test suite

**Output shows each step** just like CI logs.

---

### Option 2: Step-by-Step (for debugging)

```bash
# Step 1: Linting (like lint job)
invoke lint

# Step 2: Security (like security job)
invoke security

# Step 3: Tests (like test job)
invoke test --verbose
```

---

## 🎯 Pre-Commit/Push Checks

### Before Committing

```bash
invoke pre-commit
```

**Runs:**
1. `invoke format` - Auto-format code
2. `invoke lint` - Check linting
3. `invoke security` - Security scan
4. `invoke test.quick` - Fast tests

**Same as CI** but skips full test suite for speed.

---

### Before Pushing

```bash
invoke pre-push
```

**Runs:**
1. `invoke format` - Auto-format code
2. `invoke lint` - Check linting
3. `invoke security` - Security scan
4. `invoke test` - Full test suite ✅

**Exactly what CI runs** - perfect parity!

---

## 📊 Command Comparison Table

| What You Want | Local Command | CI Workflow | Parity |
|---------------|---------------|-------------|--------|
| Check linting | `invoke lint` | `ci.yml → lint job` | ✅ 100% |
| Security scan | `invoke security` | `security.yml` | ✅ 100% |
| Run all tests | `invoke test` | `ci.yml → test job` | ✅ 100% |
| Full CI pipeline | `invoke ci` | All workflows | ✅ 100% |
| Pre-commit check | `invoke pre-commit` | N/A (local only) | - |
| Pre-push check | `invoke pre-push` | Full CI | ✅ 100% |

---

## 🔍 Debugging CI Failures

When CI fails, follow these steps:

### 1. Identify the Failing Job

Check GitHub Actions log to see which job failed:
- **lint** job → Run `invoke lint` locally
- **security** job → Run `invoke security` locally
- **test** job → Run `invoke test` locally

### 2. Reproduce Locally

```bash
# Run the exact command that failed
invoke lint          # If lint job failed
invoke security      # If security job failed
invoke test          # If test job failed
```

### 3. Fix and Verify

```bash
# Fix the issue, then run full CI simulation
invoke ci

# If that passes, you're good to push!
```

---

## 🎨 Format Checking in CI

CI checks if code is properly formatted:

**Local:**
```bash
# Auto-format (what you should run)
invoke format

# Check if formatted (what CI runs)
invoke format
git diff --exit-code  # Fails if any changes
```

**CI does both:**
1. Runs `invoke format`
2. Checks if any files changed
3. Fails if formatting is outdated

**To fix locally:**
```bash
invoke format
git add .
git commit -m "style: format code"
```

---

## 🧪 Test Matrix Differences

**CI runs tests on:**
- Python 3.10, 3.11, 3.12, 3.13
- Ubuntu, macOS, Windows
- Total: 12 combinations

**Local runs tests on:**
- Your Python version
- Your OS
- Total: 1 combination

**To simulate matrix locally:**
```bash
# Use Docker or virtual machines
# Or trust CI to test other platforms
```

**See matrix info:**
```bash
invoke ci.matrix
```

---

## ⚡ Speed Optimizations

### Fast Feedback Loop

```bash
# Fastest: Quick tests only
invoke test.quick

# Fast: Unit tests only
invoke test.unit

# Medium: All tests, no coverage
pytest --no-cov

# Slow: Full test suite with coverage
invoke test
```

### Watch Mode (Development)

```bash
# Auto-run tests on file changes
invoke test.watch
```

---

## 🔒 Security Scan Parity

### Local Security Scan

```bash
# Console output (what CI runs first)
invoke security

# Generate JSON report (what CI runs second)
invoke security-report

# Check report (what CI runs third)
cat bandit-report.json | grep HIGH
```

### CI Security Scan

```yaml
- run: invoke security          # Step 1
- run: invoke security-report   # Step 2
- run: grep "HIGH" bandit-report.json  # Step 3
```

**Same commands, same results!**

---

## 📦 Build & Publish Parity

### Local Build

```bash
# Runs: check → build
invoke build
```

### CI Build (future)

```yaml
# Will run: invoke build
- run: invoke build
```

**Parity maintained** for future release workflows.

---

## 💡 Best Practices

### ✅ DO

```bash
# Run pre-push before pushing
invoke pre-push
git push

# Simulate CI locally when debugging
invoke ci

# Use invoke commands, not direct pytest/ruff
invoke test     # ✅ Good
invoke lint     # ✅ Good
```

### ❌ DON'T

```bash
# Don't use raw commands if invoke version exists
pytest          # ❌ Might differ from CI
ruff check .    # ❌ Might differ from CI

# Use invoke instead
invoke test     # ✅ Same as CI
invoke lint     # ✅ Same as CI
```

---

## 🔧 Troubleshooting

### "Works locally but fails in CI"

**Possible causes:**
1. **Different Python version** - CI tests 3.10-3.13, you might have different version
2. **Platform difference** - CI tests Ubuntu/macOS/Windows
3. **Env differences** - CI runs in clean environment

**Solutions:**
```bash
# Run in clean environment
python -m venv clean_test
source clean_test/bin/activate
pip install -e ".[dev]"
invoke ci
```

### "CI passes but I want to verify locally"

```bash
# Run exact CI simulation
invoke ci

# Or step by step
invoke lint
invoke security
invoke test --verbose
```

---

## 📝 CI Workflow Files

All workflows use invoke commands:

### `.github/workflows/ci.yml`
```yaml
jobs:
  lint:
    - run: invoke lint          # ← invoke command
  security:
    - run: invoke security      # ← invoke command
  test:
    - run: invoke test          # ← invoke command
```

### `.github/workflows/security.yml`
```yaml
jobs:
  bandit:
    - run: invoke security       # ← invoke command
    - run: invoke security-report # ← invoke command
```

---

## 🎯 Quick Reference

| Scenario | Command | CI Equivalent |
|----------|---------|---------------|
| Check before commit | `invoke pre-commit` | Partial CI |
| Check before push | `invoke pre-push` | Full CI |
| Simulate CI | `invoke ci` | All workflows |
| Lint check | `invoke lint` | `ci.yml → lint` |
| Security scan | `invoke security` | `security.yml` |
| Run tests | `invoke test` | `ci.yml → test` |
| Quick test | `invoke test.quick` | N/A |
| Fix linting | `invoke lint-fix` | N/A |

---

## 🚀 Recommended Workflow

```bash
# 1. Make changes
# ... edit code ...

# 2. Run tests in watch mode (optional)
invoke test.watch  # Terminal 1

# 3. Before committing
invoke pre-commit
git add .
git commit -m "feat: your changes"

# 4. Before pushing
invoke pre-push

# 5. Push (CI will run same commands)
git push
```

---

**Result**: If `invoke pre-push` passes locally, CI will pass too! 🎉

---

**Generated**: 2025-11-08  
**For**: ai-journal-kit development  
**See also**: `INVOKE_TASKS.md`, `specs/002-testing-cicd-setup/quickstart.md`

