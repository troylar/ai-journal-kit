# Quick Setup Guide

## ✅ Installation Complete!

All Claude Code features have been installed. Here's what you need to do to activate them:

---

## 🔑 Required: GitHub Token Setup

**Why?** The GitHub MCP server enables seamless issue/PR management and ensures compliance with your CLAUDE.md requirement that all work must be tied to GitHub issues.

### Steps:

1. **Create a GitHub Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: `Claude Code - AI Journal Kit`
   - Select scopes:
     - ✅ `repo` (Full repository access)
     - ✅ `read:org` (Read organization data)
     - ✅ `read:user` (Read user profile data)
   - Click "Generate token"
   - **Copy the token** (you won't see it again!)

2. **Set the environment variable:**

   Add to `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:
   ```bash
   export GITHUB_TOKEN='ghp_your_token_here'
   ```

3. **Reload your shell:**
   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

4. **Verify it's set:**
   ```bash
   echo $GITHUB_TOKEN
   ```

---

## 🧪 Test the Features

### 1. Test a Slash Command
```
/test quick
```

Should run quick tests without coverage.

### 2. Test GitHub MCP Integration
```
"List all open issues in this repository"
```

Should show your GitHub issues (requires token setup above).

### 3. Test Pre-commit Hook
```bash
# Make a small change
echo "# test" >> test.txt
git add test.txt
git commit -m "test"
```

Should run pre-commit checks (formatting, linting, security, tests).

Clean up:
```bash
git reset HEAD~1
rm test.txt
```

---

## 📋 Available Commands

Quick reference:

| Command | Purpose | Example |
|---------|---------|---------|
| `/test [type]` | Run tests | `/test unit --verbose` |
| `/ci-check` | Pre-flight CI check | `/ci-check` |
| `/coverage` | View coverage | `/coverage --generate` |
| `/release [version]` | Automated release | `/release 1.0.11 --test-pypi` |

---

## 🪝 Active Hooks

Hooks run automatically:

- **Pre-commit safety** - Runs before `git commit` (blocks broken commits)
- **Template validation** - Runs after editing templates (ensures integrity)

---

## 🚀 Optional: PyPI Token Setup (for releases)

Only needed when you want to use the `/release` command:

1. **Get PyPI API token:**
   - Go to: https://pypi.org/manage/account/token/
   - Create token with scope for `ai-journal-kit`

2. **Set environment variable:**
   ```bash
   export PYPI_TOKEN='pypi-...'
   ```

3. **For test releases (optional):**
   ```bash
   export TEST_PYPI_TOKEN='pypi-...'
   ```

---

## 📖 Full Documentation

See `.claude/README.md` for complete documentation including:
- Detailed command usage
- Hook configurations
- Troubleshooting
- Expected impact and benefits

---

## ✨ You're Ready!

All features are now active. Try running:

```
/test quick
```

Or ask Claude:
```
"Create a GitHub issue for my next feature"
```

**Happy coding!** 🎉
