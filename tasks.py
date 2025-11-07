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
    """Publish to PyPI (requires PYPI_TOKEN env var).
    
    Args:
        test_pypi: If True, publish to test.pypi.org instead
    """
    # Build first
    build(c)
    
    # Publish
    if test_pypi:
        print("📦 Publishing to Test PyPI...")
        c.run("uv publish --index-url https://test.pypi.org/legacy/")
    else:
        print("📦 Publishing to PyPI...")
        c.run("uv publish")


# Create namespace
ns = Collection()
ns.add_task(clean)
ns.add_task(format)
ns.add_task(lint)
ns.add_task(check)
ns.add_collection(test_ns)
ns.add_task(build)
ns.add_task(publish)

