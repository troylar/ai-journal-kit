# Coverage Report

Show current test coverage without re-running tests.

## Usage
/coverage [--generate]

## Options
- --generate: Run tests and generate fresh coverage report

## Examples
/coverage
/coverage --generate

## Implementation

1. If --generate flag is present:
   - Run `invoke test.coverage` to generate fresh report
   - Open HTML report in browser automatically

2. Otherwise (quick view):
   - Check if `htmlcov/index.html` exists
   - If exists, offer to open it
   - Also show terminal summary from last coverage run

3. Show terminal coverage summary:
   - Run `coverage report` to show text summary
   - Highlight modules below 80% coverage threshold
   - Show overall coverage percentage
   - Compare against target (80%)

4. If no coverage data exists:
   - Inform user no coverage report found
   - Suggest running `/coverage --generate`

## Output Format

```
📊 Coverage Summary (as of [timestamp])

Overall: 87% (target: 80%) ✅

Modules below 80% target:
- ai_journal_kit/cli/move.py: 72% ⚠️
- ai_journal_kit/core/symlinks.py: 75% ⚠️

Top performers (100%):
- ai_journal_kit/cli/app.py
- ai_journal_kit/utils/ui.py

Total: 141 tests passing

Run `/coverage --generate` to update
Open HTML report? [Y/n]
```

## Additional Info

- Coverage reports are in `htmlcov/` directory
- HTML report provides line-by-line coverage details
- Minimum coverage requirement is 80% (enforced in CI)
- Use this to identify areas needing more tests
