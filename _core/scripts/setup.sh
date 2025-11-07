#!/bin/bash

# AI Markdown Journal - Setup Script
# This script initializes your journal by copying templates and creating the folder structure

set -e  # Exit on error

echo "🚀 Setting up AI Markdown Journal..."
echo ""

# Get the script directory (works from anywhere)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

cd "$PROJECT_ROOT"

# Ask for journal location
echo "📁 Journal Location Setup"
echo ""
echo "Where would you like to store your journal?"
echo "  - Press Enter for local (./journal)"
echo "  - Or enter a custom path (e.g., ~/Documents/my-journal)"
echo ""
read -p "Journal path [./journal]: " JOURNAL_INPUT

# Default to local if empty
if [ -z "$JOURNAL_INPUT" ]; then
    JOURNAL_PATH="$PROJECT_ROOT/journal"
    USE_SYMLINK=false
else
    # Expand ~ to home directory
    JOURNAL_PATH="${JOURNAL_INPUT/#\~/$HOME}"
    
    # Validate path
    JOURNAL_DIR=$(dirname "$JOURNAL_PATH")
    if [ ! -d "$JOURNAL_DIR" ]; then
        echo ""
        echo "⚠️  Warning: Parent directory doesn't exist: $JOURNAL_DIR"
        read -p "Create it? (y/n): " CREATE_DIR
        if [ "$CREATE_DIR" != "y" ]; then
            echo "❌ Setup cancelled."
            exit 1
        fi
        mkdir -p "$JOURNAL_DIR"
    fi
    
    USE_SYMLINK=true
fi

echo ""
echo "📍 Journal will be at: $JOURNAL_PATH"
echo ""

# Ask for IDE preference
echo "🖥️  IDE Setup"
echo ""
echo "Which AI code editor are you using?"
echo "  1. Cursor"
echo "  2. Windsurf"
echo "  3. Claude Code (Cline)"
echo "  4. GitHub Copilot"
echo "  5. Multiple/All"
echo ""
read -p "Enter choice (1-5) [1]: " IDE_CHOICE

case "$IDE_CHOICE" in
    2)
        IDE_NAME="Windsurf"
        SETUP_CURSOR=false
        SETUP_WINDSURF=true
        SETUP_CLAUDE=false
        SETUP_COPILOT=false
        ;;
    3)
        IDE_NAME="Claude Code"
        SETUP_CURSOR=false
        SETUP_WINDSURF=false
        SETUP_CLAUDE=true
        SETUP_COPILOT=false
        ;;
    4)
        IDE_NAME="GitHub Copilot"
        SETUP_CURSOR=false
        SETUP_WINDSURF=false
        SETUP_CLAUDE=false
        SETUP_COPILOT=true
        ;;
    5)
        IDE_NAME="All editors"
        SETUP_CURSOR=true
        SETUP_WINDSURF=true
        SETUP_CLAUDE=true
        SETUP_COPILOT=true
        ;;
    *)
        IDE_NAME="Cursor"
        SETUP_CURSOR=true
        SETUP_WINDSURF=false
        SETUP_CLAUDE=false
        SETUP_COPILOT=false
        ;;
esac

echo ""
echo "✨ Setup for: $IDE_NAME"
echo ""

# Confirm before proceeding
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Setup Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Journal location: $JOURNAL_PATH"
if [ "$USE_SYMLINK" = true ]; then
    echo "🔗 Symlink: journal/ -> $JOURNAL_PATH"
fi
echo "🖥️  IDE: $IDE_NAME"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Proceed with setup? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "❌ Setup cancelled."
    exit 0
fi

echo ""
echo "🚀 Starting setup..."
echo ""

