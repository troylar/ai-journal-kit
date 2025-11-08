"""Invoke tasks for development automation."""

import sys

from invoke import Collection, task


def safe_print(message: str):
    """Print message with fallback for Windows encoding issues."""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version on Windows
        ascii_message = message.encode('ascii', 'ignore').decode('ascii')
        print(ascii_message)


@task
def clean(c):
    """Clean build artifacts and caches."""
    patterns = [
        "dist/",
        "build/",
        "*.egg-info/",
        "**/__pycache__/",
        "**/*.pyc",
        ".coverage",
        "coverage.xml",
        "htmlcov/",
        ".pytest_cache/",
        "bandit-report.json",
    ]
    for pattern in patterns:
        if sys.platform == "win32":
            c.run(f'if exist {pattern} rmdir /s /q {pattern}', warn=True)
        else:
            c.run(f"rm -rf {pattern}", warn=True)
    safe_print("✨ Cleaned build artifacts and caches")


@task
def format(c):
    """Format code with ruff."""
    safe_print("🎨 Formatting code...")
    c.run("ruff format ai_journal_kit tests")
    safe_print("✅ Code formatted!")


@task
def lint(c):
    """Lint code with ruff."""
    safe_print("🔍 Linting code...")
    c.run("ruff check ai_journal_kit tests")
    safe_print("✅ Linting passed!")


@task
def lint_fix(c):
    """Lint and auto-fix issues."""
    safe_print("🔧 Linting and auto-fixing...")
    c.run("ruff check ai_journal_kit tests --fix")
    safe_print("✅ Issues fixed!")


@task
def security(c):
    """Run security scan with Bandit."""
    safe_print("🔒 Running security scan...")
    c.run("bandit -r ai_journal_kit/ -c .bandit")
    safe_print("✅ Security scan complete!")


@task
def security_report(c):
    """Generate detailed security report."""
    safe_print("🔒 Generating security report...")
    c.run("bandit -r ai_journal_kit/ -c .bandit -f json -o bandit-report.json")
    safe_print("✅ Report saved to bandit-report.json")


@task(lint, security)
def check(c):
    """Run all checks (lint + security)."""
    safe_print("✅ All checks passed!")


# Test namespace
test_ns = Collection("test")


@task
def unit(c, verbose=False):
    """Run unit tests only (fast).
    
    Args:
        verbose: Show verbose output
    """
    safe_print("🧪 Running unit tests...")
    cmd = "pytest tests/unit/"
    if verbose:
        cmd += " -v"
    c.run(cmd)


@task
def integration(c, verbose=False):
    """Run integration tests.
    
    Args:
        verbose: Show verbose output
    """
    safe_print("🧪 Running integration tests...")
    cmd = "pytest tests/integration/"
    if verbose:
        cmd += " -v"
    c.run(cmd)


@task
def e2e(c, verbose=False):
    """Run end-to-end tests.
    
    Args:
        verbose: Show verbose output
    """
    safe_print("🧪 Running e2e tests...")
    cmd = "pytest tests/e2e/"
    if verbose:
        cmd += " -v"
    c.run(cmd)


@task
def all(c, verbose=False, parallel=True):
    """Run all tests with coverage.
    
    Args:
        verbose: Show verbose output
        parallel: Run tests in parallel (default: True)
    """
    safe_print("🧪 Running all tests with coverage...")
    cmd = "pytest"
    if verbose:
        cmd += " -v"
    if not parallel:
        cmd += " --no-cov"  # Disable parallel for debugging
    c.run(cmd)
    safe_print("✅ All tests complete!")


@task
def quick(c):
    """Run tests without coverage (faster)."""
    safe_print("⚡ Running quick tests...")
    c.run("pytest --no-cov -x")


@task
def coverage(c):
    """Generate and open HTML coverage report."""
    safe_print("📊 Generating coverage report...")
    c.run("pytest --cov=ai_journal_kit --cov-report=html")
    safe_print("📂 Opening coverage report...")
    if sys.platform == "darwin":
        c.run("open htmlcov/index.html")
    elif sys.platform == "win32":
        c.run("start htmlcov/index.html")
    else:
        c.run("xdg-open htmlcov/index.html")


@task
def watch(c):
    """Watch for changes and run tests automatically."""
    safe_print("👀 Watching for changes...")
    try:
        c.run("pytest-watch --clear --onpass 'echo ✅ Tests passed' --onfail 'echo ❌ Tests failed'")
    except KeyboardInterrupt:
        safe_print("\n👋 Stopped watching")


test_ns.add_task(unit)
test_ns.add_task(integration)
test_ns.add_task(e2e)
test_ns.add_task(all, default=True)
test_ns.add_task(quick)
test_ns.add_task(coverage)
test_ns.add_task(watch)


# CI/CD namespace
ci_ns = Collection("ci")


@task
def local(c):
    """Simulate CI pipeline locally (lint + security + tests)."""
    safe_print("🚀 Running local CI simulation...")
    safe_print("\n" + "="*60)
    safe_print("STEP 1: Linting")
    safe_print("="*60)
    try:
        lint(c)
    except Exception as e:
        print(f"❌ Linting failed: {e}")
        return

    safe_print("\n" + "="*60)
    safe_print("STEP 2: Security Scan")
    safe_print("="*60)
    try:
        security(c)
    except Exception as e:
        print(f"❌ Security scan failed: {e}")
        return

    safe_print("\n" + "="*60)
    safe_print("STEP 3: Tests")
    safe_print("="*60)
    try:
        all(c)
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return

    safe_print("\n" + "="*60)
    safe_print("✅ ALL CI CHECKS PASSED!")
    safe_print("="*60)


