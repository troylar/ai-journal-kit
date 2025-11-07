# AI Journal Kit

A modular, AI-powered journaling starter kit for personal growth, productivity tracking, and daily reflection.

## What Is This?

This is an **AI-powered markdown journaling system** that works with multiple AI code editors:
- **Cursor** (pre-configured with MDC rules)
- **Windsurf** (pre-configured with rules)
- **Claude Code/Cline** (hierarchical CLAUDE.md files)
- **GitHub Copilot** (path-specific instructions)
- Any markdown editor

The system provides:
- Natural conversational journaling with AI coach
- Automatic note updates as you chat
- Memory capture for insights and breakthroughs
- Pattern recognition and accountability
- Daily planning and reflection
- Personalized coaching based on your goals

## ✨ Modular Architecture

This system is built with **two separate layers**:

### 🔧 `_core/` - System Files (Updateable)
Core templates, documentation, and tools maintained by the project:
- **Templates** - Daily notes, projects, areas, people
- **Documentation** - Guides and setup instructions
- **AI Instructions** - Coach configuration templates
- **Scripts** - Setup and update automation

**Can be updated** from GitHub to get new features and improvements.

### 📓 `journal/` - Your Content (Completely Flexible)
Your personal journal content - **never touched by updates**:
- `daily/` - Your daily notes
- `projects/` - Your active projects
- `areas/` - Your ongoing responsibilities
- `resources/` - Your reference material
- `people/` - Your relationship notes
- `memories/` - Insights, breakthroughs, struggles
- `archive/` - Your completed items
- `.cursor/rules/` - Cursor AI coach rules (MDC format)
- `.windsurf/rules/` - Windsurf AI coach rules
- `CLAUDE.md` + folder-specific - Claude Code instructions
- `.github/` - GitHub Copilot instructions
- `.ai-instructions/` - Your custom AI coaching preferences

**Completely private and flexible** - organize however you want!
**Stored anywhere** - local, Google Drive, Dropbox, iCloud, or any path you choose!

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** - Fast Python package installer

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# OR
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
```

### Installation & Setup

```bash
# Run setup (installs and configures in one command)
uvx ai-journal-kit setup
```

The interactive setup will ask you:

1. **📁 Journal Location**
   - Press Enter for local (`./journal`)
   - Or enter custom path (e.g., `~/Documents/my-journal`)
   - Validates path and creates directories

2. **🖥️  Which AI Editor?**
   - Cursor (MDC rules in `.cursor/rules/`)
   - Windsurf (rules in `.windsurf/rules/`)
   - Claude Code/Cline (hierarchical `CLAUDE.md` files)
   - GitHub Copilot (`.github/copilot-instructions.md`)
   - Multiple/All (installs all configurations)

3. **✅ Confirm Setup**
   - Reviews your choices
   - Shows what will be created
   - Confirms before proceeding

**What gets created:**
- Journal folder structure (local or custom location)
- AI editor configurations (based on your choice)
- Example daily note
- Configuration file
- Symlink (if using custom location)

### 3. Open Your Journal

Based on your IDE choice during setup:

**Cursor:**
```bash
cursor journal/  # Or your custom path
```
- Rules in `.cursor/rules/` (MDC format)
- Check Settings → Rules to see all active rules
- AI coach ready immediately!

**Windsurf:**
```bash
windsurf journal/  # Or your custom path
```
- Rules in `.windsurf/rules/`
- Check Customizations → Rules panel
- AI coach ready immediately!

**Claude Code (Cline):**
- Open `journal/` folder in VS Code with Cline extension
- `CLAUDE.md` files in root and each subfolder
- Hierarchical context automatically applied

**GitHub Copilot:**
```bash
code journal/  # Or your custom path
```
- Instructions in `.github/copilot-instructions.md`
- Path-specific instructions in `.github/instructions/`
- Context applies automatically

**Any Markdown Editor:**
- Open the markdown files directly
- Templates available in `../_core/templates/`

### 4. Start Journaling with AI! 🤖

**All editors are pre-configured during setup!**

Just say: **"get the time and let's start the day"**

The AI coach will:
- ✅ Greet you warmly
- ✅ Ask about sleep and energy
- ✅ Help set priorities
- ✅ Create today's daily note
- ✅ **Automatically update notes** as you chat
- ✅ **Offer to capture** significant insights as memories

**What's Included:**

- **Core Coaching** - Energetic, supportive AI coach
- **Daily Check-Ins** - Morning and evening protocols
- **Project Updates** - Auto-update project progress
- **People Notes** - Track conversations and relationships
- **Memory Capture** - Save breakthroughs and insights
- **User Customizations** - Override defaults with your preferences

**Customize Your Coach:**
```bash
# Copy the example
cp journal/.ai-instructions/my-coach.md.example \
   journal/.ai-instructions/my-coach.md

