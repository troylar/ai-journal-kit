# v1.1.0 - Critical Config Persistence Fix & Test Improvements

## 🔥 Critical Fixes

### Config Persistence Bug (macOS)
**CRITICAL**: Fixed config file disappearing on macOS after setup
- Config now correctly uses platformdirs: `~/Library/Application Support/ai-journal-kit/`
- Added 9 unit tests + 5 integration tests to prevent regression
- Tested config persistence across multiple commands and load/save cycles
- Fixed path expansion for `~` in journal locations

### Claude Code CLAUDE.md Support
**CRITICAL**: Fixed missing CLAUDE.md file in Claude Code IDE configuration
- Claude Code now properly installs CLAUDE.md with AI coaching instructions
- Updated status command to check for CLAUDE.md
- Updated doctor command for correct file validation
- All IDE checks now validate correct files

### System File Protection
Added "DO NOT EDIT" warnings to all 19 IDE configuration files
- Clear HTML comment warnings at top of all system-managed files
- Warns users that files will be overwritten during updates
- Directs users to `.ai-instructions/` for customizations
- Prevents accidental loss of system functionality

## ✨ Major Features (from v1.0.x)

This release includes all the major features from v1.0.x releases:

### Framework-Specific Templates
Choose your preferred journaling methodology during setup:
- **GTD® (Getting Things Done®)**: Next actions, waiting for, context-based organization
- **PARA™**: Projects, Areas, Resources, Archive
- **Bullet Journal®**: Rapid logging, monthly logs, future log
- **Zettelkasten**: Atomic notes, permanent notes, index system
- **Default**: Flexible framework that adapts to any workflow

### Multi-Journal Support
Manage multiple independent journals for different areas of your life:
- Create multiple journals: `ai-journal-kit setup --name business`
- Switch between journals: `ai-journal-kit use business`
- List all journals: `ai-journal-kit list`
- Environment variable override: `AI_JOURNAL=business ai-journal-kit status`

### Switch Frameworks Safely
- New `switch-framework` command to change methodologies
- Automatic timestamped backups before switching
- Customizations detected and preserved
- Journal content completely untouched

### Manifest Tracking System
- SHA256 hashing of template files to detect modifications
- Automatic protection of customized templates
- Auto-migration for existing journals

## 🧪 Testing Improvements

### Comprehensive Test Coverage
- **Added 81 new tests** (377 → 458 total tests)
- **Improved coverage from 90% to 98%**
- Perfect 100% coverage on: add_ide, list_journals, use_journal, customize_template, ui
- 97% coverage on config.py and manifest.py

### New Test Suites
- 9 unit tests for config persistence
- 5 integration tests for end-to-end config validation
- 24 tests for UI utilities
- 10 tests for add-ide command
- 7 tests for list-journals command
- 5 tests for use-journal command
- 8 tests for customize-template command
- 11 tests for switch-framework command
- 4 tests for manifest edge cases

### Cross-Platform Testing
All 458 tests passing on:
- ✅ Ubuntu
- ✅ macOS
- ✅ Windows

## 📦 Installation

```bash
pip install --upgrade ai-journal-kit
```

## 🔗 Links

- [PyPI Package](https://pypi.org/project/ai-journal-kit/1.1.0/)
- [Full Changelog](https://github.com/troylar/ai-journal-kit/blob/main/CHANGELOG.md)
- [Documentation](https://github.com/troylar/ai-journal-kit#readme)

## 🙏 Acknowledgments

This release includes significant stability improvements and bug fixes that make the toolkit production-ready for all platforms.

---

> **Note**: GTD® and Getting Things Done® are registered trademarks of David Allen Company. Bullet Journal® is a registered trademark of Ryder Carroll. PARA™ is a methodology by Tiago Forte. AI Journal Kit provides compatible templates and is not affiliated with these trademark holders.