# Create journal folder structure
if [ ! -d "$JOURNAL_PATH" ]; then
    echo "✨ Creating journal folder structure at: $JOURNAL_PATH"
    mkdir -p "$JOURNAL_PATH/daily" "$JOURNAL_PATH/projects" "$JOURNAL_PATH/areas"
    mkdir -p "$JOURNAL_PATH/resources" "$JOURNAL_PATH/people" "$JOURNAL_PATH/archive" "$JOURNAL_PATH/memories"
    mkdir -p "$JOURNAL_PATH/.ai-instructions" "$JOURNAL_PATH/.cursor/rules"
    
    # Create .gitkeep files
    touch "$JOURNAL_PATH/daily/.gitkeep" "$JOURNAL_PATH/projects/.gitkeep" "$JOURNAL_PATH/areas/.gitkeep"
    touch "$JOURNAL_PATH/resources/.gitkeep" "$JOURNAL_PATH/people/.gitkeep" "$JOURNAL_PATH/archive/.gitkeep"
    touch "$JOURNAL_PATH/memories/.gitkeep" "$JOURNAL_PATH/.ai-instructions/.gitkeep"
    
    # Copy system files that need to be in journal/
    echo "📋 Copying AI coach configurations..."
    
    # Copy Cursor rules if selected
    if [ "$SETUP_CURSOR" = true ]; then
        echo "  ✓ Setting up Cursor (.cursor/rules/)"
        if [ -d "$PROJECT_ROOT/journal/.cursor/rules" ]; then
            cp "$PROJECT_ROOT/journal/.cursor/rules/"*.mdc "$JOURNAL_PATH/.cursor/rules/" 2>/dev/null || true
        fi
    fi
    
    # Copy Windsurf rules if selected
    if [ "$SETUP_WINDSURF" = true ]; then
        echo "  ✓ Setting up Windsurf (.windsurf/rules/)"
        mkdir -p "$JOURNAL_PATH/.windsurf/rules"
        if [ -d "$PROJECT_ROOT/journal/.windsurf/rules" ]; then
            cp "$PROJECT_ROOT/journal/.windsurf/rules/"*.md "$JOURNAL_PATH/.windsurf/rules/" 2>/dev/null || true
        fi
    fi
    
    # Copy Claude Code files if selected
    if [ "$SETUP_CLAUDE" = true ]; then
        echo "  ✓ Setting up Claude Code (CLAUDE.md files)"
        [ -f "$PROJECT_ROOT/journal/CLAUDE.md" ] && cp "$PROJECT_ROOT/journal/CLAUDE.md" "$JOURNAL_PATH/"
        [ -f "$PROJECT_ROOT/journal/daily/CLAUDE.md" ] && cp "$PROJECT_ROOT/journal/daily/CLAUDE.md" "$JOURNAL_PATH/daily/"
        [ -f "$PROJECT_ROOT/journal/projects/CLAUDE.md" ] && cp "$PROJECT_ROOT/journal/projects/CLAUDE.md" "$JOURNAL_PATH/projects/"
        [ -f "$PROJECT_ROOT/journal/people/CLAUDE.md" ] && cp "$PROJECT_ROOT/journal/people/CLAUDE.md" "$JOURNAL_PATH/people/"
        [ -f "$PROJECT_ROOT/journal/memories/CLAUDE.md" ] && cp "$PROJECT_ROOT/journal/memories/CLAUDE.md" "$JOURNAL_PATH/memories/"
    fi
    
    # Copy GitHub Copilot files if selected
    if [ "$SETUP_COPILOT" = true ]; then
        echo "  ✓ Setting up GitHub Copilot (.github/)"
        mkdir -p "$JOURNAL_PATH/.github/instructions"
        if [ -d "$PROJECT_ROOT/journal/.github" ]; then
            [ -f "$PROJECT_ROOT/journal/.github/copilot-instructions.md" ] && cp "$PROJECT_ROOT/journal/.github/copilot-instructions.md" "$JOURNAL_PATH/.github/"
            if [ -d "$PROJECT_ROOT/journal/.github/instructions" ]; then
                cp "$PROJECT_ROOT/journal/.github/instructions/"*.md "$JOURNAL_PATH/.github/instructions/" 2>/dev/null || true
            fi
        fi
    fi
    
    # Copy README and example files (always)
    echo "  ✓ Copying README and examples"
    [ -f "$PROJECT_ROOT/journal/README.md" ] && cp "$PROJECT_ROOT/journal/README.md" "$JOURNAL_PATH/"
    [ -f "$PROJECT_ROOT/journal/memories/README.md" ] && cp "$PROJECT_ROOT/journal/memories/README.md" "$JOURNAL_PATH/memories/"
    [ -f "$PROJECT_ROOT/journal/.ai-instructions/README.md" ] && cp "$PROJECT_ROOT/journal/.ai-instructions/README.md" "$JOURNAL_PATH/.ai-instructions/"
    [ -f "$PROJECT_ROOT/journal/.ai-instructions/my-coach.md.example" ] && cp "$PROJECT_ROOT/journal/.ai-instructions/my-coach.md.example" "$JOURNAL_PATH/.ai-instructions/"
