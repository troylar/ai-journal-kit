"""Invoke tasks for development automation."""

import sys

from invoke import Collection, task


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
        "htmlcov/",
        ".pytest_cache/",
    ]
    for pattern in patterns:
        if sys.platform == "win32":
            c.run(f'if exist {pattern} rmdir /s /q {pattern}', warn=True)
        else:
            c.run(f"rm -rf {pattern}", warn=True)


@task
def format(c):
    """Format code with ruff."""
    c.run("ruff format ai_journal_kit tests")


@task
def lint(c):
    """Lint code with ruff."""
    c.run("ruff check ai_journal_kit tests")


@task(lint)
def check(c):
    """Run all checks (lint + type check)."""
    print("✅ All checks passed")


# Test namespace
test_ns = Collection("test")


@task
def unit(c):
    """Run unit tests only (fast)."""
    c.run("pytest -m unit -v")


@task
def integration(c):
    """Run integration tests."""
    c.run("pytest -m integration -v")


@task
def e2e(c):
    """Run end-to-end tests (slow)."""
    c.run("pytest -m e2e -v")


@task
def all(c):
    """Run all tests with coverage."""
    c.run("pytest")


test_ns.add_task(unit)
test_ns.add_task(integration)
test_ns.add_task(e2e)
test_ns.add_task(all)


@task(check)
def build(c):
    """Build package."""
    print("🏗️  Building package...")
    c.run("uv build")
    print("✅ Build complete!")


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
            print("❌ Error: TEST_PYPI_TOKEN environment variable not set")
            print("Set it with: export TEST_PYPI_TOKEN='pypi-...'")
            return
        print("📦 Publishing to Test PyPI...")
        # Use single quotes for password with special characters
        c.run(f"UV_PUBLISH_TOKEN='{token}' uv publish --publish-url https://test.pypi.org/legacy/")
    else:
        token = os.getenv("PYPI_TOKEN")
        if not token:
            print("❌ Error: PYPI_TOKEN environment variable not set")
            print("Set it with: export PYPI_TOKEN='pypi-...'")
            return
        print("📦 Publishing to PyPI...")
        # Use single quotes for password with special characters
        c.run(f"UV_PUBLISH_TOKEN='{token}' uv publish")


# Create namespace
ns = Collection()
ns.add_task(clean)
ns.add_task(format)
ns.add_task(lint)
ns.add_task(check)
ns.add_collection(test_ns)
ns.add_task(build)
ns.add_task(publish)

