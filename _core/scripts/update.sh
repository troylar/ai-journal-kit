#!/bin/bash

# AI Markdown Journal - Update Script
# This script updates the _core/ system files from the GitHub repository

set -e  # Exit on error

echo "🔄 Updating AI Markdown Journal core files..."
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

cd "$PROJECT_ROOT"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository"
    echo "This update script only works if you cloned from GitHub."
    echo ""
    echo "To manually update:"
    echo "  1. Download latest from: https://github.com/troylar/ai-journal-kit"
    echo "  2. Copy _core/ folder to replace your existing _core/"
    echo "  3. Your journal/ folder will not be affected"
    exit 1
fi

# Save current branch
CURRENT_BRANCH=$(git branch --show-current)

echo "📋 Current branch: $CURRENT_BRANCH"
echo ""

# Check for uncommitted changes in _core/
if [ -n "$(git status --porcelain _core/)" ]; then
    echo "⚠️  Warning: You have uncommitted changes in _core/"
    echo ""
    git status --porcelain _core/
    echo ""
    read -p "Continue with update? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Update cancelled."
        exit 1
    fi
fi

# Backup _core/ before update
echo "💾 Creating backup of _core/..."
BACKUP_DIR="_core_backup_$(date +%Y%m%d_%H%M%S)"
cp -r _core "$BACKUP_DIR"
echo "Backup saved to: $BACKUP_DIR"
echo ""

# Fetch latest changes
echo "📥 Fetching latest changes from GitHub..."
git fetch origin

# Update _core/ folder only
echo "🔄 Updating _core/ folder..."
git checkout origin/main -- _core/

# Also update root documentation if desired
read -p "Update README.md and other root docs? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📄 Updating root documentation..."
    git checkout origin/main -- README.md CONTRIBUTING.md LICENSE
fi

echo ""
echo "✅ Update complete!"
echo ""
echo "📁 Updated: _core/ folder"
echo "🔒 Protected: journal/ folder (your content was not touched)"
echo "💾 Backup: $BACKUP_DIR"
echo ""
echo "🎯 What's new?"
echo "  Check _core/CHANGELOG.md for details"
echo ""
echo "⚠️  Note: If you customized any files in _core/, check the backup."
echo ""
echo "To restore from backup:"
echo "  rm -rf _core && mv $BACKUP_DIR _core"

