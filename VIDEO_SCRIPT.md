# AI Journal Kit - Video Walkthrough Script

## Opening Hook (30 seconds)

> "I've struggled with journaling for years. Too much manual work. Too inconsistent. Too much judgment when I'd miss days.
> 
> Then I built this AI journal system that's like having a personal coach who automatically takes notes while you talk. It changed my life.
> 
> I published it yesterday. 13 people starred it in 24 hours.
> 
> Let me show you why."

[Show quick B-roll of: AI conversation → auto-updating notes → memory capture]

---

## The Problem (1-2 minutes)

> "Here's the thing about traditional journaling systems:
> 
> **Too much manual overhead:**
> - You have to remember to open your journal
> - You have to create the daily note
> - You have to decide what to write
> - You have to organize it yourself
> - You have to remember to update project notes, people notes, etc.
> 
> **And the worst part?** When you miss a day, there's this guilt. This judgment. This "I failed again" feeling.
> 
> So you avoid it. Which makes the guilt worse. Which makes you avoid it more.
> 
> **I lived this cycle for years.**
> 
> I'd start systems. I'd be consistent for a week. Then life happens. Then I'd stop.
> 
> Not because I didn't want to journal. Because the system required too much from me."

[Show screen: Various journaling apps, complex templates, manual organization]

---

## The Solution (1 minute)

> "So I built something different.
> 
> **AI Journal Kit** is a conversational AI coach that:
> - Talks with you naturally (no forms, no templates unless you want them)
> - Automatically updates your notes as you talk
> - Remembers context across sessions
> - Has zero judgment for gaps
> - Learns YOUR patterns
> 
> It's like having a coach who's also your automatic note-taker.
> 
> **And here's the key:** Your data stays local. No cloud service. No company owning your thoughts. Just you, your journal, and your AI coach running in your IDE.
> 
> Let me show you how it works."

[Show screen: AI Journal Kit logo/README]

---

## Setup Demo (3-4 minutes)

> "Setup is stupidly simple. Watch this."

[Screen record - start from clean terminal]

### Step 1: Install

```bash
pip install ai-journal-kit
```

> "That's it. One command. Python package. Done."

### Step 2: Initialize

```bash
ai-journal init my-journal
cd my-journal
```

> "This creates your journal structure:
> - daily/ - for daily notes
> - projects/ - for active projects
> - people/ - for relationship notes
> - memories/ - for insights and breakthroughs
> - And all the templates and AI instructions"

[Show the folder structure]

### Step 3: Open in IDE

```bash
cursor .
# or code . for VS Code with Copilot
# or windsurf . for Windsurf
```

> "I use Cursor, but this works with GitHub Copilot, Windsurf, and Claude Code.
> 
> The setup automatically configures your IDE to understand the journaling system.
> 
> Now watch what happens..."

[Show opening the chat panel]

---

## Core Features Demo (5-6 minutes)

### Morning Check-in

> "Every morning, I start like this:"

[Type in chat]
```
get the time and let's start the day
```

[AI responds with greeting, asks about sleep, energy level]

> "See how it's natural? It's not a form. It's a conversation.
> 
> And watch what happens in the background..."

[Split screen: Chat + daily note file]

> "It's automatically creating today's daily note and updating it as we talk.
> 
> I didn't have to:
> - Create the file
> - Copy a template
> - Remember the format
> - Manually write anything
> 
> It's all happening automatically."

[Continue conversation - set priorities for the day]

---

### Throughout the Day

> "Now let's say I'm working and I check in with progress:"

[Type in chat]
```
Just finished the proposal draft with Sarah. It went really well - she's excited about the direction and offered to help with the launch plan.
```

[AI responds conversationally]

> "Look at what just happened..."

[Show two files side by side]:
1. Today's daily note - progress entry added
2. people/sarah.md - conversation log updated

> "I didn't say 'log this' or 'update that note.' 
> 
> The AI understood:
> - This is progress worth capturing
> - Sarah is a person in my life
> - This should go in both places
> 
> And it did it automatically while staying conversational."

---

### Memory Capture

> "Here's my favorite feature. Let's say I have a breakthrough:"

[Type in chat]
```
I just realized something. I've been avoiding hard projects because I'm actually afraid of failing. This pattern shows up in my work AND personal life.
```

[AI responds with empathy and offers to capture as memory]

> "See that? It recognized this is significant and offered to save it as a memory.
> 
> If I say yes..."

[Type: "yes please"]

[Show the memory file being created]

> "Now I have a permanent record of this insight. I can reference it later. The AI can remind me of it when relevant patterns show up.
> 
> **This is how you build a personal wisdom library.**
> 
> Insights you'd normally forget? Captured forever."

---

### Evening Reflection

> "At the end of the day:"

[Type in chat]
```
update my daily note
```

[AI reviews the day, asks about progress, captures wins/challenges/learnings]

> "It reviews everything we discussed, helps me reflect, and makes sure the day is properly documented.
> 
> All through conversation. No forms. No templates unless I want them."

---

## The Secret Sauce (2-3 minutes)

> "So what makes this different from other AI journaling tools?"

### 1. No Judgment Protocol

> "Most systems make you feel bad when you miss days. This one doesn't."

