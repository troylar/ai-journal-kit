# v1.1.1 - Framework Placeholder Fix & Setup UX Improvements

## 🔥 Critical Fixes

### Framework Placeholder Replacement Bug
**CRITICAL**: Fixed {framework} placeholder not being replaced in IDE configuration files
- IDE config files (CLAUDE.md, Cursor rules, Windsurf rules, Copilot instructions) now show actual framework name instead of literal `{framework}` text
- Users who set up journals with specific frameworks (GTD, PARA, Bullet Journal, Zettelkasten) will now see the correct framework name in their IDE coaching instructions
- Applied to all IDEs: Cursor, Windsurf, Claude Code, and GitHub Copilot
- Updated `copy_ide_configs()` to accept framework parameter and perform placeholder replacement
- Updated all 5 callers (setup, update, doctor, add-ide commands, and test fixtures) to pass framework parameter

### Version Tracking Bug
Fixed hardcoded version "1.0.0" in journal profiles and manifests
- Journal profiles now store actual package version (e.g., "1.1.1") instead of hardcoded "1.0.0"
- Manifest files now use actual package version for better tracking
- Updated setup.py and migration.py to use `__version__` instead of hardcoded strings
- Enables proper version tracking for future migrations and compatibility checks

## ✨ Enhancements

### Enhanced Setup Command for Existing Journals
Better messaging and confirmation when running setup on existing journal locations

**New Detection Capabilities:**
- Automatically detects all existing journal content:
  - Journal folders (daily, projects, people, memories, areas, resources, archive)
  - IDE configurations (Cursor, Windsurf, Claude Code, GitHub Copilot)
  - Template files
  - User customizations (.ai-instructions/)

**Improved User Experience:**
- Clear warning panel showing what content was detected at the location
- Explains what will happen if user proceeds with re-installation
- Offers to keep existing IDE configuration or choose a new one
- Provides helpful guidance if user decides to cancel
- Setup now shows "update" instead of "create" message when reinstalling
- Clear confirmation prompts: "Proceed with re-installation at this location?"
- Better --no-confirm mode handling with appropriate warnings

**Benefits:**
- Prevents accidental data loss from running setup on existing journals
- Makes it clearer when setup is updating vs. creating new
- Helps users who may have forgotten they changed their journal path
- Reduces confusion and support requests

## 🧪 Testing Improvements

### Comprehensive Test Coverage
- **Added 33 new tests** (458 → 491 total tests)
- All 491 tests passing on macOS, Linux, and Windows
- 100% code formatting and linting compliance

### New Test Suites

**Unit Tests (23 new):**
- 16 tests for `_detect_existing_journal()`:
  - Empty directory detection
  - Journal folder detection (all 7 folders)
  - IDE configuration detection (all 4 IDEs)
  - Template file detection
  - User customizations detection
  - Comprehensive multi-content detection
  - Edge cases (nonexistent paths, mixed content, random files)

- 7 tests for `_handle_existing_journal()`:
  - No-confirm mode behavior
  - User confirmation flows (proceed/cancel)
  - Message content verification
  - IDE name formatting
  - Cancel guidance messaging

**Integration Tests (10 new):**
- Existing journal content detection and warning
- IDE choice offering and handling
- Framework placeholder replacement verification (all 5 frameworks)
- Actual version storage verification
- Reinstall message clarity ("update" vs "create")
- Multiple IDE configuration detection
- Customization preservation messaging

### Cross-Platform Testing
All 491 tests passing on:
- ✅ Ubuntu
- ✅ macOS
- ✅ Windows

## 📦 Installation

```bash
pip install --upgrade ai-journal-kit
```

Or using uvx:

```bash
uvx --force ai-journal-kit@latest
```

## 🔗 Links

- [PyPI Package](https://pypi.org/project/ai-journal-kit/1.1.1/)
- [Full Changelog](https://github.com/troylar/ai-journal-kit/blob/main/CHANGELOG.md)
- [Documentation](https://github.com/troylar/ai-journal-kit#readme)

## 🙏 Acknowledgments

This patch release fixes critical bugs that affected IDE configuration readability and improves the setup experience for users working with existing journals.

---

> **Note**: GTD® and Getting Things Done® are registered trademarks of David Allen Company. Bullet Journal® is a registered trademark of Ryder Carroll. PARA™ is a methodology by Tiago Forte. AI Journal Kit provides compatible templates and is not affiliated with these trademark holders.
