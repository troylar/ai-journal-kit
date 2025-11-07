# Changelog

All notable changes to the AI Markdown Journal system will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-06

### Updated (2025-11-06 evening)
- **Migrated to modern Cursor rules** - Using `.mdc` format in `.cursor/rules/`
- **Removed legacy `.cursorrules`** - Now using composable MDC files
- **Created 4 rule files**:
  - `journal-coach.mdc` - Core AI coaching behavior (Always Apply)
  - `daily-notes.mdc` - Daily note helpers (Apply to daily/*.md)
  - `projects.mdc` - Project management (Apply to projects/*.md)
  - `user-customizations.mdc` - User preference loader (Always Apply)
- **Improved rule scoping** - Rules apply intelligently based on file context
- **Better organization** - Modular, composable rules following Cursor best practices

## [1.0.0] - 2025-11-06 (Initial Release)

### Added
- **Modular architecture** with `_core/` (system) and `journal/` (user content) separation
- **Setup script** (`setup.sh`) for initial installation
- **Update script** (`update-core.sh`) for getting latest features
- **Configuration system** (`.ai-journal-config.json`)
- **Daily note template** with morning/evening structure
- **Project template** with phases, milestones, and retrospective
- **Area template** for ongoing responsibilities
- **People template** for relationship tracking
- **AI coach setup guide** with full configuration instructions
- **Demo-safe AI instructions** for presentations and sharing
- **Workflows guide** with common patterns and tips
- **Comprehensive documentation** for all features
- **Example daily note** with filled-out content
- **Folder structure guides** for daily notes, projects, areas, resources, people, archive
- **MIT License** for open source sharing
- **Contributing guidelines** for community contributions

### Customization Features
- **Custom AI instructions folder** (`journal/.ai-instructions/`) protected from updates
- **Customization guide** - Complete guide for personalizing the system
- **Cloud storage guide** - Setup instructions for Google Drive, Dropbox, GitHub, etc.
- **Multiple AI personalities** - Different coach modes for different contexts
- **Custom template support** - Copy and customize any template
- **Flexible folder structure** - Organize journal however you want

### Cloud & Sync
- **Cloud storage ready** - Works with Google Drive, Dropbox, iCloud
- **Git version control** - Option to version control journal separately
- **Mobile access** - Use with Obsidian mobile or any markdown app
- **Symlink support** - Sync journal only, keep system local
- **Multiple devices** - Easy multi-device workflow

### Core Philosophy
- Modular and updateable system
- Privacy-first with protected journal folder
- Framework-agnostic (works with any markdown editor)
- Conversation-first AI coaching approach
- Simple structure with powerful results

---

## Future Releases

### [1.1.0] - Planned
- Additional templates (meeting notes, book notes, learning logs)
- Integration examples (Beeminder, Rize time tracking, ClickUp)
- Automation scripts for common tasks
- Mobile-optimized templates
- Quick capture templates

### [1.2.0] - Planned
- Data analysis tools (word frequency, mood tracking, pattern recognition)
- Weekly/monthly review templates
- Goal tracking templates
- Habit tracking integration examples
- Community template library

### [2.0.0] - Future
- Web-based interface (optional)
- Multi-vault support
- Enhanced AI coach features
- Visualization tools
- Export and analytics

---

## How to Update

Run the update script to get the latest features:

```bash
./update-core.sh
```

Your `journal/` content is always protected and will never be touched by updates.

---

## Version History

- **v1.0.0** (2025-11-06) - Initial modular release

