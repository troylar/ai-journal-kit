# Changelog

All notable changes to AI Journal Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.6] - 2025-11-07

### Fixed
- **Module packaging**: Added `__init__.py` files to `templates/` and `templates/ide-configs/` directories
  - Fixes "No module named 'ai_journal_kit.templates'" error during `update` command
  - Templates directory now properly recognized as a Python module
  - Ensures IDE configs can be refreshed during updates
- **Update command**: Fixed `show_success()` call with incorrect number of arguments
  - Corrected function call to pass only the message parameter
  - Resolves `TypeError: show_success() takes 1 positional argument but 2 were given`

## [1.0.5] - 2025-11-07

### Fixed
- **GitHub Copilot support**: Added complete AI coaching instructions for Copilot users
  - Main coaching instructions (`.github/copilot-instructions.md`)
  - Daily notes path-specific rules (`.github/instructions/daily-notes.instructions.md`)
  - System protection rules (`.github/instructions/system-protection.instructions.md`)
  - Previously only had system-protection, now has full coaching support

## [1.0.4] - 2025-11-07

### Added
- **Template updating**: `--templates` flag for update command to refresh templates with automatic backup
- **Beautiful new README**: Rich with emojis, clear value props, quick start
- **Template management module**: Check, update, backup, and restore templates

### Changed
- **README completely revamped**: More exciting, value-focused, privacy-first messaging
- **Emphasis on framework-agnostic nature**: Works with GTD, PARA, Bullet Journal, or your own system

## [1.0.3] - 2025-11-07

### Fixed
- **Update command**: Fixed package upgrade to use `pip install --upgrade` instead of non-existent `uvx --upgrade`
- **Changelog display**: Now fetches actual release notes from GitHub API instead of placeholder text

### Added
- **RELEASING.md**: Comprehensive release process documentation for maintainers

## [1.0.2] - 2025-11-07

### Fixed
- **Version string**: Fixed `__version__` in `__init__.py` to match package version

## [1.0.1] - 2025-11-07

### Fixed
- **Update command**: Now properly checks PyPI for latest version instead of always returning "Unable to check"

## [1.0.0] - 2025-11-07

### Added
- **Modern Python CLI** powered by `uv`, Typer, and Rich for beautiful terminal UI
- **`setup` command**: Interactive first-time setup with path validation and IDE selection
- **`status` command**: View journal health and configuration at a glance
- **`doctor` command**: Diagnose and auto-fix common issues
- **`update` command**: Safely update core system while preserving journal content
- **`move` command**: Relocate journal to different filesystem location
- **Cross-platform support**: Works seamlessly on macOS, Linux, and Windows
- **Multi-editor integration**: Built-in support for Cursor, Windsurf, Claude Code, and GitHub Copilot
- **Flexible journal location**: Store journal anywhere (local, Google Drive, Dropbox, etc.)
- **XDG-compliant config**: Uses platformdirs for proper config file storage
- **Comprehensive testing**: Unit + integration + E2E tests with 80%+ coverage
- **CI/CD pipelines**: Automated testing on all platforms via GitHub Actions

### Changed
- **Installation method**: Now installable via `uvx ai-journal-kit` from PyPI (replaces shell scripts)
- **Package structure**: Reorganized as proper Python package with clear module separation
- **Configuration management**: Config now stored in platform-specific locations (was: `.ai-journal-config.json` in repo)

### Deprecated
- Shell scripts (`setup.sh`, `update-core.sh`, `change-location.sh`) - replaced by Python CLI commands

### AI Behavior Changes
- No changes to AI coaching behavior in this release - all AI instructions preserved

### Migration Guide
See [MIGRATION.md](./MIGRATION.md) for upgrading from shell-script version to Python CLI.

---

## Format

### Version Headers
- **[Unreleased]**: Changes not yet released
- **[X.Y.Z] - YYYY-MM-DD**: Released versions with date

### Change Categories
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be-removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements
- **AI Behavior Changes**: Changes to default AI coaching personality or functionality

### AI Behavior Change Policy
Changes to AI coaching personality, tone, or core behavior MUST be documented under "AI Behavior Changes" section with:
1. Clear description of what changed
2. Rationale for the change
3. How users can opt-out or customize

[Unreleased]: https://github.com/troylar/ai-journal-kit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/troylar/ai-journal-kit/releases/tag/v1.0.0