else
    echo "✅ Journal folder already exists at: $JOURNAL_PATH"
fi

# Create symlink if using external location
if [ "$USE_SYMLINK" = true ]; then
    if [ -L "$PROJECT_ROOT/journal" ]; then
        echo "🔗 Removing existing journal symlink..."
        rm "$PROJECT_ROOT/journal"
    elif [ -d "$PROJECT_ROOT/journal" ]; then
        echo "⚠️  Local journal/ folder exists. Backing it up to journal.backup..."
        mv "$PROJECT_ROOT/journal" "$PROJECT_ROOT/journal.backup"
    fi
    
    echo "🔗 Creating symlink: journal -> $JOURNAL_PATH"
    ln -s "$JOURNAL_PATH" "$PROJECT_ROOT/journal"
fi

# Create config if it doesn't exist
if [ ! -f ".ai-journal-config.json" ]; then
    echo "⚙️  Creating configuration file..."
    cat > .ai-journal-config.json << EOF
{
  "version": "1.0.0",
  "setup_complete": true,
  "journal_location": "$JOURNAL_PATH",
  "use_symlink": $USE_SYMLINK,
  "ide": "$IDE_NAME",
  "preferences": {
    "daily_template": "_core/templates/daily-template.md",
    "project_template": "_core/templates/project-template.md",
    "area_template": "_core/templates/area-template.md",
    "people_template": "_core/templates/people-template.md",
    "memory_template": "_core/templates/memory-template.md"
  },
  "folders": {
    "daily": "journal/daily",
    "projects": "journal/projects",
    "areas": "journal/areas",
    "resources": "journal/resources",
    "people": "journal/people",
    "archive": "journal/archive",
    "memories": "journal/memories"
  }
}
EOF
fi

# Copy example daily note if journal is empty
if [ ! "$(ls -A "$JOURNAL_PATH/daily" 2>/dev/null | grep -v .gitkeep)" ]; then
    echo "📝 Creating example daily note..."
    TODAY=$(date +%Y-%m-%d)
    if [ -f "$PROJECT_ROOT/_core/examples/2025-11-06-example.md" ]; then
        cp "$PROJECT_ROOT/_core/examples/2025-11-06-example.md" "$JOURNAL_PATH/daily/$TODAY-example.md"
        
        # Update the date in the example
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/November 6, 2025/$(date '+%B %d, %Y')/g" "$JOURNAL_PATH/daily/$TODAY-example.md"
        else
            # Linux
            sed -i "s/November 6, 2025/$(date '+%B %d, %Y')/g" "$JOURNAL_PATH/daily/$TODAY-example.md"
        fi
    fi
fi

# Skip creating README if we already copied it above
if [ ! -f "$JOURNAL_PATH/README.md" ]; then
cat > "$JOURNAL_PATH/README.md" << 'EOF'
# Your Personal Journal

This is your workspace - **completely flexible and yours to customize**.

## Folder Structure

