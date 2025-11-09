# CI Pre-flight Check

Simulate the full CI pipeline locally before pushing.

## Usage
/ci-check

## Implementation

Run the complete CI simulation that mirrors GitHub Actions:

1. Run `invoke ci.local` which executes:
   - Linting checks
   - Security scan with Bandit
   - Full test suite with coverage

2. After completion, show summary:
   - ✅ or ❌ for each step
   - If any step fails, show relevant error details
   - Estimate whether the push will pass CI

3. If all checks pass:
   - Show "✅ Ready to push! CI should pass."
   - Show helpful reminder about the test matrix (12 combinations: 4 Python versions × 3 OSes)
   - Optionally ask if user wants to push now

4. If checks fail:
   - Show which specific checks failed
   - Suggest fix commands (e.g., `invoke lint-fix`)
   - Do NOT proceed with push

## Example Output

```
🚀 Running local CI simulation...

============================================================
STEP 1: Linting
============================================================
🔍 Linting code...
✅ Linting passed!

============================================================
STEP 2: Security Scan
============================================================
🔒 Running security scan...
✅ Security scan complete!

============================================================
STEP 3: Tests
============================================================
🧪 Running all tests with coverage...
✅ All tests complete!

============================================================
✅ ALL CI CHECKS PASSED!
============================================================

✅ Ready to push! Your local environment passes all checks.

Note: CI will run on 12 combinations (Python 3.10-3.13 × Ubuntu/macOS/Windows)
```
