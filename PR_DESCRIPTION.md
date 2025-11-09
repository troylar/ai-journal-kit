# feat: Framework Templates, Multi-Journal Support, and Customization Tracking

## Summary

This PR implements three major feature sets that significantly enhance AI Journal Kit's flexibility and power:

1. **Framework-Specific Templates** - Choose your preferred journaling methodology
2. **Multi-Journal Support** - Manage multiple independent journals
3. **Customization Tracking** - Protect user customizations from updates

Closes #1

---

## 🎨 Framework-Specific Templates

Choose your preferred journaling methodology during setup:

### Supported Frameworks
- **Default** - Flexible structure that adapts to any workflow
- **GTD** (Getting Things Done) - Next actions, waiting for lists, someday/maybe, context-based organization
- **PARA** (Projects, Areas, Resources, Archive) - Clear separation of projects vs ongoing areas
- **Bullet Journal** - Rapid logging, monthly logs, future log, custom collections
- **Zettelkasten** - Atomic notes, permanent notes, index system, emphasis on linking

### Features
- 15+ framework-specific templates across all methodologies
- `--framework` flag for non-interactive setup
- Interactive framework selector with descriptions
- Switch frameworks safely with `switch-framework` command
- Timestamped backups preserve customizations

### Commands
```bash
# Setup with framework
ai-journal-kit setup --framework gtd

# Switch framework later
ai-journal-kit switch-framework para
```

---

## 📚 Multi-Journal Support

Manage multiple independent journals for different areas of your life:

### Features
- Create journals with unique names
- Each journal has independent location, framework, IDE, and templates
- Switch between journals seamlessly
- Environment variable override for temporary switching
- Automatic backward compatibility migration

### Commands
```bash
# Create multiple journals
ai-journal-kit setup --name personal --framework bullet-journal
ai-journal-kit setup --name business --framework gtd

# List all journals
ai-journal-kit list

# Switch between journals
ai-journal-kit use business

# Temporary override
AI_JOURNAL=personal ai-journal-kit status
```

### Use Cases
- 🏢 Separate work and personal journaling
- 🔬 Individual journals for research projects
- 🎯 Different frameworks for different contexts
- 🧪 Testing frameworks without affecting main journal

---

## 🛡️ Customization Tracking

Automatic detection and protection of user customizations:

### Features
- SHA256 hashing of system-managed files
- Manifest tracking (`.system-manifest.json`)
- Prevents accidental overwrite during framework switches
- Auto-migration for existing journals

### How It Works
When you customize a template, the system detects the change and won't overwrite it during updates or framework switches. Your customizations are preserved in timestamped backups.

---

## 🔧 Enhanced IDE Configuration

All IDE configs now support modular customizations:

- Load all `.ai-instructions/*.md` files
- Separate user customizations from system rules
- Works with Cursor, Windsurf, Claude Code, and GitHub Copilot
- New `USER-CUSTOMIZATIONS.md` template for each IDE

---

## 📊 Testing

Comprehensive test coverage:
- **29 new tests** for multi-journal functionality
- **27 new tests** for framework features
- **332 total tests** passing
- **88% code coverage**

### Test Breakdown
- Unit tests for config models and framework validation
- Integration tests for all new commands
- E2E workflow tests
- Backward compatibility tests

---

## 📖 Documentation

Updated documentation includes:
- Comprehensive README sections for all features
- Detailed CHANGELOG entries
- Use case examples and workflows
- Migration guides for existing users
- CLI command reference updates

---

## 🔄 Migration & Compatibility

### Backward Compatibility
- ✅ Existing journals automatically become "default" journal
- ✅ Legacy config format automatically migrated
- ✅ No breaking changes for current users
- ✅ Journals without manifests auto-migrated

### Migration Notes
Users with existing journals will see:
1. Config automatically converted to multi-journal format
2. Existing journal becomes "default" journal
3. Manifest created for customization tracking
4. All functionality continues to work as before

---

## 🎯 Architecture Changes

### Core Changes
- New `MultiJournalConfig` and `JournalProfile` Pydantic models
- `Manifest` class for tracking system-managed files
- Migration utilities for automatic upgrades
- Legacy `Config` model maintained for backward compatibility

### File Structure
```
ai_journal_kit/
├── cli/
│   ├── customize_template.py  # New: Template customization helper
│   ├── list_journals.py       # New: List all journals
│   ├── use_journal.py         # New: Switch journals
│   └── switch_framework.py    # Enhanced: Framework switching
├── core/
│   ├── config.py              # Rewritten: Multi-journal support
│   ├── manifest.py            # New: Customization tracking
│   └── migration.py           # New: Auto-migration
└── templates/
    └── ide-configs/
        └── */USER-CUSTOMIZATIONS.md  # New: Customization templates
```

---

## ✅ Checklist

- [x] All tests passing (332 tests)
- [x] Code coverage maintained (88%)
- [x] Documentation updated (README, CHANGELOG)
- [x] Backward compatibility verified
- [x] Migration tested with legacy configs
- [x] All IDE configs updated
- [x] Examples and use cases documented

---

## 🚀 What's Next

After this PR:
- Users can choose their preferred journaling framework
- Users can manage multiple journals for different contexts
- User customizations are automatically protected
- Framework switching is safe and reversible
- Better IDE configuration flexibility

🤖 Generated with [Claude Code](https://claude.com/claude-code)
