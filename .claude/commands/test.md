# Run Tests

Run AI Journal Kit tests with common configurations.

## Usage
/test [type] [options]

## Arguments
- type: unit|integration|e2e|all|quick (default: all)
- options: --verbose, --coverage, --parallel

## Examples
/test unit
/test integration --verbose
/test quick
/test all --coverage

## Implementation

Based on the type argument:

1. **unit**: Run `invoke test.unit` - Fast unit tests only
2. **integration**: Run `invoke test.integration` - Integration tests
3. **e2e**: Run `invoke test.e2e` - End-to-end tests
4. **quick**: Run `invoke test.quick` - Fast run without coverage
5. **all**: Run `invoke test` - Full test suite with coverage

If --verbose flag is present, add `--verbose` to the invoke command.
If --coverage flag is present, ensure coverage reporting is enabled.

After running tests:
- Report pass/fail status clearly
- If failures occur, show the failed test names
- Suggest relevant fixes based on failure types
- Show coverage summary if available

## Example Output

```
🧪 Running unit tests...

================================ test session starts =================================
...
================================= 45 passed in 2.3s =================================

✅ Unit tests passed! (45 tests)
```
