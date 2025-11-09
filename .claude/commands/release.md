# Release Workflow

Automate the AI Journal Kit release process following RELEASING.md workflow.

## Usage
/release [version] [--test-pypi]

## Arguments
- version: Version number (e.g., 1.0.11, 2.0.0)
- --test-pypi: Publish to test PyPI first (recommended)

## Examples
/release 1.0.11 --test-pypi
/release 2.0.0

## Implementation Steps

### Pre-release Checks
1. Verify on `main` branch: `git branch --show-current`
   - If not on main, ERROR and exit
2. Verify clean working tree: `git status`
   - If uncommitted changes exist, ERROR and exit
3. Run full CI locally: `invoke ci.local`
   - If any checks fail, ERROR and exit

### Version Bump
1. Update version in `pyproject.toml`:
   - Find line with `version = "x.x.x"`
   - Replace with new version number
2. Update version in `ai_journal_kit/__init__.py`:
   - Find line with `__version__ = "x.x.x"`
   - Replace with new version number
3. Verify versions match: `grep -n "version" pyproject.toml ai_journal_kit/__init__.py`
   - Show both lines to confirm they match

### Changelog & Commit
1. Update CHANGELOG.md with release notes:
   - Run `git log --oneline` to see recent commits since last release
   - Group changes by type:
     - **Features**: feat() commits
     - **Fixes**: fix() commits
     - **Tests**: test() commits
     - **Documentation**: docs() commits
     - **Chores**: chore() commits
   - Add new section at top of CHANGELOG.md:
     ```
     ## [version] - YYYY-MM-DD

     ### Features
     - Feature 1
     - Feature 2

     ### Fixes
     - Fix 1

     ### Tests
     - Test improvements
     ```
2. Commit changes: `git add -A && git commit -m "chore: bump version to [version]"`
3. Create git tag: `git tag v[version]`

### Build & Publish
1. Clean previous builds: `invoke clean`
2. Build package: `invoke build`
3. If --test-pypi flag:
   - Check if TEST_PYPI_TOKEN env var exists
   - Publish to test PyPI: `invoke publish --test-pypi`
   - Verify: `uvx --from ai-journal-kit@latest --index-url https://test.pypi.org/simple/ ai-journal-kit --version`
   - Ask user to confirm before proceeding to production PyPI
4. Check if PYPI_TOKEN env var exists
5. Publish to PyPI: `invoke publish`
6. Verify: `uvx ai-journal-kit --version`

### Push & GitHub Release
1. Push to GitHub: `git push && git push --tags`
2. Extract changelog for this version from CHANGELOG.md
3. Create GitHub release using `gh`:
   ```bash
   gh release create v[version] \
     --title "v[version]" \
     --notes "[extracted changelog notes]"
   ```

### Post-release
1. Show summary with:
   - PyPI link: https://pypi.org/project/ai-journal-kit/[version]/
   - GitHub release link
   - Installation command: `uvx ai-journal-kit@[version]`
2. Remind to announce on GitHub Discussions

## Safety Checks
- MUST be on main branch
- MUST have clean working tree
- MUST pass all CI checks locally
- MUST confirm before publishing to production PyPI
- MUST have PYPI_TOKEN environment variable set
- If --test-pypi, MUST have TEST_PYPI_TOKEN set

## Error Handling
If any step fails, stop immediately and show:
- What failed
- Why it failed
- How to fix it
- Do NOT continue with subsequent steps
