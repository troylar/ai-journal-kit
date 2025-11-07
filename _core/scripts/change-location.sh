#!/bin/bash

# AI Markdown Journal - Change Journal Location
# This script helps you move your journal to a different location

set -e  # Exit on error

echo "📁 Change Journal Location"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

cd "$PROJECT_ROOT"

# Check if config exists
if [ ! -f ".ai-journal-config.json" ]; then
    echo "❌ Configuration file not found. Have you run setup.sh yet?"
    exit 1
fi

# Show current location
if [ -f ".ai-journal-config.json" ]; then
    CURRENT_PATH=$(grep "journal_location" .ai-journal-config.json | cut -d'"' -f4)
    echo "📍 Current journal location: $CURRENT_PATH"
fi

echo ""
echo "Where would you like to move your journal?"
echo ""
echo "Options:"
echo "  1. Local (default) - ./journal"
echo "  2. Google Drive - ~/Google Drive/my-journal"
echo "  3. Dropbox - ~/Dropbox/my-journal"
echo "  4. Custom path"
echo "  5. Cancel"
echo ""
read -p "Enter choice (1-5): " JOURNAL_CHOICE

case "$JOURNAL_CHOICE" in
    1)
        NEW_JOURNAL_PATH="$PROJECT_ROOT/journal"
        USE_SYMLINK=false
        ;;
    2)
        NEW_JOURNAL_PATH="$HOME/Google Drive/my-ai-journal"
        USE_SYMLINK=true
        ;;
    3)
        NEW_JOURNAL_PATH="$HOME/Dropbox/my-ai-journal"
        USE_SYMLINK=true
        ;;
    4)
        read -p "Enter full path for your journal: " NEW_JOURNAL_PATH
        # Expand ~ to home directory
        NEW_JOURNAL_PATH="${NEW_JOURNAL_PATH/#\~/$HOME}"
        USE_SYMLINK=true
        ;;
    5)
        echo "Cancelled."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice."
        exit 1
        ;;
esac

echo ""
echo "📍 New location: $NEW_JOURNAL_PATH"
echo ""

# Confirm
read -p "Do you want to MOVE your existing journal to this location? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "Cancelled."
    exit 0
fi

# Create parent directory if needed
mkdir -p "$(dirname "$NEW_JOURNAL_PATH")"

# Move journal
if [ -d "$CURRENT_PATH" ] && [ "$CURRENT_PATH" != "$NEW_JOURNAL_PATH" ]; then
    echo "📦 Moving journal from $CURRENT_PATH to $NEW_JOURNAL_PATH..."
    
    if [ -d "$NEW_JOURNAL_PATH" ]; then
        echo "⚠️  Target directory already exists!"
        read -p "Merge with existing directory? (y/n): " MERGE
        if [ "$MERGE" = "y" ]; then
            cp -r "$CURRENT_PATH/"* "$NEW_JOURNAL_PATH/"
            echo "✅ Merged journals"
        else
            echo "Cancelled."
            exit 1
        fi
    else
        mv "$CURRENT_PATH" "$NEW_JOURNAL_PATH"
        echo "✅ Moved journal"
    fi
fi

# Update symlink
if [ "$USE_SYMLINK" = true ]; then
    # Remove old symlink/folder
    if [ -L "$PROJECT_ROOT/journal" ]; then
        rm "$PROJECT_ROOT/journal"
    elif [ -d "$PROJECT_ROOT/journal" ] && [ "$PROJECT_ROOT/journal" != "$NEW_JOURNAL_PATH" ]; then
        echo "⚠️  Backing up local journal/ to journal.backup..."
        mv "$PROJECT_ROOT/journal" "$PROJECT_ROOT/journal.backup"
    fi
    
    # Create new symlink
    echo "🔗 Creating symlink: journal -> $NEW_JOURNAL_PATH"
    ln -s "$NEW_JOURNAL_PATH" "$PROJECT_ROOT/journal"
else
    # Remove symlink if exists and we're going local
    if [ -L "$PROJECT_ROOT/journal" ]; then
        rm "$PROJECT_ROOT/journal"
    fi
fi

# Update config
echo "⚙️  Updating configuration..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|\"journal_location\": \".*\"|\"journal_location\": \"$NEW_JOURNAL_PATH\"|" .ai-journal-config.json
    sed -i '' "s|\"use_symlink\": .*|\"use_symlink\": $USE_SYMLINK,|" .ai-journal-config.json
else
    # Linux
    sed -i "s|\"journal_location\": \".*\"|\"journal_location\": \"$NEW_JOURNAL_PATH\"|" .ai-journal-config.json
    sed -i "s|\"use_symlink\": .*|\"use_symlink\": $USE_SYMLINK,|" .ai-journal-config.json
fi

echo ""
echo "✅ Journal location updated!"
echo ""
echo "📁 Your journal is now at: $NEW_JOURNAL_PATH"
if [ "$USE_SYMLINK" = true ]; then
    echo "🔗 Accessible via: $PROJECT_ROOT/journal (symlink)"
fi
echo ""
echo "🎯 Next steps:"
echo "  1. Open your journal in your AI editor:"
if [ "$USE_SYMLINK" = true ]; then
    echo "     cursor \"$NEW_JOURNAL_PATH\"      # Direct path"
    echo "     cursor journal/                  # Via symlink"
else
    echo "     cursor journal/"
fi
echo ""