[Show example: Coming back after a gap]

```
User: "get the time - it's been 6 days"
AI: "Welcome back! No judgment about the gap - you're here now. Want to catch up or just jump into today?"
```

> "See that? No guilt. No shame. Just support.
> 
> Because the system understands that consistency is great, but LIFE HAPPENS."

---

### 2. Proactive Updates

> "It doesn't wait for you to say 'update this note.'
> 
> It listens for meaningful information and captures it automatically.
> 
> This is the difference between a chatbot and a coach who's actually paying attention."

---

### 3. Pattern Recognition

> "Over time, it learns YOUR patterns:
> - When you tend to procrastinate
> - What triggers overwhelm
> - What gives you energy
> - What drains you
> 
> And it reflects these back to help you see yourself more clearly."

---

### 4. Fully Customizable

[Show `.ai-instructions/my-coach.md`]

> "You can customize how it talks to you:
> - Energetic and motivational? (like a Brendon Burchard coach)
> - Calm and reflective? (like a therapist)
> - Direct and practical? (like a mentor)
> 
> It adapts to YOU."

---

### 5. Your Data, Your Control

> "Here's the most important part:
> 
> **This is not a cloud service.**
> 
> Your journal lives on YOUR computer. Your notes are markdown files YOU own. The AI runs in YOUR IDE using your existing API keys.
> 
> No company mining your thoughts for training data.
> No subscription that locks your journal behind a paywall.
> No service that can shut down and take your life's work with it.
> 
> **This is YOUR journal. Period.**"

---

## The Real Impact (1-2 minutes)

> "I want to be real with you about why I built this.
> 
> I struggled with sleep for YEARS. Waking up multiple times a night. Checking my worth by working at 4:30 AM.
> 
> This journal system helped me process the patterns underneath that behavior.
> 
> Now? I sleep through the night. First time in years.
> 
> This isn't just about productivity or organization.
> 
> **This is about self-awareness, healing, and growth.**
> 
> And apparently, I'm not the only one who needed this. 13 stars in 24 hours tells me other people are struggling with the same things."

---

## Call to Action (30 seconds)

> "If this resonates with you:
> 
> **1. Try it:** Link in description to the GitHub repo
> 
> **2. Star it:** If you think others need this too
> 
> **3. Comment:** Tell me what journaling challenges you face
> 
> **4. Reach out:** I'm considering offering mentoring to help people build custom systems like this. DM me if that interests you.
> 
> I'm Troy Larson. This is my journey. And maybe it can help yours too.
> 
> Thanks for watching."

---

## B-Roll / Screen Recording Shots Needed

1. Terminal showing install command
2. Folder structure being created
3. Opening in Cursor/IDE
4. AI chat panel conversation
5. Split screen: chat + notes updating in real-time
6. Memory file being created
7. `.ai-instructions/my-coach.md` customization
8. GitHub repo page
9. Daily notes folder with multiple days
10. Project structure overview

---

## Thumbnail Ideas

1. "I Built an AI Coach That Changed My Life" + screenshot of AI conversation
2. "13 GitHub Stars in 24 Hours" + repo screenshot
3. "The Journal System I Actually Use Daily" + folder structure
4. Split screen: You + AI conversation visible

---

## YouTube Title Options

1. "I Built an AI Journal Coach That Writes My Notes While We Talk"
2. "This AI Journaling System Changed My Life (Here's How It Works)"
3. "AI Journal Kit: The Personal Coach That Never Judges"
4. "How I Built a Journaling System I Actually Use Every Day"

## LinkedIn Post Version (Shorter, 3-5 minutes)

Same structure but condensed:
- 30 sec hook + problem
- 1 min setup demo
- 2 min core features
- 30 sec CTA

Focus on: "From idea to 13 stars in 24 hours - here's the journaling system I built for myself that others actually wanted."

---

## Technical Setup for Recording

**Screen Recording:**
- Use QuickTime or OBS for screen capture
- Show Cursor IDE in full screen
- Picture-in-picture of you in corner (optional)
- Clear audio (use good mic)

**Resolution:**
- 1920x1080 minimum
- Make sure text is readable

**Prepare Before Recording:**
- Fresh journal folder
- Clean terminal
- Prepared prompts
- Example notes ready to show

**Consider:**
- Multiple takes are fine
- Edit out pauses/mistakes
- Add music (subtle, don't overpower voice)
- Add text overlays for key points

---

## Post-Production Checklist

- [ ] Intro hook grabs attention in first 10 seconds
- [ ] Clear audio throughout
- [ ] Screen readable (text not too small)
- [ ] Pacing keeps energy up
- [ ] B-roll covers talking head moments
- [ ] CTA is clear and actionable
- [ ] Add GitHub link in description
- [ ] Add timestamps in description
- [ ] Add relevant tags/keywords
- [ ] Thumbnail is eye-catching

---

## Follow-Up Content Ideas

After this walkthrough, create:
1. **Deep dives** - Advanced features, customization
2. **Use cases** - How different people use it
3. **Build series** - How you built it (for technical audience)
4. **Journey stories** - Personal transformations
5. **Q&A** - Answer common questions from comments

**You've got this, Troy. Show the world what you built.** 💪

