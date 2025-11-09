# 📝✨ AI Journal Kit

> **Your Personal AI Coach for Journaling, Growth & Clarity**
> 🔐 100% Private • 🎨 5 Built-in Frameworks • 📚 Multi-Journal Support • 🤖 AI-Powered • 🛠️ Works Everywhere

<div align="center">

[![PyPI version](https://img.shields.io/pypi/v/ai-journal-kit.svg)](https://pypi.org/project/ai-journal-kit/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![CI](https://github.com/troylar/ai-journal-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/troylar/ai-journal-kit/actions/workflows/ci.yml)
[![Security Scan](https://github.com/troylar/ai-journal-kit/actions/workflows/security.yml/badge.svg)](https://github.com/troylar/ai-journal-kit/actions/workflows/security.yml)
[![codecov](https://codecov.io/gh/troylar/ai-journal-kit/branch/main/graph/badge.svg)](https://codecov.io/gh/troylar/ai-journal-kit)
[![Tests](https://img.shields.io/badge/tests-332%20passing-brightgreen.svg)](https://github.com/troylar/ai-journal-kit/actions)
[![Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen.svg)](https://github.com/troylar/ai-journal-kit/actions)

[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Tested on](https://img.shields.io/badge/tested%20on-Ubuntu%20%7C%20macOS%20%7C%20Windows-blue.svg)](https://github.com/troylar/ai-journal-kit/actions)

</div>

---

## 📑 Table of Contents

**Getting Started**
[Why AI Journal Kit?](#-why-ai-journal-kit) • [Quick Start](#-quick-start-60-seconds) • [Installation](#-installation)

**Core Features**
[File Referencing](#-powerful-file-referencing) • [Journaling Frameworks](#-journaling-frameworks) • [Multi-Journal Support](#-multiple-journals) • [CLI Commands](#%EF%B8%8F-cli-commands) • [Customization](#%EF%B8%8F-customization) • [Obsidian Integration](#-obsidian-powerful-visualization--manual-editing)

**Learning More**
[How It Works](#-how-it-works) • [Examples & Use Cases](#-examples--use-cases) • [FAQ](#-faq) • [Documentation](#-documentation)

---

## 🎯 Why AI Journal Kit?

### 🔐 **100% Private**
Your journal stays on **YOUR** computer. No cloud sync required. No data collection. No privacy compromises.

### 🎨 **5 Built-in Frameworks (or Create Your Own!)**
Choose **YOUR** methodology: GTD®, PARA™, Bullet Journal®, Zettelkasten, or start with our flexible Default. Switch anytime!

### 📚 **Multi-Journal Support**
Separate work from personal. Manage multiple independent journals with different frameworks and settings.

### 🤖 **AI-Powered Intelligence**
Your personal AI coach proactively:
- ✅ Updates your notes as you talk
- ✅ Links and references across people, projects, and memories
- ✅ Captures insights and breakthroughs
- ✅ Recognizes patterns you might miss
- ✅ Provides accountability without judgment
- ✅ Helps you reflect and grow

### 🛠️ **Works Everywhere**
Built for **YOUR** favorite tools:
- **Cursor** • **Windsurf** • **Claude Code** • **GitHub Copilot**
- **Obsidian** for powerful visualization and graph views
- Or any markdown editor!

---

## ⚡ Quick Start (60 Seconds)

### 1️⃣ Install & Setup

```bash
uvx ai-journal-kit setup
```

That's it! The AI will guide you through setup interactively, including:
- **Choose your journal location** (local or cloud folder)
- **Pick a journaling framework** (GTD®, PARA™, Bullet Journal®, Zettelkasten, or flexible default)
- **Select your AI editor** (Cursor, Windsurf, Claude Code, GitHub Copilot)

### 2️⃣ Open Your Journal

```bash
# Open in your AI editor
cursor ~/journal     # or wherever you chose
windsurf ~/journal
code ~/journal
```

### 3️⃣ Start Talking

Just say:

> "Help me get started"

The AI will introduce itself and guide you through customization!

---

## 🎁 What You Get

### 💬 **Natural Conversation**
Talk naturally with your AI coach. No rigid commands or syntax.

```
You: "I'm feeling overwhelmed with the Q4 launch project"
AI: "Let's break it down. What's the biggest blocker right now?"
     [Automatically creates/updates projects/q4-launch.md
      and links it to today's daily note]
```

### 🧠 **Automatic Memory Capture**
The AI recognizes significant moments and offers to save them:

```
You: "I just realized I procrastinate when I'm afraid of failing"
AI: "That's a powerful insight. Want me to capture this as a memory?"
```

### 📊 **Smart Pattern Recognition**
Your AI coach spots patterns you might miss:

```
AI: "I notice you mention feeling tired every Wednesday. 
     Want to explore what's happening mid-week?"
```

### 🎯 **Proactive Updates**
No manual note-taking! The AI updates your notes automatically:

- **Daily notes** - Progress, wins, challenges as they happen
- **Project notes** - Status updates, blockers, decisions
- **People notes** - Conversations, action items, context
- **Memories** - Breakthroughs, insights, patterns

### 🔗 **Powerful File Referencing**
Connect the dots across your entire journal by referencing other notes. The AI helps you build a web of context:

```
You: "I had a great conversation with Sarah about the Q4 launch"

AI: "Nice! I'll update today's daily note and Sarah's people note.
     Should I link this to your 'Q4 Product Launch' project?"

     [Creates connections between daily/2025-01-15.md,
      people/sarah.md, and projects/q4-launch.md]
```

#### Why This Matters

**Cross-Reference Everything:**
- Mention a person → AI updates their people note and links conversations
- Discuss a project → AI connects it to related daily notes and decisions
- Capture a memory → AI links it to relevant projects and people
- Spot a pattern → AI references past memories and insights

**Example Connections:**
```markdown
# Daily Note (2025-01-15)
## Meetings
- Met with [[people/sarah]] about [[projects/q4-launch]]
  - Decided to move deadline to March (see [[memories/deadline-flexibility]])
  - Sarah suggested new approach to testing

# Sarah's People Note
## Recent Conversations
- **2025-01-15**: Q4 Launch Discussion
  - Suggested testing approach (linked in [[projects/q4-launch]])
  - Very supportive of deadline change

# Q4 Launch Project
## Key Decisions
- **2025-01-15**: Extended deadline to March
  - Discussed with [[people/sarah]]
  - Applied lesson from [[memories/deadline-flexibility]]
```

**Benefits:**
- 📊 **See the full picture** - All context about a person, project, or topic in one place
- 🧠 **Never lose context** - Conversations, decisions, and insights are interconnected
- 🔍 **Find information fast** - Click through references instead of searching
- 💡 **Discover patterns** - See how people, projects, and ideas relate over time
- 🎯 **Make better decisions** - Access all relevant history when making choices

The AI helps you maintain these connections automatically—just talk naturally and it handles the references!

---

## 🚀 Installation

### Option 1: Quick Run (Recommended)
```bash
# Install and setup in one command
uvx ai-journal-kit setup
```

### Option 2: Global Install
```bash
# Install globally
pip install ai-journal-kit

# Run setup
ai-journal-kit setup
```

### Option 3: With UV
```bash
# Install as a tool
uv tool install ai-journal-kit

# Run setup
ai-journal-kit setup
```

---

## 📋 Journaling Frameworks

### What Framework Should I Choose?

Each framework is designed for different workflows and preferences:

#### 🎯 **Default** - Best for: Beginners, flexible workflows
- Simple daily notes with morning/evening structure
- Project and people tracking
- Memory capture for insights
- **Perfect if**: You want to start simple and evolve your system organically

#### ⚡ **GTD® (Getting Things Done®)** - Best for: Productivity enthusiasts, task managers
- Next Actions organized by context (@work, @home, @calls, etc.)
- Waiting For tracking
- Someday/Maybe lists
- Weekly review process
- **Perfect if**: You love David Allen's methodology and want comprehensive task management

#### 📁 **PARA™ (Projects, Areas, Resources, Archive)** - Best for: Knowledge workers, organizers
- Clear separation of Projects (time-bound) vs Areas (ongoing)
- Resource library for references
- Archive for completed items
- Goal-oriented structure
- **Perfect if**: You want to organize everything by actionability (Tiago Forte's method)

#### 🔘 **Bullet Journal®** - Best for: Visual thinkers, habit trackers
- Rapid logging with tasks, events, notes
- Monthly logs with calendar view
- Future log for long-term planning
- Custom collections for tracking anything
- **Perfect if**: You love Ryder Carroll's analog system and want a digital version

#### 🔗 **Zettelkasten** - Best for: Researchers, writers, learners
- Atomic notes (one idea per note)
- Permanent notes with unique IDs
- Index/structure notes to organize topics
- Emphasis on linking and connections
- **Perfect if**: You're building a knowledge base or writing long-form content (Niklas Luhmann's method)

### Framework Examples

**GTD Daily Note:**
```markdown
## 📥 Inbox
- Capture everything on your mind

## ⚡ Next Actions
### @work
- [ ] Review quarterly goals
### @calls
- [ ] Schedule dentist appointment

## ⏳ Waiting For
| Item | Who | Date |
|------|-----|------|
| Budget approval | Sarah | 2025-01-15 |
```

**PARA Project:**
```markdown
# Project: Launch Newsletter

**Status**: Active
**Deadline**: End of Q1
**Related Area**: Marketing

## Next Actions
- [ ] Draft first 3 issues
- [ ] Set up email service
```

**Bullet Journal Daily:**
```markdown
# January 15, 2025

## Daily Log
- [ ] Team meeting at 10am
○ Launched new feature
─ Great feedback from users
* Important deadline tomorrow
```

**Zettelkasten Note:**
```markdown
# 202501151430 - Spaced Repetition Learning

The spacing effect shows that information is better retained when study sessions are spaced out over time.

## Related Notes
- [[202501141200 - Memory consolidation]]
- [[202501101500 - Active recall techniques]]

## Sources
- "Make It Stick" by Brown et al.
```

### Switching Frameworks

**Changed your mind?** You can switch frameworks at any time without losing your journal content!

```bash
ai-journal-kit switch-framework para              # Switch to PARA
ai-journal-kit switch-framework gtd               # Switch to GTD
ai-journal-kit switch-framework                   # Interactive selection
```

#### What Gets Backed Up

When you switch frameworks, all your existing templates are automatically backed up:

```
journal/
└── .framework-backups/
    ├── 20250115-143022-123456/    # Timestamped backup from first switch
    │   ├── daily-template.md
    │   ├── project-template.md
    │   └── waiting-for-template.md
    └── 20250120-091545-789012/    # Another backup from second switch
        ├── daily-template.md
        ├── area-template.md
        └── resource-template.md
```

Each backup is timestamped down to the microsecond, so you can switch multiple times and keep all your customized templates.

#### What Stays Untouched

Your actual journal content **never changes**:
- ✅ All daily notes (`daily/`)
- ✅ All project notes (`projects/`)
- ✅ All people notes (`people/`)
- ✅ All memories (`memories/`)
- ✅ Any custom folders or files you've created

**Only the templates change** - your notes are 100% safe!

#### Example Workflow

```bash
# 1. Start with GTD®
ai-journal-kit setup --framework gtd

# 2. Journal for a few months, customize templates
# ... edit waiting-for-template.md with your own style ...

# 3. Want to try PARA™? Switch safely!
ai-journal-kit switch-framework para
# ✅ Your GTD® templates (including customizations) are backed up
# ✅ PARA™ templates are installed
# ✅ All your journal notes are untouched

# 4. Changed your mind? Go back!
# Just restore from .framework-backups/TIMESTAMP/ if needed
```

#### When to Switch

You might want to switch frameworks if:
- 📈 **Your workflow evolved** - Started simple with Default, now ready for GTD®
- 🔄 **Testing methodologies** - Trying different systems to find your fit
- 🎯 **Life changes** - New job/role needs different organization (e.g., researcher → Zettelkasten)
- 🧪 **Experimenting** - Want to try a methodology you've been reading about

**No commitment!** Switch as often as you like - your journal content is always safe.

---

## 📚 Multiple Journals

### Separate Work from Personal Life

Do you keep separate journals for different areas of your life? AI Journal Kit makes it easy to manage multiple independent journals:

#### Create Multiple Journals

```bash
# First journal defaults to "default"
ai-journal-kit setup --location ~/personal-journal --framework bullet-journal

# Create additional journals with unique names
ai-journal-kit setup --name business --location ~/work-journal --framework gtd
ai-journal-kit setup --name research --location ~/research --framework zettelkasten
```

#### Switch Between Journals

```bash
# View all journals
ai-journal-kit list

# Output:
#  Name      Location           Framework    IDE     Status
#  default   ~/personal-journal bullet-journal cursor  ✓ Active
#  business  ~/work-journal     gtd           cursor
#  research  ~/research         zettelkasten  cursor

# Switch to a different journal
ai-journal-kit use business

# Now all commands operate on the "business" journal
ai-journal-kit status    # Shows business journal status
```

#### Temporary Journal Override

Use the `AI_JOURNAL` environment variable to temporarily use a different journal:

```bash
# Quick check on business journal without switching
AI_JOURNAL=business ai-journal-kit status

# Run multiple commands on research journal
AI_JOURNAL=research ai-journal-kit status
AI_JOURNAL=research ai-journal-kit doctor
```

#### Use Cases

- **🏢 Work/Personal Split**: Keep professional projects separate from personal journaling
- **🔬 Research Projects**: Separate journal for each major research topic with Zettelkasten
- **🎯 Different Frameworks**: Use GTD® for work, Bullet Journal® for personal life
- **👥 Team Collaboration**: Separate journal for each team or project
- **🧪 Testing**: Try new frameworks without affecting your main journal

#### How It Works

Each journal is completely independent:
- ✅ **Own location** - Different folder on disk
- ✅ **Own framework** - GTD®, PARA™, or any other methodology
- ✅ **Own IDE** - Can use different editors
- ✅ **Own templates** - Customizations don't affect other journals
- ✅ **Own content** - Notes never mix between journals

**Configuration is stored centrally** in `~/.config/ai-journal-kit/config.json` (or platform equivalent), tracking all your journals and which one is active.

---

## 🎛️ CLI Commands

```bash
# Interactive setup wizard
ai-journal-kit setup

# Setup with specific framework
ai-journal-kit setup --framework gtd              # GTD methodology
ai-journal-kit setup --framework para             # PARA method
ai-journal-kit setup --framework bullet-journal   # Bullet Journal
ai-journal-kit setup --framework zettelkasten     # Zettelkasten

# Create named journal (for multiple journals)
ai-journal-kit setup --name personal              # Create "personal" journal
ai-journal-kit setup --name business --framework gtd   # Named journal with framework

# Switch to a different framework (with timestamped backup)
ai-journal-kit switch-framework para              # Switch to PARA
ai-journal-kit switch-framework gtd               # Switch to GTD
ai-journal-kit switch-framework                   # Interactive selection

# Add IDE configurations to existing journal
ai-journal-kit add-ide cursor        # Add Cursor config
ai-journal-kit add-ide windsurf      # Add Windsurf config
ai-journal-kit add-ide claude-code   # Add Claude Code config
ai-journal-kit add-ide copilot       # Add GitHub Copilot config
ai-journal-kit add-ide all           # Add all IDE configs
ai-journal-kit add-ide               # Interactive prompt

# Multi-journal management
ai-journal-kit list                  # Show all configured journals
ai-journal-kit use business          # Switch to "business" journal
AI_JOURNAL=business ai-journal-kit status  # Temporarily use specific journal

# Check journal health
ai-journal-kit status

# Update to latest version
ai-journal-kit update

# Update with new templates
ai-journal-kit update --templates

# Diagnose and fix issues
ai-journal-kit doctor

# Move journal to new location
ai-journal-kit move
```

---

## 🎓 How It Works

### Morning Check-In
```
You: "Get the time and let's start the day"

AI: "Good morning! It's 6:30 AM on Friday, Nov 7, 2025.

     How did you sleep? ⭐⭐⭐⭐⭐ (Rate 1-5)"

[Creates today's daily note, captures your energy level, 
 helps you set priorities and emotional outcomes]
```

### Throughout the Day
```
You: "Just finished that proposal! Feeling great."

AI: "Awesome! 🎉 That's a big win."

[Automatically updates your daily note:
 "**2:30 PM** - Completed proposal draft! Feeling accomplished."]
```

### Evening Reflection
```
You: "Update my daily note"

AI: "Let's reflect on today:
     - What went well?
     - What challenges came up?
     - What did you learn?
     - What's your top priority tomorrow?"

[Captures your reflection in the daily note]
```

---

## 🛠️ Customization

### Your AI, Your Way

Create `.ai-instructions/my-coach.md`:

```markdown
# My Coaching Preferences

## Style
- Be concise and direct
- Challenge me when I'm avoiding something
- Celebrate wins enthusiastically

## Focus Areas
- Deep work and focus
- Work-life balance
- Health and fitness

## Don't
- Be overly supportive (I need pushback)
- Let me procrastinate
```

The AI will follow **YOUR** preferences!

### Custom Templates

Modify any template:
```bash
# Edit templates in your journal
journal/daily-template.md
journal/project-template.md
journal/people-template.md
```

On setup, the AI uses **YOUR** templates automatically!

---

## 📊 Obsidian: Powerful Visualization & Manual Editing

While AI editors (Cursor, Windsurf, Claude Code) handle the conversational journaling and automatic updates, **Obsidian** is the perfect companion for visualizing connections and manual editing.

### Why Obsidian?

**See Your Entire Knowledge Graph:**
- 🌐 **Graph View** - Visualize all connections between people, projects, and memories
- 🔗 **Backlinks** - See every note that references a specific person or project
- 🔍 **Search Everything** - Instantly find any mention across your entire journal
- 📊 **Canvas View** - Create visual maps of projects, ideas, and relationships
- 📱 **Mobile App** - Review and edit your journal on the go

### The Perfect Workflow

#### Option 1: AI for Writing, Obsidian for Viewing
```
Morning: Use AI editor (Cursor/Windsurf/Claude Code)
→ "Let's start the day"
→ AI creates today's note, captures your thoughts
→ AI automatically cross-references people, projects, memories

Anytime: Open Obsidian to visualize
→ See graph of all your connections
→ Review backlinks for a specific person
→ Browse daily notes in calendar view
→ Add manual thoughts/notes if desired
```

#### Option 2: Hybrid Approach
```
Conversational Journaling: Use AI editor
→ Natural conversation, automatic updates
→ AI creates cross-references

Deep Thinking: Use Obsidian
→ Manually refine notes
→ Add additional context
→ Create canvas boards for planning
→ Explore connections in graph view
```

### Setup Obsidian with Your Journal

**1. Install Obsidian:**
- Download from [obsidian.md](https://obsidian.md)
- It's free for personal use

**2. Open Your Journal as a Vault:**
```bash
1. Launch Obsidian
2. Click "Open folder as vault"
3. Select your journal folder (e.g., ~/journal)
```

**3. Enjoy the Magic:**
- Wiki-style links (`[[people/sarah]]`) automatically work
- Graph view shows all connections
- Backlinks panel shows related notes
- All cross-references created by the AI are instantly navigable

### Recommended Obsidian Plugins

**Core Plugins** (built-in, enable in Settings):
- 📅 **Daily Notes** - Quick access to today's note
- 🔗 **Backlinks** - See what links to current note
- 🌐 **Graph View** - Visualize your knowledge network
- 🔍 **Quick Switcher** - Jump to any note instantly

**Community Plugins** (optional):
- 📆 **Calendar** - Visual calendar of daily notes
- 🎨 **Dataview** - Query and display journal data
- 🌲 **Excalidraw** - Draw diagrams and mind maps
- 📊 **Tracker** - Visualize habits and patterns over time

### Example: Viewing Cross-References

When the AI creates connections like:
```markdown
Met with [[people/sarah]] about [[projects/q4-launch]]
```

**In Obsidian:**
- Click `[[people/sarah]]` → Opens Sarah's note with full conversation history
- View Sarah's **backlinks** → See every daily note and project that mentions her
- Open **graph view** → See Sarah's connections to all projects, people, and topics
- Use **canvas** → Create a visual project board linking Sarah, Q4 launch, and related decisions

### Best of Both Worlds

| Feature | AI Editor (Cursor, etc.) | Obsidian |
|---------|-------------------------|----------|
| **Conversational input** | ✅ Natural dialogue | ❌ Manual typing |
| **Auto-updates** | ✅ Proactive | ❌ Manual |
| **Cross-referencing** | ✅ Automatic | ✅ Manual/navigation |
| **Graph visualization** | ❌ Limited | ✅ Excellent |
| **Backlinks** | ❌ None | ✅ Automatic |
| **Mobile editing** | ❌ Desktop only | ✅ iOS & Android |
| **Canvas/visual boards** | ❌ None | ✅ Built-in |
| **Search & queries** | Basic | ✅ Advanced (Dataview) |

### Tips for Using Both

1. **Morning routine**: Use AI editor for daily check-in and conversational reflection
2. **Throughout the day**: Quick notes via AI or Obsidian mobile
3. **Evening review**: Open Obsidian to visualize the day's connections
4. **Weekly review**: Use Obsidian's graph and backlinks to spot patterns
5. **Planning**: Use Obsidian canvas to create visual project boards
6. **Deep work**: Use Obsidian for focused, manual refinement of ideas

**The AI creates the structure, Obsidian helps you see the big picture!**

---

## 🔐 Privacy & Security

### Your Data Stays Yours
- ✅ Everything stored locally
- ✅ No cloud sync required
- ✅ No telemetry or tracking
- ✅ No data collection
- ✅ 100% private

### AI Access
- ✅ Your chosen AI editor processes locally or via their API
- ✅ You control what the AI can read/write
- ✅ System protection prevents accidental modifications
- ✅ You can review every change

---

## 📚 Documentation

### Getting Started
- [Quick Start Guide](QUICKSTART.md) - Get up and running
- [Architecture](ARCHITECTURE.md) - How it's built
- [Release Process](RELEASING.md) - For maintainers

### Templates & Examples
All templates are in your journal after setup:
- `daily-template.md` - Daily note structure
- `project-template.md` - Project tracking
- `people-template.md` - Relationship notes
- `memory-template.md` - Capturing insights

### Advanced
- **Multi-computer setup**: Use cloud storage for `journal/` folder
- **Team journaling**: Share templates via git
- **Integrations**: Beeminder, RescueTime, ClickUp (examples in docs)

---

## 🤝 Contributing & Community

### How to Contribute

We welcome contributions!

- 🐛 **Bug reports**: [Open an issue](https://github.com/troylar/ai-journal-kit/issues)
- 💡 **Feature requests**: [Start a discussion](https://github.com/troylar/ai-journal-kit/discussions)
- 📖 **Documentation**: Improve guides and examples
- 🎨 **Templates**: Share your custom templates
- 🔧 **Code**: Submit pull requests

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Join the Community

- **GitHub Discussions**: Ask questions, share tips, and connect with other users
- **Issues**: Report bugs and request features
- **Show & Tell**: Share your setup, workflows, and customizations

---

## 📖 Examples & Use Cases

### For Entrepreneurs
```
- Track multiple projects and ventures
- Capture business insights and lessons
- Manage relationships with clients and partners
- Reflect on wins, challenges, and growth
```

### For Developers
```
- Document technical decisions and learnings
- Track bug investigations and solutions
- Manage multiple projects and codebases
- Reflect on code reviews and improvements
```

### For Students
```
- Organize notes across classes and subjects
- Track assignments and deadlines
- Capture study insights and understanding
- Reflect on learning progress
```

### For Personal Growth
```
- Daily gratitude and reflection
- Goal setting and tracking
- Habit formation and accountability
- Emotional processing and awareness
```

---

## 🎯 Philosophy

### No Judgment
The AI creates psychological safety. Gaps are normal. Progress over perfection.

### Proactive, Not Reactive
The AI updates notes automatically as you talk. You shouldn't have to remember to journal—it happens naturally.

### Conversational, Not Transactional
Talk naturally. No commands, no syntax, no friction.

### Your System, Your Rules
Not opinionated about methodology. Adapts to **YOUR** way of working.

---

## 🚦 Roadmap

### ✅ Completed (v1.0+)
- Multi-editor support (Cursor, Windsurf, Claude Code, Copilot)
- Cross-platform CLI with beautiful UI (Ubuntu, macOS, Windows)
- 5 built-in journaling frameworks (GTD®, PARA™, Bullet Journal®, Zettelkasten, Default)
- Multi-journal support (manage multiple independent journals)
- Framework switching with automatic backups
- Customization tracking (manifest system protects your changes)
- Automatic memory capture and pattern recognition
- Safe updates with transparency

### 🎯 Planned
- [ ] Web dashboard for insights and analytics
- [ ] Mobile companion app
- [ ] Voice input support
- [ ] Advanced integrations (calendar, task managers)
- [ ] Community template library
- [ ] Multi-language support

---

## ❓ FAQ

**Q: Is my data private?**  
A: Yes! Everything stays on your computer. No cloud, no tracking, no data collection.

**Q: Do I need an AI editor?**  
A: No! Works with any markdown editor. AI features are optional but recommended.

**Q: Can I use my own journaling system?**
A: Absolutely! Not opinionated. Use GTD®, PARA™, Bullet Journal®, or your own method.

**Q: Will updates break my journal?**  
A: Never. Updates only touch system files, never your content or customizations.

**Q: Can I customize the AI's behavior?**  
A: Yes! Create `.ai-instructions/` files to define your coaching preferences.

**Q: How much does it cost?**  
A: The AI Journal Kit is free and open source (MIT License). You only pay for your chosen AI editor (Cursor, Windsurf, etc.) if using AI features.

**Q: Can I sync across computers?**  
A: Yes! Put your `journal/` folder in Dropbox, Google Drive, or iCloud. The CLI stays installed per-machine.

---

## 🧪 For Developers

### Comprehensive Test Coverage

AI Journal Kit has a robust test suite with **332 tests and 87% code coverage** covering:

- **Unit Tests** (`tests/unit/`): Fast, focused tests for individual components
- **Integration Tests** (`tests/integration/`): Real filesystem operations, command workflows  
- **E2E Tests** (`tests/e2e/`): Complete user journeys across the entire system

### Running Tests

```bash
# Run all tests
pytest

# Run specific test types
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest tests/e2e/           # E2E tests only

# Using invoke tasks
invoke test               # All tests with coverage
invoke test.unit          # Unit tests only
invoke test.integration   # Integration tests only
invoke test.e2e           # E2E tests only
invoke test.quick         # Fast run (no coverage)

# Simulate full CI pipeline locally
invoke ci.local
```

### Contributing

We welcome contributions! Before submitting a PR:

1. **Run tests**: `pytest` or `invoke test`
2. **Run linting**: `ruff check ai_journal_kit tests`
3. **Run security scan**: `bandit -r ai_journal_kit`
4. **Simulate CI**: `invoke ci.local`

All tests must pass on **Ubuntu**, **macOS**, and **Windows** before merging.

---

## 🙏 Credits

Built with love for better journaling and personal growth.

**Author**: Troy Larson ([@troylar](https://github.com/troylar))  
**License**: MIT  
**Repository**: [github.com/troylar/ai-journal-kit](https://github.com/troylar/ai-journal-kit)

---

## ™️ Trademarks & Attribution

**GTD®** and **Getting Things Done®** are registered trademarks of the David Allen Company.

**Bullet Journal®** is a registered trademark of Ryder Carroll.

**PARA™** is a methodology created by Tiago Forte (Forte Labs).

**Zettelkasten** is a note-taking methodology developed by Niklas Luhmann and is not trademarked.

**AI Journal Kit is an independent project** and is not affiliated with, endorsed by, or sponsored by any of the above trademark holders or methodology creators. The software provides templates and folder structures that are compatible with and inspired by these popular productivity methodologies. Users are encouraged to learn more about these methodologies directly from their creators and official resources.

---

## 💝 Support

If AI Journal Kit helps you, consider:

- ⭐ **Star the repo** to help others discover it
- 🐦 **Share your experience** on social media
- 🤝 **Contribute** templates, docs, or code
- 💬 **Spread the word** to friends who journal

---

<div align="center">

---

### 🚀 Ready to Start Your Journaling Journey?

**100% Private • 5 Frameworks • Multi-Journal Support • Works with Your Favorite AI Editor**

```bash
uvx ai-journal-kit setup
```

*Set up in 60 seconds. No cloud required. Your data stays yours.*

**[⭐ Star on GitHub](https://github.com/troylar/ai-journal-kit)** • **[📖 Read the Docs](https://github.com/troylar/ai-journal-kit#readme)** • **[💬 Join Discussions](https://github.com/troylar/ai-journal-kit/discussions)**

</div>
