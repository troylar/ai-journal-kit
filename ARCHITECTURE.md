# Architecture Overview

## Design Philosophy

AI Markdown Journal is built on a **modular architecture** that separates system files from user content, enabling:

1. **Updateability** - Core system can evolve without touching user content
2. **Flexibility** - Users can customize everything in their journal
3. **Privacy** - User content is protected and gitignored by default
4. **Simplicity** - Clear separation of concerns

## Two-Layer Architecture

### Layer 1: `_core/` - System Files (Maintained & Updateable)

Core templates, documentation, and tooling maintained by the project.

```
_core/
├── templates/          # Reusable note templates
├── docs/              # Setup guides and documentation
│   └── guides/        # Detailed how-to guides
├── instructions/      # AI coach system instructions
├── examples/          # Filled-out example notes
├── scripts/           # Automation (setup, update)
├── CHANGELOG.md       # Version history
├── VERSION            # Current version number
└── MAINTAINERS.md     # Maintainer's guide
```

**Characteristics:**
- Version controlled and tracked in git
- Can be updated via `git pull` or `./update-core.sh`
- Generic and reusable content only
- Never contains user-specific information

### Layer 2: `journal/` - User Content (Private & Flexible)

User's personal journal workspace - completely customizable.

```
journal/
├── daily/             # Daily notes (YYYY-MM-DD.md)
├── projects/          # Active projects
├── areas/            # Ongoing responsibilities
├── resources/        # Reference material
├── people/           # Relationship notes
├── archive/          # Completed items
└── README.md         # Journal guide
```

**Characteristics:**
- Gitignored by default (private)
- User has complete control
- Never touched by updates
- Completely flexible organization

## Update Mechanism

### Initial Setup: `setup.sh`

```bash
./setup.sh
```

**What it does:**
1. Creates `journal/` folder structure
2. Copies example daily note
3. Creates `.ai-journal-config.json`
4. Adds README to journal/
5. Preserves folder structure with `.gitkeep`

**Safe to run multiple times** - won't overwrite existing content.

### Getting Updates: `update-core.sh`

```bash
./update-core.sh
```

**What it does:**
1. Checks for uncommitted changes in `_core/`
2. Creates backup of current `_core/`
3. Updates `_core/` from git origin
4. Optionally updates root documentation
5. **Never touches `journal/`**

**Result:**
- ✅ Latest templates and features
- ✅ Improved documentation
- ✅ New tools and scripts
- ✅ Your journal content completely safe

## Configuration System

### `.ai-journal-config.json`

User preferences and settings.

```json
{
  "version": "1.0.0",
  "preferences": {
    "daily_template": "_core/templates/daily-template.md",
    "coaching_style": "energetic",
    "ai_instructions": "_core/instructions/demo-safe.md"
  },
  "folders": {
    "daily": "journal/daily",
    "projects": "journal/projects"
  },
  "integrations": {
    "beeminder": { "enabled": false },
    "rize": { "enabled": false }
  }
}
```

**Purpose:**
- Customize template locations
- Configure AI coach behavior
- Adjust folder structure
- Enable/disable integrations

**Can be committed or gitignored** - user's choice.

## File Organization Rules

### What Goes in `_core/`

✅ **Include:**
- Generic, reusable templates
- Documentation and guides
- AI coach instructions
- Example notes (with generic content)
- Automation scripts
- Version and changelog

❌ **Never Include:**
- User journal entries
- Personal information
- Sensitive content
- User-specific customizations

### What Goes in `journal/`

✅ **User Creates:**
- Daily notes
- Project tracking
- Area management
- Resource notes
- People/relationship tracking
- Archived items

**Completely flexible** - user organizes however they want.

## Versioning Strategy

Following [Semantic Versioning](https://semver.org/):

### Major Version (X.0.0)
Breaking changes that affect user workflow:
- Folder structure changes
- Template format changes
- Breaking config changes

### Minor Version (0.X.0)
New features, backwards compatible:
- New templates
- New documentation
- New integrations
- Enhanced features

### Patch Version (0.0.X)
Bug fixes and minor improvements:
- Documentation fixes
- Template improvements
- Script bug fixes
- Minor enhancements

## Git Workflow

### For Users (Cloning the Starter Kit)

```bash
# Clone the repo
git clone https://github.com/troylar/ai-journal-kit.git
cd ai-journal-kit

# Run setup
./setup.sh

# Start journaling
# journal/ is gitignored - your content stays private

# Get updates when available
./update-core.sh
```

### For Users (Version Controlling Their Journal)

```bash
# Edit .gitignore to allow journal/
# Remove or comment out the journal/* line

# Use a PRIVATE repository!
git add journal/
git commit -m "Add journal content"
git push
```

### For Maintainers (Releasing Updates)

```bash
# 1. Make changes to _core/
# 2. Update CHANGELOG.md
# 3. Update VERSION
# 4. Test setup and update scripts

# 5. Commit and tag
git add .
git commit -m "Release v1.1.0: [description]"
git tag v1.1.0
git push origin main --tags

# 6. Create GitHub release
```

## Security Considerations

### Privacy Protection

1. **journal/ gitignored by default**
   - User content never accidentally committed
   - Folder structure preserved with .gitkeep

2. **Config contains no secrets**
   - API keys stored separately
   - Example config shows structure only

3. **Clear separation**
   - System files vs user content
   - No mixing of concerns

### Best Practices for Users

- Use private repo if version controlling journal
- Never commit API keys
- Review files before committing
- Keep sensitive notes in separate files
- Use generic terms if needed

## Extensibility

### Adding New Templates

1. Create in `_core/templates/`
2. Add guide in `_core/docs/guides/`
3. Add example in `_core/examples/`
4. Update CHANGELOG
5. Release new minor version

### Adding Integrations

1. Create guide in `_core/docs/integrations/`
2. Add config to `.ai-journal-config.json.example`
3. Document in main README
4. Update CHANGELOG
5. Release new minor version

### Custom User Templates

Users can:
1. Copy template from `_core/templates/`
2. Customize in their own location
3. Update config to point to custom template
4. Never affected by updates

## Platform Support

### Tested Platforms
- macOS (primary)
- Linux (Ubuntu, Debian)
- Windows (WSL)

### Markdown Editors
- Obsidian (recommended)
- Logseq
- VS Code
- Typora
- Any markdown editor

### AI Platforms
- Claude (Anthropic)
- ChatGPT (OpenAI)
- Custom implementations
- Local models (via API)

## Performance Considerations

### Scalability

**Daily Notes:**
- One file per day
- Organize by year/month if needed
- Archive old notes periodically

**Search:**
- Full-text search via editor (Obsidian, VS Code)
- Git grep for advanced searches
- Fast even with thousands of notes

**Backups:**
- Plain text markdown = easy backups
- Git = version history
- Cloud sync via Dropbox/iCloud

## Future Enhancements

### Planned Features (v1.x)
- Additional template types
- Integration examples
- Mobile templates
- Quick capture system

### Long-term Vision (v2.x)
- Optional web interface
- Data visualization tools
- Enhanced AI features
- Community template library

---

## Key Takeaways

1. **Modular** - Clear separation between system and content
2. **Updateable** - Get new features without losing content
3. **Private** - Your journal stays yours
4. **Flexible** - Customize everything
5. **Simple** - Plain markdown, no lock-in

This architecture enables the project to evolve while respecting user privacy and flexibility.