- `daily/` - Your daily notes (one per day: YYYY-MM-DD.md)
- `projects/` - Active projects with clear outcomes and deadlines
- `areas/` - Ongoing areas of responsibility
- `resources/` - Reference material, guides, notes
- `people/` - Relationship notes and 1-on-1s
- `archive/` - Completed projects and old notes

## Getting Started

1. **Daily Notes**: Copy the template from `../_core/templates/daily-template.md`
2. **Projects**: Copy `../_core/templates/project-template.md` when starting new projects
3. **Areas**: Copy `../_core/templates/area-template.md` for ongoing responsibilities

## Documentation

All guides and documentation are in `../_core/docs/guides/`:
- `daily-notes.md` - How to use daily notes
- `projects.md` - Project management guide
- `areas.md` - Managing areas of responsibility
- `resources.md` - Organizing reference material
- `people.md` - Relationship notes guide
- `archive.md` - Archiving completed items

## AI Coach Setup

See `../_core/docs/ai-coach-setup.md` for full AI coach configuration.

Quick start: Use `../_core/instructions/demo-safe.md` for demo-friendly instructions.

## Customization

This is **YOUR** journal. Organize however you want:
- Add subfolders as needed
- Create your own templates
- Adjust folder structure
- Build your own system

The `_core/` folder contains system files that can be updated.
Everything in `journal/` is yours and will never be touched by updates.

---

**Remember**: The best journaling system is the one you actually use.
EOF
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
if [ "$USE_SYMLINK" = true ]; then
    echo "📁 Your journal: $JOURNAL_PATH"
    echo "🔗 Symlink: $PROJECT_ROOT/journal"
else
    echo "📁 Your journal: $PROJECT_ROOT/journal"
fi
echo "🖥️  Configured for: $IDE_NAME"
echo ""
echo "📚 System files: _core/docs/"
echo "📋 Templates: _core/templates/"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 Next Steps"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# IDE-specific instructions
case "$IDE_CHOICE" in
    2)
        echo "1. Open your journal in Windsurf:"
        if [ "$USE_SYMLINK" = true ]; then
            echo "   windsurf \"$JOURNAL_PATH\""
            echo "   Or: windsurf journal/"
        else
            echo "   windsurf journal/"
        fi
        echo ""
        echo "2. Rules are in: .windsurf/rules/"
        ;;
    3)
        echo "1. Open your journal in Claude Code:"
        if [ "$USE_SYMLINK" = true ]; then
            echo "   Open: $JOURNAL_PATH"
        else
            echo "   Open: journal/"
        fi
        echo ""
        echo "2. CLAUDE.md files are in each folder"
        ;;
    4)
        echo "1. Open your journal in VS Code with Copilot:"
        if [ "$USE_SYMLINK" = true ]; then
            echo "   code \"$JOURNAL_PATH\""
        else
            echo "   code journal/"
        fi
        echo ""
        echo "2. Instructions in: .github/copilot-instructions.md"
        ;;
    5)
        echo "1. Open your journal in any AI editor:"
        if [ "$USE_SYMLINK" = true ]; then
            echo "   cursor \"$JOURNAL_PATH\"     # Cursor"
            echo "   windsurf \"$JOURNAL_PATH\"   # Windsurf"
            echo "   code \"$JOURNAL_PATH\"       # VS Code + Copilot"
        else
            echo "   cursor journal/     # Cursor"
            echo "   windsurf journal/   # Windsurf"
            echo "   code journal/       # VS Code + Copilot"
        fi
        echo ""
        echo "2. All editor configs installed"
        ;;
    *)
        echo "1. Open your journal in Cursor:"
        if [ "$USE_SYMLINK" = true ]; then
            echo "   cursor \"$JOURNAL_PATH\""
            echo "   Or: cursor journal/"
        else
            echo "   cursor journal/"
        fi
        echo ""
        echo "2. Rules are in: .cursor/rules/"
        ;;
esac

echo ""
echo "3. Check out the example daily note"
echo ""
echo "4. Start your first check-in by saying:"
echo "   \"get the time and let's start the day\""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Happy journaling! 📝✨"
echo ""