@task
def matrix(c):
    """Show test matrix info (would run in CI)."""
    safe_print("🔀 Test Matrix Configuration:")
    safe_print("\nPython Versions:")
    safe_print("  - 3.10")
    safe_print("  - 3.11")
    safe_print("  - 3.12")
    safe_print("  - 3.13")
    safe_print("\nOperating Systems:")
    safe_print("  - ubuntu-latest")
    safe_print("  - macos-latest")
    safe_print("  - windows-latest")
    safe_print("\nTotal Combinations: 12")
    safe_print("\nTo run locally: invoke test")


@task
def check_workflows(c):
    """Validate GitHub Actions workflow syntax."""
    safe_print("🔍 Checking workflow files...")
    from pathlib import Path

    import yaml

    workflows_dir = Path(".github/workflows")
    if not workflows_dir.exists():
        safe_print("❌ No .github/workflows directory found")
        return

    for workflow_file in workflows_dir.glob("*.yml"):
        print(f"  Checking {workflow_file.name}...")
        try:
            with open(workflow_file) as f:
                yaml.safe_load(f)
            print("    ✅ Valid YAML")
        except Exception as e:
            print(f"    ❌ Invalid: {e}")
            return

    safe_print("\n✅ All workflow files are valid!")


ci_ns.add_task(local, default=True)
ci_ns.add_task(matrix)
ci_ns.add_task(check_workflows)


@task
def pre_commit(c):
    """Run all pre-commit checks (format, lint, security, quick test)."""
    safe_print("🎯 Running pre-commit checks...")

    safe_print("\n1️⃣  Formatting code...")
    format(c)

    safe_print("\n2️⃣  Linting...")
    try:
        lint(c)
    except Exception:
        safe_print("❌ Linting failed. Run 'invoke lint-fix' to auto-fix issues.")
        return

    safe_print("\n3️⃣  Security scan...")
    try:
        security(c)
    except Exception:
        safe_print("❌ Security scan found issues.")
        return

    safe_print("\n4️⃣  Quick tests...")
    try:
        quick(c)
    except Exception:
        safe_print("❌ Tests failed.")
        return

    safe_print("\n" + "="*60)
    safe_print("✅ ALL PRE-COMMIT CHECKS PASSED! Safe to commit.")
    safe_print("="*60)


@task
def pre_push(c):
    """Run all checks before pushing (includes full test suite)."""
    safe_print("🚀 Running pre-push checks...")

    safe_print("\n1️⃣  Formatting...")
    format(c)

    safe_print("\n2️⃣  Linting...")
    try:
        lint(c)
    except Exception:
        safe_print("❌ Linting failed. Run 'invoke lint-fix' to auto-fix.")
        return

    safe_print("\n3️⃣  Security scan...")
    try:
        security(c)
    except Exception:
        safe_print("❌ Security scan found issues.")
        return

    safe_print("\n4️⃣  Full test suite...")
    try:
        all(c)
    except Exception:
        safe_print("❌ Tests failed.")
        return

    safe_print("\n" + "="*60)
    safe_print("✅ ALL PRE-PUSH CHECKS PASSED! Safe to push.")
    safe_print("="*60)


@task(check)
def build(c):
    """Build package."""
    safe_print("🏗️  Building package...")
    c.run("uv build")
    safe_print("✅ Build complete!")


@task(check)
def publish(c, test_pypi=False):
    """Publish to PyPI (requires PYPI_TOKEN or TEST_PYPI_TOKEN env var).
    
    Args:
        test_pypi: If True, publish to test.pypi.org instead
    """
    import os

    # Build first
    build(c)

    # Get token from environment
    if test_pypi:
        token = os.getenv("TEST_PYPI_TOKEN")
        if not token:
            safe_print("❌ Error: TEST_PYPI_TOKEN environment variable not set")
            safe_print("Set it with: export TEST_PYPI_TOKEN='pypi-...'")
            return
        safe_print("📦 Publishing to Test PyPI...")
        # Use single quotes for password with special characters
        c.run(f"UV_PUBLISH_TOKEN='{token}' uv publish --publish-url https://test.pypi.org/legacy/")
    else:
        token = os.getenv("PYPI_TOKEN")
        if not token:
            safe_print("❌ Error: PYPI_TOKEN environment variable not set")
            safe_print("Set it with: export PYPI_TOKEN='pypi-...'")
            return
        safe_print("📦 Publishing to PyPI...")
        # Use single quotes for password with special characters
        c.run(f"UV_PUBLISH_TOKEN='{token}' uv publish")


# Create namespace
ns = Collection()
ns.add_task(clean)
ns.add_task(format)
ns.add_task(lint)
ns.add_task(lint_fix)
ns.add_task(security)
ns.add_task(security_report)
ns.add_task(check)
ns.add_task(pre_commit)
ns.add_task(pre_push)
ns.add_collection(test_ns)
ns.add_collection(ci_ns)
ns.add_task(build)
ns.add_task(publish)

