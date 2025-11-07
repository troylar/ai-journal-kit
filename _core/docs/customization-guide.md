# Customization Guide

AI Markdown Journal is designed to be fully customizable while staying updateable.

## 🎯 Customization Philosophy

### Two Types of Files

**System Files (_core/):**
- Provided by the project
- Can be updated via `./update-core.sh`
- Should NOT be edited directly (will be overwritten)

**User Files (journal/ and custom locations):**
- Completely yours
- Never touched by updates
- Customize freely

### The Pattern

1. **Start with system defaults** from `_core/`
2. **Copy to user location** (in `journal/` or custom folder)
3. **Customize your copy**
4. **Update config** to use your version

---

## 🤖 Customizing AI Coach Behavior

### Quick Start

```bash
# Copy demo-safe instructions as starting point
cp _core/instructions/demo-safe-instructions.md \
   journal/.ai-instructions/my-coach.md

# Edit to your preferences
# vim/nano/code journal/.ai-instructions/my-coach.md
```

Update `.ai-journal-config.json`:
```json
{
  "preferences": {
    "ai_instructions": "journal/.ai-instructions/my-coach.md"
  }
}
```

### What to Customize

#### 1. Coaching Style

```markdown
### Tone & Approach
- [x] Energetic and motivational (Brendon Burchard)
- [ ] Calm and analytical (strategist)
- [ ] Warm and supportive (therapist)
- [ ] Direct and challenging (drill sergeant)
```

#### 2. Your Goals

```markdown
### Current Top 3 Goals
1. **[Your Goal]**
   - Why it matters: [Your reason]
   - Success looks like: [Outcome]
   - Key obstacles: [Challenges]
```

#### 3. Communication Preferences

```markdown
### What I Need From You
- Ask one question at a time
- Use data and metrics
- Challenge me when I make excuses
- End with specific action items
```

#### 4. Habits to Track

```markdown
### Habits I'm Working On
- [ ] Morning workout (6x/week)
- [ ] Journal daily
- [ ] No social media before 10 AM
- [ ] Read for 30 minutes
```

#### 5. Check-in Protocols

```markdown
### Morning Start Trigger
When I say "get the time":
1. Greet warmly
2. Ask about sleep (7-8 hours is my target)
3. Check energy level
4. Ask about TODAY'S top priority (not general goals)
5. Help me block time for it
```

### Multiple Personalities

Create different coach personas for different contexts:

```bash
journal/.ai-instructions/
├── daily-coach.md        # Supportive daily check-ins
├── accountability.md     # No-BS accountability mode
├── deep-work.md         # Focus and flow state
├── therapy-mode.md      # Processing emotions
└── planning.md          # Strategic planning
```

Switch based on context:
```json
{
  "preferences": {
    "ai_instructions": "journal/.ai-instructions/accountability.md"
  }
}
```

---

## 📝 Customizing Templates

### Daily Note Template

```bash
# Copy system template
cp _core/templates/daily-template.md \
   journal/.templates/my-daily.md

# Customize sections
# Add your own sections
# Remove what you don't use
```

Update config:
```json
{
  "preferences": {
    "daily_template": "journal/.templates/my-daily.md"
  }
}
```

### Common Customizations

#### Add Mood Tracking
```markdown
## 😊 Mood & Energy

**Morning mood:** 😊 😐 😔 😤 😰
**Energy level:** ⚡⚡⚡⚡⚡ (X/5)
**Sleep quality:** ★★★★★ (X/5)
```

#### Add Meal Tracking
```markdown
## 🍽️ Meals

**Breakfast:** 
**Lunch:** 
**Dinner:** 
**Snacks:** 
**Water:** [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] (8 glasses)
```

#### Add Exercise Tracking
```markdown
## 💪 Exercise

**Type:** Cardio / Strength / Yoga / Rest
**Duration:** 
**Intensity:** Low / Medium / High
**Notes:** 
```

#### Add Custom Sections
```markdown
## 📚 Learning
**What I learned today:**

## 💰 Financial
**Money spent:** $
**On what:** 

## 🎯 Deep Work
**Pomodoros:** ████ ████ ████ (12)
**Hours:** 
```

---

## 🗂️ Customizing Folder Structure

### Default Structure
```
journal/
├── daily/
├── projects/
├── areas/
├── resources/
├── people/
└── archive/
```

### Your Custom Structure

You can reorganize however you want:

```
journal/
├── daily/
│   ├── 2025/
│   │   ├── 01-january/
│   │   ├── 02-february/
│   │   └── ...
├── work/
│   ├── projects/
│   ├── meetings/
│   └── clients/
├── personal/
│   ├── health/
│   ├── family/
│   └── hobbies/
├── learning/
│   ├── books/
│   ├── courses/
│   └── articles/
└── archive/
```

Update config:
```json
{
  "folders": {
    "daily": "journal/daily",
    "projects": "journal/work/projects",
    "work_meetings": "journal/work/meetings",
    "personal": "journal/personal"
  }
}
```

