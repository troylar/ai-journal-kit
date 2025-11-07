# Quick Start Guide

Get your AI-powered journal up and running in 5 minutes! ⚡

## Prerequisites (30 seconds)

You need:
- **Python 3.10+** (check: `python --version`)
- **uv** - Fast Python package installer

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# OR
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
```

---

## Step 1: Install & Setup (2 minutes)

Run the setup command - it installs the package and configures everything:

```bash
uvx ai-journal-kit setup
```

### What happens:
1. 📍 **Choose location** - Where to store your journal (default: `~/journal`)
2. 🖥️  **Visual selector** - Pick your AI editor with arrow keys:
   - Cursor ⭐ (recommended)
   - Windsurf
   - Claude Code (Cline)
   - GitHub Copilot
   - All of the above
3. ✅ **Confirm** - Review and confirm your choices
4. 🎉 **Done!** - Journal created with AI coach ready

**Output:**
```
✨ Setup complete!

Next steps:
1. Open /Users/you/journal in your IDE
2. Start journaling with your AI coach
3. Check status anytime: ai-journal-kit status
```

---

## Step 2: Open Your Journal (30 seconds)

Based on your IDE choice:

### Cursor
```bash
cursor ~/journal  # Or your custom path
```
✅ AI coach rules automatically loaded from `.cursor/rules/`

### Windsurf
```bash
windsurf ~/journal
```
✅ Rules loaded from `.windsurf/rules/`

### Claude Code (Cline)
```bash
code ~/journal  # Open with VS Code + Cline extension
```
✅ Hierarchical `CLAUDE.md` files automatically applied

### GitHub Copilot
```bash
code ~/journal
```
✅ Instructions from `.github/copilot-instructions.md` automatically applied

---

## Step 3: Start Journaling with AI! (1 minute)

Just say: **"get the time and let's start the day"**

The AI coach will:
- ✅ Greet you warmly
- ✅ Ask about sleep and energy
- ✅ Help set priorities
- ✅ Create today's daily note
- ✅ **Automatically update notes** as you chat
- ✅ **Offer to capture** significant insights as memories

### Example Session:
```
You: get the time and let's start the day

AI: Good morning! It's 8:30 AM on Thursday, November 7, 2025.

How did you sleep last night?

You: Pretty well, 7 hours

AI: Nice! That's solid rest. 

Energy level this morning? ⭐⭐⭐⭐⭐ (X/5)

You: 4/5

AI: Great! You're feeling energized. What's your top priority for today?

You: Finish the project proposal

AI: Perfect. Let's focus on that. [Creates today's daily note with your priority]
```

---

## CLI Commands

After setup, you have these commands:

```bash
# Check your journal health
uvx ai-journal-kit status

# Show detailed info
uvx ai-journal-kit status --verbose

# Diagnose issues
uvx ai-journal-kit doctor

# Auto-fix problems
uvx ai-journal-kit doctor --fix

# Check for updates
uvx ai-journal-kit update --check

# Update to latest version
uvx ai-journal-kit update

# Move journal to new location
uvx ai-journal-kit move ~/new-location

# See all commands
uvx ai-journal-kit --help
```

---

## Your Journal Structure

Setup created these folders:

```
~/journal/
├── daily/              # Daily notes
├── projects/           # Active projects
├── areas/              # Life areas
├── resources/          # Reference materials
├── people/             # Relationship notes
├── memories/           # Captured insights & breakthroughs
├── archive/            # Completed items
├── .ai-instructions/   # Your custom AI preferences (optional)
└── .cursor/rules/      # AI coach configurations (or .windsurf, .github, etc.)
```

---

## Customize Your AI Coach (Optional)

Want to change how your AI coach behaves?

1. **Check what IDE configs were installed:**
   ```bash
   uvx ai-journal-kit status --verbose
   ```

2. **Edit the coaching rules** in your journal:
   - **Cursor**: Edit `.cursor/rules/*.mdc` files
   - **Windsurf**: Edit `.windsurf/rules/*.md` files
   - **Claude Code**: Edit `CLAUDE.md` files
   - **Copilot**: Edit `.github/copilot-instructions.md`

3. **Or create custom instructions:**
   ```bash
   # Create custom preferences file
   mkdir -p ~/journal/.ai-instructions
   echo "# My Custom Coach Preferences" > ~/journal/.ai-instructions/my-coach.md
   ```

The AI automatically loads your customizations! ✨

---

## Tips for Success

### Start Small
- Just use daily notes for the first week
- Don't organize everything immediately
- Let the system evolve with your needs

### Be Consistent, Not Perfect
- Missing a day? Just start again - no judgment!
- Brief notes are better than no notes
- Progress over perfection

### Use the AI Coach
- **Morning**: "get the time and let's start the day"
- **Evening**: "update my daily note"
- **Stuck**: "I'm feeling overwhelmed"
- **Insights**: AI offers to capture them as memories!

---

## Common Questions

### Where is my journal stored?
```bash
uvx ai-journal-kit status
# Shows: Journal Location: /Users/you/journal
```

### Can I move it later?
```bash
uvx ai-journal-kit move ~/Google\ Drive/journal
# Moves everything safely and updates config
```

### How do I update the system?
```bash
uvx ai-journal-kit update
# Never touches your journal content!
```

### What if something breaks?
```bash
uvx ai-journal-kit doctor --fix
# Auto-repairs common issues
```

### Can I change IDE later?
Yes! Just manually install the configs:
- Look in your Python package location for templates
- Or run setup again for a new location

---

## Need Help?

- **Check status**: `uvx ai-journal-kit status`
- **Diagnose**: `uvx ai-journal-kit doctor`
- **View help**: `uvx ai-journal-kit COMMAND --help`
- **Issues**: [GitHub Issues](https://github.com/troylar/ai-journal-kit/issues)

---

**You're ready! Open your journal and say "get the time and let's start the day" 📝✨**