# Edit your preferences - AI automatically uses them!
```

## 🛠️  CLI Commands

After setup, you have access to these commands:

### Status
```bash
# Check journal health and configuration
uvx ai-journal-kit status

# Show detailed information
uvx ai-journal-kit status --verbose

# Output as JSON
uvx ai-journal-kit status --json
```

### Update
```bash
# Check for updates
uvx ai-journal-kit update --check

# Update to latest version
uvx ai-journal-kit update

# Skip AI behavior changes (apply other updates only)
uvx ai-journal-kit update --skip-ai-changes
```

**Note**: Updates NEVER touch your journal content or customizations!

### Move
```bash
# Move journal to new location
uvx ai-journal-kit move ~/new-location

# Interactive mode (prompts for location)
uvx ai-journal-kit move
```

### Doctor
```bash
# Diagnose issues
uvx ai-journal-kit doctor

# Auto-fix common problems
uvx ai-journal-kit doctor --fix

# Show detailed diagnostics
uvx ai-journal-kit doctor --verbose
```

## 📚 Documentation

All documentation is in `_core/docs/`:

### Getting Started
- **`cursor-setup.md`** - 🎯 Cursor (MDC rules)
- **`windsurf-setup.md`** - Windsurf rules system
- **`claude-code-setup.md`** - Claude Code hierarchical CLAUDE.md
- **`copilot-setup.md`** - GitHub Copilot instructions
- **`workflows.md`** - Common workflows and tips
- **`cloud-storage-guide.md`** - ☁️ Custom journal locations
- **`customization-guide.md`** - 🎨 Customize AI behavior and templates

### Guides (in `_core/docs/guides/`)
- **`daily-notes.md`** - How to use daily notes
- **`projects.md`** - Project management guide
- **`areas.md`** - Managing areas of responsibility
- **`resources.md`** - Organizing reference material
- **`people.md`** - Relationship notes guide
- **`memories.md`** - Capturing insights and breakthroughs
- **`archive.md`** - Archiving completed items

## 🔄 Updating

### 📦 Get Latest Features

```bash
# Check for updates
uvx ai-journal-kit update --check

# Install latest version
uvx ai-journal-kit update

# Force reinstall IDE configs (if needed)
uvx ai-journal-kit update --force
```

#### How Updates Work

**1. Check PyPI for Latest Version**
- Compares your installed version with PyPI
- Shows changelog with new features
- **Highlights any AI behavior changes** (Constitution principle)

**2. Review What's Changing**
```
Update Plan:
• Package: 1.0.0 → 1.1.0
• IDE Configs: Refresh Cursor configurations
• Journal: /path/to/your/journal

What's Protected:
✓ All journal content (daily, projects, people, memories)
✓ Your custom preferences (.ai-instructions/)
✓ Your data remains untouched

What's Updated:
→ IDE configuration files with new features
→ System templates and rules
→ WELCOME.md (if exists)
```

**3. Safe Update Process**
- Upgrades Python package via `uvx`
- Refreshes IDE configs (`.cursor/rules/`, `.windsurf/rules/`, etc.)
- Never touches your journal content
- Never touches `.ai-instructions/my-coach.md`

#### What Gets Updated

**System Files (from PyPI):**
- ✅ IDE configuration files (new AI rules and features)
- ✅ System templates (improved structures)
- ✅ WELCOME.md (updated onboarding guide)
- ✅ CLI commands (bug fixes, new features)

**What NEVER Changes:**
- ❌ Your journal content (`daily/`, `projects/`, `people/`, `memories/`, etc.)
- ❌ Your customizations (`.ai-instructions/my-coach.md`)
- ❌ Your configuration (journal location, IDE choice)
- ❌ Your data is sacrosanct

#### Development Mode

If you're running from source (not PyPI):
```bash
# Can't check PyPI, but can refresh configs
uvx ai-journal-kit update --force

