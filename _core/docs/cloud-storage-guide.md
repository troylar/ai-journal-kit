# Cloud Storage & Sync Guide

Your `journal/` folder is plain markdown files, making it easy to sync across devices using cloud storage.

## ☁️ Cloud Storage Options

### Option 1: Native Cloud Folders (Easiest)

**Put the entire project in a cloud folder:**

```bash
# Move project to cloud storage
mv ai-markdown-journal ~/Google\ Drive/
cd ~/Google\ Drive/ai-markdown-journal

# Or Dropbox
mv ai-markdown-journal ~/Dropbox/
cd ~/Dropbox/ai-markdown-journal

# Or iCloud Drive (macOS)
mv ai-markdown-journal ~/Library/Mobile\ Documents/com~apple~CloudDocs/
```

**Pros:**
- ✅ Everything syncs automatically
- ✅ Works across all devices
- ✅ No manual setup
- ✅ System files and journal together

**Cons:**
- ⚠️ System files (_core/) also sync (unnecessary but harmless)

---

### Option 2: Journal-Only Sync (Recommended)

**Keep system files local, sync journal only:**

```bash
# Option A: Copy journal to cloud, then symlink
cp -r journal ~/Google\ Drive/my-journal
rm -rf journal
ln -s ~/Google\ Drive/my-journal journal

# Option B: Move journal to cloud, then symlink
mv journal ~/Dropbox/my-journal
ln -s ~/Dropbox/my-journal journal
```

**Pros:**
- ✅ Only journal syncs (efficient)
- ✅ System files stay local (faster updates)
- ✅ Clean separation
- ✅ Smaller sync size

**Cons:**
- ⚠️ Requires symlink setup on each device

---

### Option 3: Separate Git Repository (Advanced)

**Version control your journal separately:**

```bash
cd journal/

# Initialize git in journal folder
git init

# Create private GitHub repo, then:
git remote add origin https://github.com/yourusername/my-private-journal.git
git add .
git commit -m "Initial journal commit"
git push -u origin main
```

**On other devices:**
```bash
cd ai-markdown-journal
rm -rf journal
git clone https://github.com/yourusername/my-private-journal.git journal
```

**Pros:**
- ✅ Full version history
- ✅ Works anywhere with git
- ✅ Easy rollback
- ✅ Professional workflow

**Cons:**
- ⚠️ Requires git knowledge
- ⚠️ Must use PRIVATE repository
- ⚠️ Manual commits needed

---

### Option 4: Obsidian Sync (Obsidian Users)

**Use Obsidian's built-in sync:**

1. Subscribe to Obsidian Sync ($8/month)
2. Open vault in Obsidian
3. Enable sync in settings
4. Choose what to sync (include `journal/`)

**Pros:**
- ✅ Designed for Obsidian
- ✅ End-to-end encrypted
- ✅ Instant sync
- ✅ Mobile support

**Cons:**
- ⚠️ Costs $8/month
- ⚠️ Only works with Obsidian

---

## 📱 Mobile Access

### iOS/Android + Obsidian

```bash
# Setup on computer
# Put project in iCloud Drive or Google Drive

# On mobile
# Install Obsidian app
# Open vault from cloud folder
# Edit notes on the go
```

### iOS + Working Copy (Git)

```bash
# If using git for journal/
# Install Working Copy app (iOS)
# Clone your journal repo
# Open in Obsidian or other markdown editor
```

### Any Cloud + Mobile Markdown App

- **iOS**: 1Writer, iA Writer, Drafts
- **Android**: Markor, Epsilon Notes, Joplin
- **Cross-platform**: Notion, Obsidian, Logseq

---

## 🔄 Multi-Device Workflow

### Recommended Setup

**Computer 1 (Primary):**
```bash
~/projects/ai-markdown-journal/
  ├── _core/          # Local system files
  └── journal/        # Symlinked to ~/Google Drive/journal/
```

**Computer 2:**
```bash
# Clone the system
git clone https://github.com/troylar/ai-journal-kit.git
cd ai-markdown-journal

# Link to cloud journal
rm -rf journal
ln -s ~/Google\ Drive/journal journal

# Get updates anytime
./update-core.sh
```

**Mobile:**
- Access journal via cloud folder
- Use Obsidian mobile or markdown editor

---

## 🔐 Security Considerations

### Private vs. Public

**journal/ folder:**
- ❌ NEVER make public (contains personal notes)
- ✅ Use private GitHub repo if version controlling
- ✅ Encrypt cloud storage if possible
- ✅ Use secure passwords

**_core/ folder:**
- ✅ Public (just templates and docs)
- ✅ Can be freely shared

### Best Practices

1. **Use private repositories** if version controlling journal
2. **Review before committing** to avoid accidental sensitive data
3. **Encrypt cloud storage** for extra security
4. **Use 2FA** on cloud storage accounts
5. **Backup regularly** to local drive as well

---

## 🔧 Configuration

### Tell the System About Your Setup

Update `.ai-journal-config.json`:

```json
{
  "cloud_storage": {
    "type": "google_drive",
    "sync_location": "~/Google Drive/my-journal",
    "notes": "Journal is symlinked from local to cloud"
  }
}
```

This is just documentation for you - doesn't affect functionality.

---

## 🐛 Troubleshooting

### Sync Conflicts

**Google Drive/Dropbox:**
- If conflict occurs, cloud creates duplicate file
- Review both versions
- Merge manually if needed
- Delete duplicate

**Git:**
```bash
# Pull latest before working
git pull

# If conflict occurs
git status  # See conflicted files
# Edit files to resolve
git add .
git commit -m "Resolve conflict"
git push
```

### Symlink Issues

**Broken symlink:**
```bash
# Check if symlink is valid
ls -la journal

# If broken, recreate
rm journal
ln -s ~/Google\ Drive/my-journal journal
```

**Windows (WSL):**
- Symlinks work in WSL
- May have permission issues with Windows cloud folders
- Consider native cloud folder approach instead

### Performance Issues

**Slow sync:**
- Check cloud storage app settings
- Reduce file count (archive old notes)
- Use selective sync if available

**Obsidian slow:**
- Exclude `node_modules/` and other large folders
- Use `.obsidian/workspace` to cache

---

## 📋 Quick Setup Examples

### Google Drive + Symlink

```bash
# Copy journal to Google Drive
cp -r journal ~/Google\ Drive/my-ai-journal

# Remove local journal
rm -rf journal

# Create symlink
ln -s ~/Google\ Drive/my-ai-journal journal

# Verify
ls -la journal  # Should show symlink arrow
```

### Dropbox + Symlink

```bash
# Move journal to Dropbox
mv journal ~/Dropbox/my-ai-journal

# Create symlink
ln -s ~/Dropbox/my-ai-journal journal

# Verify
ls -la journal
```

### GitHub Private Repo

```bash
cd journal/
git init
git add .
git commit -m "Initial journal"

# Create private repo on GitHub, then:
git remote add origin https://github.com/YOU/journal-private.git
git push -u origin main

# On other devices:
cd ai-markdown-journal
rm -rf journal
git clone https://github.com/YOU/journal-private.git journal
```

---

## ✅ Recommended Approach

For most users:

1. **Use native cloud folder** for simplicity (Option 1)
2. **Or use symlink to cloud** for efficiency (Option 2)
3. **Add git** if you want version history (Option 3)

The choice depends on:
- Your technical comfort
- How many devices you use
- Whether you want version history
- Your privacy requirements

---

**Remember:** Your journal is just markdown files. You have complete control over where and how you store them.

