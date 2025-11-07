# Cursor AI Setup Guide

AI Markdown Journal is **Cursor-first** - the AI coach is pre-configured using modern `.mdc` rules and ready to use!

## 🚀 Quick Start (Cursor Users)

### 1. Open in Cursor

```bash
# Clone or download the repo
git clone https://github.com/troylar/ai-journal-kit.git

# Open the JOURNAL folder in Cursor (not root)
cursor ai-markdown-journal/journal
```

**Important:** Open the `journal/` folder as your workspace, not the root `ai-markdown-journal/` folder. This keeps you focused on your content without seeing system files.

### 2. Start Journaling

The AI coach is already configured! Just start chatting:

```
You: "get the time and let's start the day"

AI: [Greets you, asks about sleep, helps plan your day]
```

### 3. (Optional) Customize AI Behavior

```bash
# Copy the example customization file
cp journal/.ai-instructions/my-coach.md.example \
   journal/.ai-instructions/my-coach.md

# Edit to match your preferences
# Cursor automatically picks up changes
```

That's it! 🎉

---

## How It Works

### Modern MDC Rules

The system uses [Cursor's modern rules format](https://cursor.com/docs/context/rules) with `.mdc` files in `.cursor/rules/`:

**4 Composable Rules:**

1. **journal-coach.mdc** (Always Apply)
   - Core AI coaching behavior
   - Check-in protocols
   - No-judgment guidelines
   - Conversation patterns

2. **daily-notes.mdc** (Apply to daily/*.md)
   - Daily note creation helpers
   - Date formatting
   - Template copying
   - Linking strategies

3. **projects.mdc** (Apply to projects/*.md)
   - Project management guidance
   - Template usage
   - Project vs Area distinction
   - Completion workflows

4. **user-customizations.mdc** (Always Apply)
   - Loads your preferences from `.ai-instructions/`
   - Overrides system defaults
   - Multiple personality support

### Benefits of MDC Format

- **Composable**: Rules combine intelligently
- **Scoped**: Rules apply only when relevant
- **Version-controlled**: Easy to track changes
- **Best practice**: Following Cursor's modern approach
- **Visible**: See all rules in Cursor Settings → Rules

---

## Customization Workflow

### 1. Copy Example to My-Coach

```bash
cp journal/.ai-instructions/my-coach.md.example \
   journal/.ai-instructions/my-coach.md
```

### 2. Edit Your Preferences

Open `journal/.ai-instructions/my-coach.md` and customize:

```markdown
## MY COACHING PREFERENCES

### Coaching Style
- [x] Energetic and motivational (Brendon Burchard style)
- [ ] Calm and analytical
- [ ] Warm and supportive
- [ ] Direct and challenging

### Communication Preferences
- [x] Ask one question at a time
- [x] Use data and metrics
- [x] Challenge me when I make excuses

### What I Need From You
- Push me to take action, not just reflect
- Remind me of my goals when I get distracted
- Celebrate wins without being over-the-top
```

### 3. Reload Cursor

Cursor automatically picks up changes, but you can force reload:
- `Cmd+Shift+P` → "Developer: Reload Window"

---

## Multiple AI Personalities

Create different coach modes for different contexts:

```bash
journal/.ai-instructions/
├── my-coach.md              # Default coaching
├── accountability.md        # No-BS accountability mode
├── deep-work.md            # Focus session coach
├── planning.md             # Strategic planning mode
└── supportive.md           # Extra supportive mode
```

To switch modes:
1. Rename files (e.g., `mv accountability.md my-coach.md`)
2. Or edit `.cursorrules` to reference different file
3. Reload Cursor

---

## Common Customizations

### Change Coaching Tone

```markdown
### Coaching Style
- [x] Direct and challenging
- Challenge me hard when I make excuses
- Don't let me off the hook
- Push for specific commitments
```

### Add Custom Habits

```markdown
### Habits I'm Working On
- [ ] Morning workout (6x/week) - Health goal
- [ ] No social media before 10 AM - Focus goal
- [ ] Journal every evening - Reflection goal
- [ ] Read for 30 minutes - Learning goal

### How to Support My Habits
- Ask about them every morning check-in
- Track streaks and celebrate them
- Help me troubleshoot when I miss
- NEVER shame - just curiosity and support
```

### Customize Check-In Protocol

```markdown
### Morning Start
When I say "get the time":
1. Get the current time
2. Greet me warmly
3. Ask about sleep (target: 7-8 hours)
4. Check energy level (1-5)
5. Ask: "What's THE ONE thing that matters most today?"
6. Help me block 2-hour focused session for it
7. End with: "You've got this! Let's go!"
```

---

## Working with Daily Notes

### Creating Today's Note

```
You: "create today's daily note"

AI: [Creates journal/daily/YYYY-MM-DD.md from template]
```

The AI knows how to:
- Calculate today's date
- Copy template to correct location
- Handle both bash and fish shell syntax
- Open the note for editing

### Reading Your Notes

```
You: "what did I work on yesterday?"

AI: [Reads journal/daily/YYYY-MM-DD.md and summarizes]
```

### Updating Notes

```
You: "update my daily note with today's progress"

AI: [Reviews your day, asks questions, helps reflect]
```

---

## Tips for Success

### 1. Start Your Day with AI

Every morning:
```
You: "get the time and let's start the day"
```

This becomes your daily ritual.

### 2. Check In Throughout Day

Share progress, challenges, wins:
```
You: "Just finished the proposal!"
You: "Feeling stuck on this problem"
You: "Energy is low today"
```

### 3. End Day with Reflection

Every evening:
```
You: "update my daily note"
```

AI helps you capture learnings and prepare tomorrow.

### 4. Be Authentic

The AI doesn't judge. Share struggles, fears, wins, all of it.

### 5. Iterate Your Customizations

Try different coaching styles, habits, check-in formats.
Find what works for YOU.

---

## Advanced: Editing `.cursorrules` Directly

If you want to modify the core loader logic:

```bash
# Make it private first
echo ".cursorrules" >> .gitignore

# Then edit
code .cursorrules
```

You can:
- Change how system and custom instructions combine
- Add additional instruction sources
- Modify the base prompts
- Add custom tool configurations

But 99% of customization should happen in `journal/.ai-instructions/`!

---

## Troubleshooting

### AI Not Using My Customizations

1. Check file exists: `ls journal/.ai-instructions/my-coach.md`
2. Check file has content: `cat journal/.ai-instructions/my-coach.md`
3. Reload Cursor: `Cmd+Shift+P` → "Developer: Reload Window"

### AI Behavior Seems Off

1. Check `.cursorrules` is present
2. Verify it references correct paths
3. Check for syntax errors in your custom files

### Want to Reset to Defaults

```bash
# Remove your customizations
rm journal/.ai-instructions/my-coach.md

# Reload Cursor
# Will use system defaults
```

---

## Cursor-Specific Features

### Codebase Awareness

The AI knows about:
- Your journal structure
- Available templates
- Documentation locations
- Where to create files

### Multi-File Context

The AI can:
- Read multiple daily notes
- Compare patterns across weeks
- Reference your projects and areas
- Link related notes

### File Operations

The AI can:
- Create new notes from templates
- Update existing notes
- Search your journal
- Organize files

---

## Privacy & Security

### What's Included in Context

The AI can read:
- Your journal notes (when you ask)
- System documentation
- Templates
- Your custom instructions

### What's Private

- Your `.cursorrules` (if you gitignore it)
- Your `journal/.ai-instructions/` files (gitignored by default)
- All your journal content (gitignored by default)

### Best Practices

1. Don't commit API keys to `.cursorrules`
2. Use gitignore for sensitive customizations
3. Review context before sharing workspace
4. Keep private journal separate from shared projects

---

## FAQ

**Q: Do I need to edit `.cursorrules`?**
A: No! Just customize files in `journal/.ai-instructions/`

**Q: Can I use this without Cursor?**
A: Yes! See `_core/docs/ai-coach-setup.md` for Claude, ChatGPT, etc.

**Q: Will updates overwrite my `.cursorrules`?**
A: By default, no - it's tracked in git. But you can gitignore it if you customize heavily.

**Q: How do I switch between different AI personalities?**
A: Rename your instruction files or edit `.cursorrules` to reference different ones.

**Q: Can I share my customizations?**
A: Yes! Just share files from `journal/.ai-instructions/` (remove personal info first).

---

**Ready to go! Open Cursor, start chatting, and let's build momentum!** 🚀