# Reinstalls latest IDE configs from your local package
```

## 🎯 Philosophy

### 1. **Modular & Updateable**
- Core system can evolve and improve
- Your content stays private and flexible
- Get new features without losing your work
- `uvx ai-journal-kit update` pulls latest without touching your journal

### 2. **Fully Customizable**
- **AI personality**: Customize coaching style, tone, and behavior
- **Templates**: Adjust daily notes, projects, areas to your needs
- **Folder structure**: Organize however you want
- **All customizations protected** from updates (stored in `journal/`)

### 3. **Flexible Journal Location**
- **Local**: Default `./journal` folder
- **Cloud**: Google Drive, Dropbox, iCloud, OneDrive
- **Custom**: Any path on your system
- **Mobile access**: Sync via cloud, use any markdown app
- **Setup handles it**: Path validation, symlinks, directory creation
- **Change anytime**: `uvx ai-journal-kit move` to move your journal

### 4. **Conversation First**
- Journal through natural conversation, not forms
- AI coach asks curious questions, not interrogations
- Insights emerge organically from dialogue
- Multiple AI personalities for different contexts

### 5. **Privacy & Ownership**
- Your data stays in plain text markdown files
- No lock-in to any platform
- Full control over what you share with AI
- Easy to backup, version, and migrate

## 🛠️ Customization

### ⚡ Quick Customizations

**Customize AI Coach Personality:**
```bash
# Copy the example customization file
cp journal/.ai-instructions/my-coach.md.example \
   journal/.ai-instructions/my-coach.md

# Edit to match your preferences
# Cursor automatically applies your customizations via user-customizations.mdc rule
```

**Customize Daily Template:**
```bash
# Copy and edit
cp _core/templates/daily-template.md journal/.templates/my-daily.md

# Add your own sections (mood, meals, exercise, etc.)
# Update config to use your version
```

**Customize Folder Structure:**
```bash
# Organize however you want!
journal/
├── daily/2025/11/           # By year/month
├── work/projects/           # By category
├── personal/health/         # By life area
└── your-structure/          # Your way!
```

See **`_core/docs/customization-guide.md`** for complete guide.

### ☁️ Custom Journal Location

**During Setup:**
```bash
uvx ai-journal-kit setup

# You'll be asked: "Where would you like to store your journal?"
# - Press Enter for local (./journal)
# - Or enter: ~/Google Drive/my-journal
#           ~/Dropbox/my-journal
#           ~/Documents/journal
#           Any path you want!

# Setup validates the path and creates symlink automatically
```

**After Setup:**
```bash
# Change location anytime
uvx ai-journal-kit move

# Moves your journal and updates configuration
```

**Mobile Access:**
- Put journal in iCloud/Dropbox during setup
- Use Obsidian mobile or any markdown app
- Syncs automatically via cloud

See **`_core/docs/cloud-storage-guide.md`** for all options.

### 🎨 Multiple AI Personalities

Create different coach modes for different contexts:

```bash
journal/.ai-instructions/
├── daily-supportive.md      # Morning check-ins
├── accountability.md        # No-BS mode
├── deep-work.md            # Focus sessions
└── planning.md             # Strategic planning
```

Switch based on your needs!

## 📁 Full Structure

```
ai-journal-kit/
├── README.md                          # This file
├── setup.sh                           # Initial setup script
├── update-core.sh                     # Update system files
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guide
├── .gitignore                         # Protects journal/
│
├── _core/                             # SYSTEM FILES (updateable)
│   ├── templates/                     # System templates
│   │   ├── daily-template.md
│   │   ├── project-template.md
│   │   ├── area-template.md
│   │   └── people-template.md
│   ├── docs/                          # Documentation
│   │   ├── ai-coach-setup.md
│   │   ├── workflows.md
│   │   └── guides/                    # How-to guides
│   │       ├── daily-notes.md
│   │       ├── projects.md
│   │       ├── areas.md
│   │       ├── resources.md
│   │       ├── people.md
│   │       └── archive.md
│   ├── instructions/                  # AI coach instructions
│   │   └── demo-safe.md
│   ├── examples/                      # Example notes
│   │   └── 2025-11-06-example.md
│   └── scripts/                       # Automation scripts
│       ├── setup.sh
│       └── update.sh
│
└── journal/                           # YOUR CONTENT (private, flexible)
    ├── README.md                      # Journal guide
    ├── daily/                         # Daily notes
    │   └── CLAUDE.md                  # Claude Code: daily-specific rules
    ├── projects/                      # Active projects
    │   └── CLAUDE.md                  # Claude Code: project-specific rules
    ├── areas/                         # Ongoing areas
    ├── resources/                     # Reference material
    ├── people/                        # Relationship notes
    │   └── CLAUDE.md                  # Claude Code: people-specific rules
    ├── memories/                      # Insights & breakthroughs
    │   ├── README.md                  # Memory capture guide
    │   └── CLAUDE.md                  # Claude Code: memory-specific rules
    ├── archive/                       # Completed items
    ├── .cursor/rules/                 # Cursor AI rules (MDC format)
    │   ├── journal-coach.mdc
    │   ├── daily-notes.mdc
    │   ├── projects.mdc
    │   ├── memory-capture.mdc
    │   ├── people-notes.mdc
    │   └── user-customizations.mdc
    ├── .windsurf/rules/               # Windsurf AI rules
    │   ├── journal-coach.md
    │   ├── daily-notes.md
    │   ├── projects.md
    │   ├── memory-capture.md
    │   └── people-notes.md
    ├── .github/                       # GitHub Copilot
    │   ├── copilot-instructions.md    # Repository-wide
    │   └── instructions/              # Path-specific
    │       ├── daily-notes.instructions.md
    │       ├── projects.instructions.md
    │       ├── people-notes.instructions.md
    │       └── memories.instructions.md
    ├── CLAUDE.md                      # Claude Code: main instructions
    └── .ai-instructions/              # Custom preferences
        ├── my-coach.md.example
        └── README.md
