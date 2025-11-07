# Changelog

All notable changes to AI Journal Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - TBD

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

