#!/bin/bash
# Validate template modifications

COMMAND="$1"

# Only check when editing template files
if [[ ! "$COMMAND" =~ templates.*\.md ]]; then
  exit 0
fi

echo "📝 Validating template files..."

# Check all markdown templates exist
REQUIRED_TEMPLATES=(
  "ai_journal_kit/templates/daily-template.md"
  "ai_journal_kit/templates/project-template.md"
  "ai_journal_kit/templates/people-template.md"
  "ai_journal_kit/templates/memory-template.md"
  "ai_journal_kit/templates/WELCOME.md"
)

for template in "${REQUIRED_TEMPLATES[@]}"; do
  if [ ! -f "$template" ]; then
    echo "❌ Missing required template: $template"
    exit 1
  fi

  # Check it's not empty
  if [ ! -s "$template" ]; then
    echo "❌ Template is empty: $template"
    exit 1
  fi
done

# Validate IDE config directories exist
IDE_CONFIGS=(
  "ai_journal_kit/templates/ide-configs/cursor"
  "ai_journal_kit/templates/ide-configs/windsurf"
  "ai_journal_kit/templates/ide-configs/claude-code"
  "ai_journal_kit/templates/ide-configs/copilot"
)

for config_dir in "${IDE_CONFIGS[@]}"; do
  if [ ! -d "$config_dir" ]; then
    echo "❌ Missing IDE config directory: $config_dir"
    exit 1
  fi
done

echo "✅ All templates validated!"
exit 0
