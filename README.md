# 📝✨ AI Journal Kit

> **Your Personal AI Coach for Journaling, Growth & Clarity**  
> 100% Private • Fully Customizable • Works with Any Framework

<div align="center">

[![PyPI version](https://badge.fury.io/py/ai-journal-kit.svg)](https://pypi.org/project/ai-journal-kit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[Quick Start](#-quick-start-60-seconds) • [Features](#-why-ai-journal-kit) • [Installation](#-installation) • [Documentation](#-documentation)

</div>

---

## 🎯 Why AI Journal Kit?

### 🔐 **100% Private**
Your journal stays on **YOUR** computer. No cloud sync required. No data collection. No privacy compromises.

### 🎨 **Fully Customizable**
Adapt to **YOUR** workflow. Use any journaling method: GTD, PARA, Bullet Journal, Zettelkasten, or create your own.

### 🤖 **AI-Powered Intelligence**
Your personal AI coach proactively:
- ✅ Updates your notes as you talk
- ✅ Captures insights and breakthroughs
- ✅ Recognizes patterns you might miss
- ✅ Provides accountability without judgment
- ✅ Helps you reflect and grow

### 🛠️ **Works Everywhere**
Built for **YOUR** favorite tools:
- **Cursor** • **Windsurf** • **Claude Code** • **GitHub Copilot**
- Or any markdown editor!

---

## ⚡ Quick Start (60 Seconds)

### 1️⃣ Install & Setup

```bash
uvx ai-journal-kit setup
```

That's it! The AI will guide you through setup interactively.

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
You: "I'm feeling overwhelmed with this project"
AI: "Let's break it down. What's the biggest blocker right now?"
     [Automatically creates project note and captures your thoughts]
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

---

## 🏗️ Architecture

### Two Separate Layers

#### 🔧 **Core System** (Maintained by project)
Templates, AI rules, and tools that can be updated:
```
ai-journal-kit/
├── templates/          # Daily, project, people templates
├── ide-configs/        # AI rules for each editor
└── cli/               # Setup and update tools
```

#### 📓 **Your Journal** (100% Yours)
Your private content that **never changes on update**:
```
~/journal/
├── daily/             # Your daily notes
├── projects/          # Your projects
├── people/            # Your relationships
├── memories/          # Your insights
├── .ai-instructions/  # Your custom AI behavior
└── [any structure you want!]
```

**Updates are safe**: Only the core system updates. Your journal stays untouched!

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

## 🎛️ CLI Commands

```bash
# Interactive setup wizard
ai-journal-kit setup

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

## 🌟 Key Features

### 🎨 **Framework Agnostic**
Not opinionated! Use any journaling methodology:

- **GTD** (Getting Things Done)
- **PARA** (Projects, Areas, Resources, Archive)
- **Bullet Journal**
- **Zettelkasten**
- **Your own system!**

The AI adapts to **YOUR** structure, not the other way around.

### 🛡️ **AI Protection Built-In**
The AI **cannot** modify:
- ✅ Your core system files
- ✅ Your journal content (unless you ask)
- ✅ Your configuration

Safety first!

### 🔄 **Transparent Updates**
When updates change AI behavior:
- ✅ Clear changelog highlighting changes
- ✅ Release notes explaining why
- ✅ You control when to update
- ✅ Templates update with backup

No surprises!

### 🎭 **Multiple Editor Support**

#### Cursor
```
journal/
└── .cursor/
    └── rules/
        ├── journal-coach.mdc
        ├── daily-notes.mdc
        └── system-protection.mdc
```

#### Windsurf
```
journal/
└── .windsurf/
    └── rules/
        ├── journal-coach.md
        └── daily-notes.md
```

#### Claude Code
```
journal/
├── CLAUDE.md          # Root instructions
├── daily/
│   └── CLAUDE.md      # Daily-specific rules
└── projects/
    └── CLAUDE.md      # Project-specific rules
```

#### GitHub Copilot
```
journal/
└── .github/
    ├── copilot-instructions.md
    └── instructions/
        └── daily-notes.instructions.md
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

## 🤝 Contributing

We welcome contributions!

- 🐛 **Bug reports**: [Open an issue](https://github.com/troylar/ai-journal-kit/issues)
- 💡 **Feature requests**: [Start a discussion](https://github.com/troylar/ai-journal-kit/discussions)
- 📖 **Documentation**: Improve guides and examples
- 🎨 **Templates**: Share your custom templates
- 🔧 **Code**: Submit pull requests

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 💬 Community

- **GitHub Discussions**: Ask questions, share tips
- **Issues**: Report bugs, request features
- **Show & Tell**: Share your setup and workflows

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

### ✅ Completed (v1.0)
- Multi-editor support (Cursor, Windsurf, Claude Code, Copilot)
- Cross-platform CLI with beautiful UI
- Automatic memory capture
- Pattern recognition
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
A: Absolutely! Not opinionated. Use GTD, PARA, Bullet Journal, or your own method.

**Q: Will updates break my journal?**  
A: Never. Updates only touch system files, never your content or customizations.

**Q: Can I customize the AI's behavior?**  
A: Yes! Create `.ai-instructions/` files to define your coaching preferences.

**Q: How much does it cost?**  
A: The AI Journal Kit is free and open source (MIT License). You only pay for your chosen AI editor (Cursor, Windsurf, etc.) if using AI features.

**Q: Can I sync across computers?**  
A: Yes! Put your `journal/` folder in Dropbox, Google Drive, or iCloud. The CLI stays installed per-machine.

---

## 🙏 Credits

Built with love for better journaling and personal growth.

**Author**: Troy Larson ([@troylar](https://github.com/troylar))  
**License**: MIT  
**Repository**: [github.com/troylar/ai-journal-kit](https://github.com/troylar/ai-journal-kit)

---

## 💝 Support

If AI Journal Kit helps you, consider:

- ⭐ **Star the repo** to help others discover it
- 🐦 **Share your experience** on social media
- 🤝 **Contribute** templates, docs, or code
- 💬 **Spread the word** to friends who journal

---

<div align="center">

**Ready to transform your journaling?**

```bash
uvx ai-journal-kit setup
```

**Let's go! 📝✨**

</div>
