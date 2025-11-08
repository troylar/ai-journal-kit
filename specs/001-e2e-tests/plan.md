# Implementation Plan: Integration & E2E Test Suite

**Branch**: `001-e2e-tests` | **Date**: 2025-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-e2e-tests/spec.md`

## Summary

Add comprehensive integration and end-to-end test coverage for all CLI commands (setup, update, status, doctor, move) with cross-platform validation. Tests will ensure data integrity, validate error handling, and verify user-facing functionality works correctly across Windows, macOS, and Linux. Primary focus on setup flow (P1), update preservation (P2), and diagnostic commands (P3).

**Technical Approach**: Extend existing pytest infrastructure with dedicated integration and e2e test suites, using pytest fixtures for test isolation, CliRunner for fast integration tests, and subprocess for true e2e validation.

## Technical Context

**Language/Version**: Python 3.10+ (project requires 3.10+)  
**Primary Dependencies**: pytest, pytest-bdd, pytest-xdist, typer, click  
**Storage**: File system (markdown files, JSON config)  
**Testing**: pytest with Click CliRunner + subprocess for e2e  
**Target Platform**: Cross-platform (Windows, macOS, Linux)  
**Project Type**: Single CLI application  
**Performance Goals**: <10 minutes for full test suite on CI/CD, <5 seconds per integration test  
**Constraints**: Must test real file I/O, must not interfere with developer's journal  
**Scale/Scope**: ~50-100 new integration/e2e tests covering 5 CLI commands across 3 platforms

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Relevant Principles

✅ **Principle I - Modular Architecture**: Tests MUST verify separation between core (`_core/`) and user content. Integration tests MUST validate that updates don't modify user journal entries.

✅ **Principle II - Multi-Editor Support**: Tests MUST validate IDE config installation for all supported editors (Cursor, Windsurf, Claude Code, Copilot, All).

✅ **Principle III - Flexible Journal Location**: Tests MUST verify journal creation at custom paths, including cloud sync locations and symlink handling.

✅ **Principle V - Privacy & Data Ownership**: Tests MUST validate that journal data remains in plain text markdown, no external dependencies required for core functionality.

✅ **Principle VI - Proactive Intelligence**: Not applicable to testing infrastructure (N/A)

✅ **Principle VII - User Customization Override**: Tests MUST verify that custom `.ai-instructions/` files are preserved during updates.

✅ **Principle VIII - Transparent Updates**: Tests MUST validate that update command shows changelog and preserves user customizations without changing AI behavior unexpectedly.

✅ **Principle IX - Methodological Neutrality**: Not directly applicable to testing (N/A)

✅ **Issue-Driven Development**: This feature has granular issue [to be created] describing need for integration test coverage.

### Constitution Compliance: ✅ PASS

All relevant principles are addressed by test scenarios. No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-e2e-tests/
├── plan.md              # This file
├── research.md          # Phase 0 output (COMPLETE)
├── data-model.md        # Not applicable (testing infrastructure)
├── quickstart.md        # Phase 1 output (NEXT)
├── contracts/           # Not applicable (no API contracts)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
tests/
├── unit/                      # Existing unit tests (90+ tests)
│   ├── conftest.py           # Shared fixtures
│   ├── test_cli_setup.py     # Existing
│   ├── test_cli_status.py    # Existing
│   └── ...
│
├── integration/               # EXPAND: Add comprehensive integration tests
│   ├── conftest.py           # NEW: Integration test fixtures
│   ├── test_setup_complete.py     # NEW: Full setup flow
│   ├── test_update_flow.py        # NEW: Update preserves customizations
│   ├── test_status_diagnostics.py # NEW: Status health checks
│   ├── test_doctor_repairs.py     # NEW: Doctor command
│   ├── test_move_journal.py       # NEW: Journal relocation
│   └── fixtures/             # NEW: Test data factories
│       ├── journal_factory.py
│       └── config_factory.py
│
└── e2e/                       # NEW: True end-to-end tests
    ├── conftest.py           # E2E fixtures
    ├── test_fresh_install.py      # NEW: Complete install scenario
    ├── test_upgrade_workflow.py   # NEW: Update existing installation
    ├── test_cross_platform.py     # NEW: Platform-specific features
    └── test_user_workflows.py     # NEW: Real user scenarios

tasks.py                       # EXTEND: Add test-integration, test-e2e targets
.github/workflows/ci.yml       # EXTEND: Add integration/e2e test stages
```

**Structure Decision**: Single project with expanded test infrastructure. Tests organized by scope (unit → integration → e2e) with shared fixtures in `conftest.py` files at appropriate levels.

## Complexity Tracking

**No violations** - this feature aligns with all constitution principles and adds testing infrastructure without introducing complexity.

---

## Phase 0: Research ✅ COMPLETE

See [research.md](./research.md) for detailed technical decisions and rationale.

**Key Decisions Made**:
- Test framework: pytest + pytest-bdd
- CLI testing: Click CliRunner + subprocess
- Test isolation: pytest tmp_path fixtures
- Cross-platform: GitHub Actions matrix
- Mocking: Minimal - prefer real file I/O
- Organization: tests/integration/ + tests/e2e/
- CI/CD: Extend invoke tasks
- Parallelization: pytest-xdist

---

## Phase 1: Design & Contracts

### Data Model

**Not applicable** - This feature is testing infrastructure and doesn't introduce new domain entities. Tests validate existing entities (Config, Journal structure, IDE configs).

### API Contracts

**Not applicable** - This feature tests CLI commands, not APIs. Test assertions serve as "contracts" for expected behavior.

### Quickstart Guide

See [quickstart.md](./quickstart.md) - Developer guide for running and writing integration/e2e tests.

---

## Phase 2: Task Breakdown

**Status**: Not started - run `/speckit.tasks` to generate granular implementation tasks.

**Expected Task Categories**:
1. Setup integration test fixtures and factories
2. Implement setup command integration tests
3. Implement update command integration tests
4. Implement status/doctor command tests
5. Implement move command tests
6. Add e2e test scenarios
7. Extend invoke tasks for test execution
8. Update CI/CD pipeline
9. Add testing documentation

**Estimated Tasks**: 30-40 granular tasks

---

## Constitution Re-Check (Post-Design)

✅ **PASS** - No design decisions violate constitution principles. Testing infrastructure enhances system quality without compromising core values.

**Verification**:
- ✅ Tests validate modular architecture (Principle I)
- ✅ Tests cover all supported editors (Principle II)
- ✅ Tests verify flexible journal locations (Principle III)
- ✅ Tests ensure user customization preservation (Principle VII)
- ✅ Tests validate transparent updates (Principle VIII)

---

## Next Steps

1. ✅ Phase 0 complete - Research decisions documented
2. ⏭️ Phase 1 complete - Generate quickstart.md
3. ⏭️ Update agent context with testing decisions
4. 🔜 Phase 2 - Run `/speckit.tasks` to generate implementation tasks
5. 🔜 Phase 3 - Run `/speckit.implement` to execute tasks

**Ready for**: `/speckit.tasks` command to generate granular task breakdown.
