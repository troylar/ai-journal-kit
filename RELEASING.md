# Release Process for AI Journal Kit

This document describes the complete process for releasing a new version of AI Journal Kit to PyPI and GitHub.

## Prerequisites

Before you begin:

1. **PyPI Account**: Have accounts on both Test PyPI and Production PyPI
2. **API Tokens**: Generate API tokens for both environments
3. **Environment Variables**: Store tokens in `.env` file:
   ```bash
   TEST_PYPI_TOKEN="pypi-..."
   PYPI_TOKEN="pypi-..."
   ```
4. **Clean Working Directory**: Ensure all changes are committed

## Release Checklist

### 1. Determine Version Number

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (x.0.0): Breaking changes
- **MINOR** (1.x.0): New features, backward compatible
- **PATCH** (1.0.x): Bug fixes, backward compatible

### 2. Update Version Numbers

Update the version in **THREE** places:

```bash
# 1. pyproject.toml
version = "1.0.x"

# 2. ai_journal_kit/__init__.py
__version__ = "1.0.x"

# 3. CHANGELOG.md (add new section)
## [1.0.x] - YYYY-MM-DD
```

**⚠️ CRITICAL**: All three must match or users will see wrong version!

### 3. Update CHANGELOG.md

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [Unreleased]

## [1.0.x] - 2025-11-07

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

### 🛡️ AI Behavior Changes (if any)
- Document any changes to AI instructions or behavior
- This is CRITICAL per our constitution
```

**Important**: Be explicit about AI behavior changes!

### 4. Run Tests and Linting

```bash
# Lint and format
invoke lint
invoke format

# Run tests
invoke test

# Or run full check
invoke check
```

Fix any issues before proceeding.

### 5. Commit Version Bump

```bash
git add pyproject.toml ai_journal_kit/__init__.py CHANGELOG.md
git commit -m "chore: Bump version to v1.0.x"
git push origin main
```

### 6. Test on Test PyPI

**Always test first!**

```bash
# Load environment variables
export $(cat .env | xargs)

# Publish to Test PyPI
invoke publish --test-pypi
```

Verify the upload:
```bash
# Check Test PyPI page
open https://test.pypi.org/project/ai-journal-kit/

# Test installation
uvx --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    ai-journal-kit --version
```

### 7. Publish to Production PyPI

Once Test PyPI works:

```bash
# Load environment variables
export $(cat .env | xargs)

# Publish to Production
invoke publish
```

Verify:
```bash
# Check PyPI page
open https://pypi.org/project/ai-journal-kit/

# Wait 30 seconds for CDN propagation, then test
sleep 30
uvx ai-journal-kit@latest --version
```

### 8. Create Git Tag

```bash
# Create annotated tag
git tag -a v1.0.x -m "Release v1.0.x: Brief description

- Key feature 1
- Key feature 2
- Bug fix"

# Push tag (bypassing hook if needed)
git push origin v1.0.x --no-verify
```

### 9. Create GitHub Release

```bash
gh release create v1.0.x \
  --title "v1.0.x: Release Title" \
  --notes "# 🎉 Release v1.0.x

## ✨ What's New

- Feature 1
- Feature 2

## 🐛 Bug Fixes

- Fix 1
- Fix 2

## 🛡️ AI Behavior Changes

- None (or list changes)

## 📦 Installation

\`\`\`bash
uvx ai-journal-kit setup
\`\`\`

---

**Full Changelog**: https://github.com/troylar/ai-journal-kit/compare/v1.0.(x-1)...v1.0.x"
```

Or use the web interface: https://github.com/troylar/ai-journal-kit/releases/new

### 10. Post-Release Verification

```bash
# Verify PyPI has the new version
curl -s https://pypi.org/pypi/ai-journal-kit/json | jq -r '.info.version'

# Test clean install
pip install --user --force-reinstall --no-cache-dir ai-journal-kit
ai-journal-kit --version

# Test update command
ai-journal-kit update --check
```

### 11. Announce Release (Optional)

- Update README.md badges if needed
- Tweet/post about the release
- Update documentation site
- Notify users in discussions

## Troubleshooting

### PyPI Upload Fails

**Error: "File already exists"**
- You already published this version
- Bump version and try again
- Cannot delete or replace PyPI versions

**Error: "Invalid credentials"**
- Check your API token
- Verify it's not expired
- Ensure `UV_PUBLISH_TOKEN` is set correctly

### Version Mismatch

**Users report wrong version number**
- You forgot to update `__init__.py`
- Bump to next patch version
- Fix all three version locations
- Re-publish

### Update Command Shows "Unable to check"

**PyPI check failing**
- Verify package is on PyPI
- Check network connectivity
- Try again after CDN propagation (60 seconds)

## Version History Quick Reference

```bash
# See all published versions
curl -s https://pypi.org/pypi/ai-journal-kit/json | jq -r '.releases | keys[]'

# See latest version
curl -s https://pypi.org/pypi/ai-journal-kit/json | jq -r '.info.version'

# See all git tags
git tag -l

# See commits since last tag
git log v1.0.x..HEAD --oneline
```

## Emergency Rollback

If a release has critical bugs:

1. **Cannot unpublish from PyPI** - versions are permanent
2. **Options**:
   - Publish hotfix version (e.g., 1.0.x+1)
   - Update documentation warning about broken version
   - Use GitHub releases to mark version as broken

3. **Hotfix Process**:
   ```bash
   # Fix the bug
   # Bump to patch version
   # Follow full release process
   # Mark GitHub release as hotfix
   ```

## Best Practices

### DO

- ✅ Always test on Test PyPI first
- ✅ Update CHANGELOG.md before releasing
- ✅ Keep version numbers in sync
- ✅ Tag releases in git
- ✅ Write detailed release notes
- ✅ Test installation from PyPI
- ✅ Document AI behavior changes

### DON'T

- ❌ Skip Test PyPI
- ❌ Forget to update `__init__.py`
- ❌ Publish without testing
- ❌ Skip changelog updates
- ❌ Rush hotfixes without testing
- ❌ Hide AI behavior changes

## Automation Ideas (Future)

- GitHub Actions for automatic PyPI publishing on tag push
- Automated changelog generation from commits
- Version bump scripts
- Release note templates
- CI/CD pipeline for releases

## Questions?

Open a GitHub issue or discussion if you have questions about the release process.

---

**Remember**: Take your time. A delayed release is better than a broken one!