```

## 🤝 Contributing

This is an open-source starter kit. We welcome:
- Better templates
- Improved documentation
- New integrations
- Bug fixes
- Feature ideas

See `CONTRIBUTING.md` for guidelines.

## 📜 License

MIT License - use freely, modify as needed, share with others.

## 🆘 Support

- **Documentation**: Check `_core/docs/` for guides
- **Issues**: Open a GitHub issue
- **Discussions**: Start a GitHub discussion
- **Updates**: Run `uvx ai-journal-kit update` regularly

## 🌟 Features

### ✅ Already Included
- **Multi-Editor Support**: Cursor, Windsurf, Claude Code, GitHub Copilot
- **Custom Journal Location**: Local or any path (Google Drive, Dropbox, etc.)
- **Automatic Note Updates**: AI updates daily notes, projects, people as you chat
- **Memory Capture**: Saves breakthroughs, struggles, and insights automatically
- **Smart Check-Ins**: Morning and evening protocols
- **User Customizations**: Override AI behavior with your preferences
- **Modular Architecture**: Update system without touching your content
- **Path Validation**: Setup validates and creates directories
- **Symlink Support**: Journal can live anywhere, accessed via symlink
- **IDE-Specific Setup**: Only installs configs for your chosen editor

### 🚧 Coming Soon
- More templates (meeting notes, book notes, etc.)
- Integration examples (Beeminder, Toggl, RescueTime)
- Habit tracking integrations
- Weekly/monthly review templates
- Data analysis and visualization tools

## ❓ FAQ

**Q: Will updates overwrite my journal?**
A: No! The `journal/` folder is protected. Only `_core/` gets updated.

**Q: Can I use this without AI?**
A: Absolutely! The templates and structure work great standalone.

**Q: What if I want to version control my journal?**
A: Edit `.gitignore` to allow `journal/` content. Use a private repo.

**Q: Can I customize the templates?**
A: Yes! Copy them and edit as needed. Update config to use your versions.

**Q: Does this work on mobile?**
A: Yes with Obsidian mobile or any markdown editor. Sync via iCloud/Dropbox.

**Q: How do I share with others?**
A: This repo is the starter kit. Clone, customize, share your version!

**Q: Can I change my journal location after setup?**
A: Yes! Run `uvx ai-journal-kit move` to move your journal anywhere.

**Q: Which AI editor should I choose?**
A: All work great! Cursor and Windsurf have the best AI integration. Choose "All" if unsure.

**Q: Will my notes be automatically updated?**
A: Yes! The AI proactively updates daily notes, projects, people, and memories as you chat.

**Q: What are memories?**
A: Significant moments, insights, or breakthroughs the AI helps you capture for later reflection.

---

**Remember:** The best journaling system is the one you actually use. Start simple, stay consistent, and let it evolve with you.

**Let's go! 📝✨**
