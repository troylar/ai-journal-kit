#!/bin/bash
# Pre-commit safety check for AI Journal Kit

COMMAND="$1"

# Only trigger on git commit commands
if [[ ! "$COMMAND" =~ ^git[[:space:]]+commit ]]; then
  exit 0
fi

echo "🎯 Running pre-commit checks..."

# 1. Format check
echo "1️⃣ Checking code formatting..."
ruff format --check ai_journal_kit tests 2>/dev/null
FORMAT_EXIT=$?
if [ $FORMAT_EXIT -ne 0 ]; then
  echo "❌ Code formatting failed. Run: ruff format ai_journal_kit tests"
  exit 1
fi
echo "✅ Formatting OK"

# 2. Lint check
echo "2️⃣ Running linter..."
ruff check ai_journal_kit tests 2>/dev/null
LINT_EXIT=$?
if [ $LINT_EXIT -ne 0 ]; then
  echo "❌ Linting failed. Run: ruff check ai_journal_kit tests --fix"
  exit 1
fi
echo "✅ Linting OK"

# 3. Security scan
echo "3️⃣ Running security scan..."
bandit -r ai_journal_kit/ -c .bandit -q 2>/dev/null
SECURITY_EXIT=$?
if [ $SECURITY_EXIT -ne 0 ]; then
  echo "❌ Security scan found issues. Run: bandit -r ai_journal_kit/ -c .bandit"
  exit 1
fi
echo "✅ Security OK"

# 4. Quick tests
echo "4️⃣ Running quick tests..."
pytest --no-cov -x -q 2>/dev/null
TEST_EXIT=$?
if [ $TEST_EXIT -ne 0 ]; then
  echo "❌ Tests failed. Fix failing tests before committing."
  exit 1
fi
echo "✅ Tests OK"

echo ""
echo "✅ ALL PRE-COMMIT CHECKS PASSED!"
exit 0
