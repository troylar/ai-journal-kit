# Changelog

All notable changes to AI Journal Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Note**: GTD® and Getting Things Done® are registered trademarks of David Allen Company. Bullet Journal® is a registered trademark of Ryder Carroll. PARA™ is a methodology by Tiago Forte. AI Journal Kit provides compatible templates and is not affiliated with these trademark holders.

## [Unreleased]

## [1.1.1] - 2025-11-09

### Fixed
- **CRITICAL: Framework placeholder replacement bug**: Fixed {framework} placeholder not being replaced in IDE configuration files
  - IDE config files (CLAUDE.md, Cursor rules, Windsurf rules, Copilot instructions) now show actual framework name instead of literal `{framework}` text
  - Applied to all IDEs: Cursor, Windsurf, Claude Code, and GitHub Copilot
  - Updated `copy_ide_configs()` to accept framework parameter and perform placeholder replacement
  - Updated all 5 callers (setup, update, doctor, add-ide, journal_factory) to pass framework parameter
- **Version tracking bug**: Fixed hardcoded version "1.0.0" in journal profiles and manifests
  - Journal profiles now store actual package version (e.g., "1.1.1") instead of hardcoded "1.0.0"
  - Manifest files now use actual package version
  - Updated setup.py and migration.py to use `__version__` instead of hardcoded strings

### Added
- **Enhanced setup command for existing journals**: Better messaging and confirmation when running setup on existing journal
  - New `_detect_existing_journal()` function detects all existing content:
    - Journal folders (daily, projects, people, etc.)
    - IDE configurations (all 4 supported IDEs)
    - Template files
    - User customizations (.ai-instructions/)
  - New `_handle_existing_journal()` function provides clear messaging:
    - Shows what content was detected
    - Explains what will happen if user proceeds
    - Offers to keep existing IDE configuration or choose new one
    - Provides helpful guidance if user cancels
  - Setup now shows "update" instead of "create" message when reinstalling
  - Clear confirmation prompts: "Proceed with re-installation at this location?"
  - Better --no-confirm mode handling with appropriate warnings

### Technical
- **33 new tests added** (458 → 491 total tests)
  - 23 new unit tests in `test_cli_setup.py`:
    - 16 tests for `_detect_existing_journal()` covering all detection scenarios
    - 7 tests for `_handle_existing_journal()` covering messaging and user flows
  - 10 new integration tests in `test_setup_complete.py`:
    - Existing journal detection and warning
    - IDE choice offering and handling
    - Framework placeholder replacement verification
    - Actual version storage verification
    - Reinstall message clarity
    - Multiple IDE config detection
    - Customization preservation messaging
    - All frameworks placeholder replacement
- All 491 tests passing on macOS, Linux, and Windows
- 100% code formatting and linting compliance

## [1.1.0] - 2025-11-09

### Added
- **Framework-Specific Templates**: Choose your preferred journaling methodology during setup
  - **GTD® (Getting Things Done®)**: Next actions, waiting for lists, someday/maybe, context-based organization
  - **PARA™ (Projects, Areas, Resources, Archive)**: Clear separation of projects vs ongoing areas, resource library
  - **Bullet Journal®**: Rapid logging, monthly logs, future log, custom collections
  - **Zettelkasten**: Atomic notes, permanent notes, index system, emphasis on linking
  - **Default**: Flexible framework that adapts to any workflow
  - Each framework includes custom templates tailored to the methodology
  - Add `--framework` flag to setup command for non-interactive selection
  - Interactive framework selector with descriptions during setup
  - 15+ framework-specific templates across all methodologies
- **New `switch-framework` command**: Change journaling frameworks safely after setup
  - Switch between any framework (default, GTD, PARA, Bullet Journal, Zettelkasten)
  - Automatic timestamped backups of existing templates before switching
  - Backups stored in `.framework-backups/` with microsecond-precision timestamps
  - Multiple backups preserved - switch as many times as you want
  - Journal content (daily/, projects/, people/, etc.) completely untouched
  - Interactive framework selection or specify framework directly
  - Use `ai-journal-kit switch-framework <framework>` or interactive prompt
  - Preserves all template customizations in timestamped backups
- **Multi-Journal Support**: Manage multiple independent journals for different areas of your life
  - Create multiple journals with unique names: `ai-journal-kit setup --name business`
  - Each journal has its own location, framework, IDE, and templates
  - New `list` command shows all configured journals with active indicator
  - New `use` command switches between journals: `ai-journal-kit use business`
  - Environment variable override: `AI_JOURNAL=business ai-journal-kit status`
  - First journal defaults to "default" name automatically
  - Additional journals require `--name` flag or interactive prompt
  - All journals tracked in central config file
  - Completely independent - different frameworks, locations, and customizations per journal
  - Automatic migration of old single-journal configs to multi-journal format
  - Backward compatible - existing journals automatically become "default" journal