---

## 🎨 Customizing for Your Workflow

### Example: Developer Workflow

```markdown
## 💻 Dev Log

**Features shipped:**
- 

**Bugs fixed:**
- 

**Code reviews:**
- 

**Learning:**
- 

**Tomorrow's focus:**
- 
```

### Example: Creative Workflow

```markdown
## 🎨 Creative Work

**Project:** 
**Medium:** Writing / Art / Design / Music
**Session length:** 
**Progress:** 

**Breakthrough moments:**

**Stuck on:**

**Next session:**
```

### Example: Health & Fitness Focus

```markdown
## 🏃 Fitness

**Workout:** 
**Duration:** 
**Heart rate:** 
**Calories:** 

## 🥗 Nutrition

**Calories:** Target: 2000 | Actual: 
**Protein:** Target: 150g | Actual: 
**Water:** ████████ (8 glasses)

**Energy levels:**
Morning: ⭐⭐⭐⭐⭐
Afternoon: ⭐⭐⭐⭐⭐
Evening: ⭐⭐⭐⭐⭐
```

---

## 🔗 Custom Integrations

### Config Structure

```json
{
  "integrations": {
    "your_tool": {
      "enabled": true,
      "api_key": "your-key",
      "settings": {
        "auto_sync": true,
        "frequency": "daily"
      }
    }
  }
}
```

### Common Integrations

**Beeminder:**
```json
{
  "integrations": {
    "beeminder": {
      "enabled": true,
      "api_key": "your-key",
      "goals": ["journal-daily", "exercise"]
    }
  }
}
```

**Time Tracking:**
```json
{
  "integrations": {
    "rize": {
      "enabled": true,
      "api_key": "your-key",
      "auto_import": true
    }
  }
}
```

---

## 🛠️ Advanced Customizations

### Custom Scripts

Create your own automation:

```bash
journal/.scripts/
├── new-daily.sh      # Create today's daily note
├── weekly-review.sh  # Generate weekly review
└── backup.sh         # Backup journal
```

Example `new-daily.sh`:
```bash
#!/bin/bash
TODAY=$(date +%Y-%m-%d)
cp ../.templates/my-daily.md ../daily/$TODAY.md
echo "Created: journal/daily/$TODAY.md"
```

### Custom Shortcuts

Add to your shell profile:

```bash
# ~/.zshrc or ~/.bashrc
alias jn='cd ~/ai-markdown-journal && ./journal/.scripts/new-daily.sh'
alias jr='cd ~/ai-markdown-journal/journal/daily'
alias ju='cd ~/ai-markdown-journal && ./update-core.sh'
```

---

## 📊 Data & Analytics

### Custom Tracking

Add structured data for analysis:

```markdown
---
date: 2025-11-06
mood: 4
energy: 3
sleep_hours: 7
exercise: true
social_media_time: 30
deep_work_hours: 4
---
```

Then analyze with scripts:
```bash
# Extract YAML frontmatter
grep -h "^mood:" journal/daily/*.md

# Calculate averages
# Plot trends
# Generate insights
```

---

## 🎯 Best Practices

### 1. Start with Defaults
- Use system defaults first
- Understand what works
- Then customize

### 2. Copy Before Editing
- Never edit `_core/` files directly
- Always copy to `journal/` or custom location
- Keep originals as reference

### 3. Version Control Your Customizations
```bash
cd journal/
git add .ai-instructions/
git add .templates/
git commit -m "Update custom templates"
```

### 4. Document Your Changes
Create `journal/CUSTOMIZATIONS.md`:
```markdown
# My Customizations

## Templates
- Daily: Added mood and meal tracking
- Project: Added client info section

## AI Instructions
- Using accountability mode for weekdays
- Using supportive mode for weekends

## Folder Structure
- Organized daily/ by month
- Added work/ and personal/ top-level folders
```

### 5. Review Periodically
- Monthly: Review what's working
- Quarterly: Refine and simplify
- Yearly: Major restructure if needed

---

## 🔄 Updating While Customized

### Safe Update Process

1. **Run update:**
   ```bash
   ./update-core.sh
   ```

2. **Review changes:**
   ```bash
   # Check what changed in _core/
   git log _core/
   ```

3. **Update your customizations:**
   - Check new templates for ideas
   - Update your copies if you want new features
   - Your custom files are safe

4. **Config is preserved:**
   - `.ai-journal-config.json` never overwritten
   - Your custom paths remain intact

---

## 💡 Inspiration

### Community Templates

Check out community customizations:
- GitHub Discussions
- Share your templates
- Learn from others

### Iterate and Improve

- Start simple
- Add one customization at a time
- Remove what doesn't work
- Keep evolving

---

**Remember:** This is YOUR system. Customize it to match your brain, your workflow, and your goals. There's no "right" way—only what works for you.