- **Manifest Tracking System**: Automatic detection and protection of template customizations
  - SHA256 hashing of template files to detect user modifications
  - Manifest file (`.system-manifest.json`) tracks all system-managed files
  - Prevents accidental overwrite of customized templates during framework switches
  - Auto-migration for existing journals without manifests
- **Enhanced IDE Configuration Loading**: All IDE configs now load all .ai-instructions/*.md files
  - Cursor, Windsurf, Claude Code, and Copilot all load custom instructions
  - Users can add multiple .ai-instructions/*.md files for modular AI behavior
  - Each IDE automatically discovers and loads all instruction files
  - Better separation of system rules and user customizations

### Changed
- Setup now prompts for framework choice in addition to IDE and location
- Config model updated to store selected framework
- Templates automatically copied based on chosen framework
- Non-interactive setup (with `--no-confirm`) defaults to 'default' framework
- **Config architecture completely rewritten** for multi-journal support
  - New `MultiJournalConfig` and `JournalProfile` Pydantic models
  - Legacy `Config` model maintained for backward compatibility
  - `load_config()` returns active journal as legacy Config object
  - All config operations now journal-aware
  - Automatic migration from single-journal to multi-journal format on first load

### Technical
- Added `validate_framework()` function for framework validation
- Added `ask_framework()` UI function for interactive framework selection
- Updated `create_structure()` to accept framework parameter
- Added `copy_framework_templates()` function
- Added `switch_framework()` CLI command with backup functionality
- Added `update_config()` function to update framework in config
- Added `list_journals()` CLI command to show all journals
- Added `use_journal()` CLI command to switch active journal
- Added `get_active_journal_name()` function for journal selection with env var support
- Added `migrate_legacy_config()` function for automatic config migration
- Added `Manifest` class for tracking system-managed files with SHA256 hashing
- Added `migrate_to_manifest_system()` for auto-migration of existing journals
- 27 new tests (19 integration + 8 unit) for framework and switching functionality
  - 10 comprehensive tests for switch-framework command covering:
    - Framework switching between all frameworks
    - Timestamped backup creation
    - Multiple backup preservation
    - Journal content preservation
    - Error handling (no setup, invalid framework, same framework)
    - Interactive mode
- 29 new tests for multi-journal functionality
  - 13 unit tests for `MultiJournalConfig` and `JournalProfile` models
  - 9 integration tests for `use` and `list` commands
  - 8 integration tests for multi-journal setup workflow
  - Tests cover: journal creation, switching, env var override, duplicate detection, legacy migration
- **81 additional tests added** bringing total to **458 tests**
  - 9 unit tests for config persistence (roundtrip, corruption handling, datetime serialization)
  - 5 integration tests for end-to-end config persistence validation
  - 24 tests for UI utilities (prompts, IDE selection, framework selection)
  - 10 tests for add-ide command
  - 7 tests for list-journals command
  - 5 tests for use-journal command
  - 8 tests for customize-template command
  - 11 tests for switch-framework command
  - 4 tests for manifest edge cases (non-relative paths)
- **Test coverage improved from 90% to 98%**
  - Perfect 100% coverage on: add_ide.py, list_journals.py, use_journal.py, customize_template.py, ui.py
  - 97% coverage on config.py and manifest.py

### Fixed
- **CRITICAL: Config persistence bug**: Fixed config file disappearing on macOS
  - Config now correctly uses platformdirs for macOS: `~/Library/Application Support/ai-journal-kit/`
  - Added 9 unit tests + 5 integration tests to prevent regression
  - Tested config persistence across multiple commands and load/save cycles
  - Fixed path expansion for `~` in journal locations
- **Claude Code CLAUDE.md support**: Fixed missing CLAUDE.md file in Claude Code IDE configuration
  - Claude Code now properly installs CLAUDE.md with AI coaching instructions
  - Updated status command to check for CLAUDE.md instead of old SYSTEM-PROTECTION.md check
  - Updated doctor command for correct file validation
  - All IDE checks now validate correct files
- **System file protection**: Added "DO NOT EDIT" warnings to all 19 IDE configuration files
  - Clear HTML comment warnings at top of all system-managed files
  - Warns users that files will be overwritten during updates
  - Directs users to `.ai-instructions/` for customizations
  - Prevents accidental loss of system functionality

### Security
- Enhanced file protection warnings prevent users from breaking their installation by editing system files

## [1.0.13] - 2025-11-09

### Added
- **New `add-ide` command**: Add IDE configurations to existing journal without recreating
  - Install Cursor, Windsurf, Claude Code, or GitHub Copilot configs to existing journal
  - Use `ai-journal-kit add-ide <ide>` or interactive prompt
  - Idempotent - safe to run multiple times
  - Preserves all journal content and settings
  - Supports adding individual IDEs or all at once with `add-ide all`

### Changed
- Enhanced IDE configuration flexibility
- Users can now mix and match multiple IDE configurations in one journal

## [1.0.12] - 2025-11-09

### Fixed
- **Update command downgrade protection**: Fixed bug where update command would attempt to downgrade when running development version
  - Now properly compares semantic versions using `packaging.version.parse()`
  - Detects when current version is newer than PyPI and refuses to downgrade
  - Shows clear warning when running development version
  - Use `--force` to refresh IDE configs without package downgrade

## [1.0.11] - 2025-11-09

### Fixed
- **Template updater bug**: Fixed incorrect import that prevented template update functionality from working
  - Changed `get_template_path` to `get_template` in template_updater.py
  - Template comparison and updates now work correctly
- **Claude Code IDE detection**: Fixed doctor command to check for correct file
  - Now correctly checks for `SYSTEM-PROTECTION.md` instead of `CLAUDE.md`
  - Matches actual Claude Code template structure
- **Claude Code template installation**: Fixed template copying to match actual structure
  - Copies markdown files to journal root directory as intended
- **Pydantic v2 compatibility**: Eliminated deprecation warnings
  - Migrated from class-based `Config` to `ConfigDict` pattern
  - No functional changes, internal modernization only

### Changed
- **Improved automation support**: `--no-confirm` flag now auto-creates parent directories
  - Applies to both `setup` and `move` commands
  - Better support for scripted/automated installations
- **Massively improved test coverage**: Increased from 75% to 99% coverage
  - Added 116 new tests (181 → 297 total tests)
  - Comprehensive unit tests for all core modules
  - Integration tests for all CLI commands
  - End-to-end workflow testing
  - All 264 tests passing on Ubuntu, macOS, and Windows

### Developer Experience
- **Enhanced type safety**: Improved validation.py type checking
- **Test infrastructure**: Added isolated test fixtures and helpers
- **CI improvements**: Better GitHub Actions workflow for cross-platform testing

## [1.0.10] - 2025-11-07

### Fixed
- **Cross-platform pip detection**: Update command now auto-detects the correct pip command
  - Tries `pip`, `pip3`, `python -m pip`, `python3 -m pip` in order
  - Works on Windows where `python3` doesn't exist (uses `pip` or `python -m pip`)
  - Works on Linux/Mac where `pip` might not exist (uses `pip3` or `python3 -m pip`)
  - Shows correct command in error messages based on detected pip

### Changed
- **Smart pip command selection**: No more hardcoded `python3 -m pip`
  - Automatically adapts to user's system
  - Better cross-platform compatibility

## [1.0.9] - 2025-11-07

### Fixed
- **Critical update command bug**: `--force` flag no longer skips package upgrade
  - Previously `--force` would skip the pip upgrade entirely, causing silent failures
  - Now package upgrade always happens, even with `--force`
  - Better error messages when upgrade fails (shows stderr, suggests --no-cache-dir)
  - `--force` now only skips version check/confirmation, as intended

### Changed
- **Update command behavior**: Package upgrade is now mandatory during updates
  - Ensures IDE configs match installed package version
  - Prevents stale configuration files
  - More reliable update process

## [1.0.8] - 2025-11-07

### Added
- **Copilot user customizations**: Added `.ai-instructions/` support for GitHub Copilot users
  - Created `user-customizations.instructions.md` to load custom coaching preferences
  - Copilot now checks for and applies `.ai-instructions/my-coach.md` overrides
  - Full feature parity with Cursor, Windsurf, and Claude Code
  - Users can customize AI behavior without modifying core system files

### Changed
- **Copilot coaching instructions**: Added user customization section to `journal-coach.instructions.md`
  - Explicitly mentions checking `.ai-instructions/` folder
  - Documents available customization files
  - Aligns with other IDE implementations

## [1.0.7] - 2025-11-07

### Changed
- **Copilot configuration structure**: Reorganized GitHub Copilot instructions for consistency
  - Moved `copilot-instructions.md` to `.github/instructions/journal-coach.instructions.md`
  - All instructions now in `.github/instructions/` folder for better organization
  - Matches pattern used by Cursor and Windsurf IDEs
  
### Fixed
- **Update command**: Automatically cleans up old Copilot structure for existing users
  - Removes outdated `copilot-instructions.md` from `.github/` root if present
  - Applies new structure seamlessly during updates

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

