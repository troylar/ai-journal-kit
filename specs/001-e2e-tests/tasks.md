# Tasks: Integration & E2E Test Suite

**Input**: Design documents from `/specs/001-e2e-tests/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, quickstart.md ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETE

**Purpose**: Project initialization and test infrastructure setup

- [X] T001 Create tests/integration/conftest.py with shared integration test fixtures
- [X] T002 Create tests/e2e/conftest.py with shared e2e test fixtures
- [X] T003 [P] Add journal_factory fixture to tests/integration/fixtures/journal_factory.py
- [X] T004 [P] Add config_factory fixture to tests/integration/fixtures/config_factory.py
- [X] T005 Add pytest-bdd to project dependencies in pyproject.toml
- [X] T006 [P] Create helper functions for journal validation in tests/integration/helpers.py

---

## Phase 2: Foundational (Blocking Prerequisites) ✅ COMPLETE

**Purpose**: Core test utilities that MUST be complete before user story tests can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create assert_journal_structure_valid() helper in tests/integration/helpers.py
- [X] T008 [P] Create assert_ide_config_installed() helper in tests/integration/helpers.py
- [X] T009 [P] Create assert_config_valid() helper in tests/integration/helpers.py
- [X] T010 Add invoke test-integration task to tasks.py
- [X] T011 [P] Add invoke test-e2e task to tasks.py
- [X] T012 [P] Add invoke test-all task to tasks.py

**Checkpoint**: ✅ Foundation ready - user story tests can now be implemented in parallel

---

## Phase 3: User Story 1 - Complete Setup Flow Validation (Priority: P1) 🎯 MVP

**Goal**: Comprehensive integration tests for the setup command covering all acceptance scenarios

**Independent Test**: Run `pytest tests/integration/test_setup_complete.py -v` to verify all setup scenarios work correctly

**Test Coverage for Acceptance Scenarios**:
1. Setup with default options creates complete journal
2. Setup with Cursor IDE installs correct configs
3. Setup with custom path works at any location
4. Setup prevents duplicate installation
5. Setup handles deleted journal gracefully

### Implementation Tasks

- [ ] T013 [US1] Create tests/integration/test_setup_complete.py skeleton
- [ ] T014 [P] [US1] Add test_setup_creates_all_folders() in tests/integration/test_setup_complete.py
- [ ] T015 [P] [US1] Add test_setup_creates_all_templates() in tests/integration/test_setup_complete.py
- [ ] T016 [P] [US1] Add test_setup_creates_config_file() in tests/integration/test_setup_complete.py
- [ ] T017 [P] [US1] Add test_setup_installs_cursor_config() in tests/integration/test_setup_complete.py
- [ ] T018 [P] [US1] Add test_setup_installs_windsurf_config() in tests/integration/test_setup_complete.py
- [ ] T019 [P] [US1] Add test_setup_installs_claude_config() in tests/integration/test_setup_complete.py
- [ ] T020 [P] [US1] Add test_setup_installs_copilot_config() in tests/integration/test_setup_complete.py
- [ ] T021 [P] [US1] Add test_setup_installs_all_configs() in tests/integration/test_setup_complete.py
- [ ] T022 [P] [US1] Add test_setup_with_custom_path() in tests/integration/test_setup_complete.py
- [ ] T023 [P] [US1] Add test_setup_prevents_duplicate_installation() in tests/integration/test_setup_complete.py
- [ ] T024 [P] [US1] Add test_setup_handles_deleted_journal() in tests/integration/test_setup_complete.py
- [ ] T025 [P] [US1] Add test_setup_creates_parent_directory() in tests/integration/test_setup_complete.py
- [ ] T026 [P] [US1] Add test_setup_dry_run_mode() in tests/integration/test_setup_complete.py
- [ ] T027 [P] [US1] Add test_setup_handles_cancellation() in tests/integration/test_setup_complete.py

### E2E Tests

- [ ] T028 [US1] Create tests/e2e/test_fresh_install.py skeleton
- [ ] T029 [P] [US1] Add test_e2e_fresh_install_cursor() in tests/e2e/test_fresh_install.py
- [ ] T030 [P] [US1] Add test_e2e_fresh_install_all_ides() in tests/e2e/test_fresh_install.py
- [ ] T031 [P] [US1] Add test_e2e_setup_with_cloud_path() in tests/e2e/test_fresh_install.py

---

## Phase 4: User Story 2 - Update Command Validation (Priority: P2)

**Goal**: Comprehensive integration tests for update command ensuring customization preservation

**Independent Test**: Run `pytest tests/integration/test_update_flow.py -v` to verify all update scenarios preserve user data

**Test Coverage for Acceptance Scenarios**:
1. Update refreshes core templates without touching custom ones
2. Update adds new IDE configs without breaking existing structure
3. Update preserves custom .ai-instructions/ files
4. Update migrates old template structure safely

### Implementation Tasks

- [ ] T032 [US2] Create tests/integration/test_update_flow.py skeleton
- [ ] T033 [P] [US2] Add test_update_preserves_custom_templates() in tests/integration/test_update_flow.py
- [ ] T034 [P] [US2] Add test_update_preserves_ai_instructions() in tests/integration/test_update_flow.py
- [ ] T035 [P] [US2] Add test_update_preserves_journal_entries() in tests/integration/test_update_flow.py
- [ ] T036 [P] [US2] Add test_update_refreshes_core_templates() in tests/integration/test_update_flow.py
- [ ] T037 [P] [US2] Add test_update_adds_new_ide_configs() in tests/integration/test_update_flow.py
- [ ] T038 [P] [US2] Add test_update_migrates_old_structure() in tests/integration/test_update_flow.py
- [ ] T039 [P] [US2] Add test_update_dry_run_mode() in tests/integration/test_update_flow.py
- [ ] T040 [P] [US2] Add test_update_handles_corrupted_config() in tests/integration/test_update_flow.py
- [ ] T041 [P] [US2] Add test_update_with_force_flag() in tests/integration/test_update_flow.py

### E2E Tests

- [ ] T042 [US2] Create tests/e2e/test_upgrade_workflow.py skeleton
- [ ] T043 [P] [US2] Add test_e2e_upgrade_preserves_everything() in tests/e2e/test_upgrade_workflow.py
- [ ] T044 [P] [US2] Add test_e2e_upgrade_multiple_versions() in tests/e2e/test_upgrade_workflow.py

---

## Phase 5: User Story 3 - Status & Doctor Commands Validation (Priority: P3)

**Goal**: Integration tests for diagnostic commands (status and doctor)

**Independent Test**: Run `pytest tests/integration/test_status_diagnostics.py tests/integration/test_doctor_repairs.py -v` to verify diagnostic commands work correctly

**Test Coverage for Acceptance Scenarios**:
1. Status command shows all health checks for healthy journal
2. Status command detects missing folders
3. Doctor command detects and suggests repairs for issues
4. Multiple IDE configs are validated correctly

### Implementation Tasks - Status Command

- [ ] T045 [US3] Create tests/integration/test_status_diagnostics.py skeleton
- [ ] T046 [P] [US3] Add test_status_healthy_journal() in tests/integration/test_status_diagnostics.py
- [ ] T047 [P] [US3] Add test_status_missing_folders() in tests/integration/test_status_diagnostics.py
- [ ] T048 [P] [US3] Add test_status_missing_ide_configs() in tests/integration/test_status_diagnostics.py
- [ ] T049 [P] [US3] Add test_status_corrupted_config() in tests/integration/test_status_diagnostics.py
- [ ] T050 [P] [US3] Add test_status_json_output() in tests/integration/test_status_diagnostics.py
- [ ] T051 [P] [US3] Add test_status_verbose_mode() in tests/integration/test_status_diagnostics.py

### Implementation Tasks - Doctor Command

- [ ] T052 [US3] Create tests/integration/test_doctor_repairs.py skeleton
- [ ] T053 [P] [US3] Add test_doctor_detects_missing_folders() in tests/integration/test_doctor_repairs.py
- [ ] T054 [P] [US3] Add test_doctor_detects_corrupted_config() in tests/integration/test_doctor_repairs.py
- [ ] T055 [P] [US3] Add test_doctor_suggests_repairs() in tests/integration/test_doctor_repairs.py
- [ ] T056 [P] [US3] Add test_doctor_repairs_structure() in tests/integration/test_doctor_repairs.py

---

## Phase 6: User Story 4 - Move Command Validation (Priority: P3)

**Goal**: Integration tests for move command ensuring safe journal relocation

**Independent Test**: Run `pytest tests/integration/test_move_journal.py -v` to verify move operations preserve data integrity

**Test Coverage for Acceptance Scenarios**:
1. Move relocates all files and updates config
2. Move updates symlink targets
3. Move preserves IDE configs at new location
4. Move can be cancelled safely

### Implementation Tasks

- [ ] T057 [US4] Create tests/integration/test_move_journal.py skeleton
- [ ] T058 [P] [US4] Add test_move_relocates_all_files() in tests/integration/test_move_journal.py
- [ ] T059 [P] [US4] Add test_move_updates_config() in tests/integration/test_move_journal.py
- [ ] T060 [P] [US4] Add test_move_preserves_ide_configs() in tests/integration/test_move_journal.py
- [ ] T061 [P] [US4] Add test_move_updates_symlinks() in tests/integration/test_move_journal.py
- [ ] T062 [P] [US4] Add test_move_dry_run_mode() in tests/integration/test_move_journal.py
- [ ] T063 [P] [US4] Add test_move_handles_cancellation() in tests/integration/test_move_journal.py
- [ ] T064 [P] [US4] Add test_move_to_cloud_drive() in tests/integration/test_move_journal.py

---

## Phase 7: Cross-Platform & Edge Cases

**Goal**: Validate platform-specific behavior and edge cases

- [ ] T065 Create tests/e2e/test_cross_platform.py skeleton
- [ ] T066 [P] Add test_setup_on_windows() in tests/e2e/test_cross_platform.py (Windows only)
- [ ] T067 [P] Add test_setup_on_macos() in tests/e2e/test_cross_platform.py (macOS only)
- [ ] T068 [P] Add test_setup_on_linux() in tests/e2e/test_cross_platform.py (Linux only)
- [ ] T069 [P] Add test_junction_creation_windows() in tests/e2e/test_cross_platform.py (Windows only)
- [ ] T070 [P] Add test_symlink_creation_unix() in tests/e2e/test_cross_platform.py (Unix only)
- [ ] T071 [P] Add test_unicode_paths() in tests/e2e/test_cross_platform.py
- [ ] T072 [P] Add test_special_characters_in_path() in tests/e2e/test_cross_platform.py
- [ ] T073 [P] Add test_insufficient_disk_space() in tests/e2e/test_cross_platform.py
- [ ] T074 [P] Add test_write_protected_directory() in tests/e2e/test_cross_platform.py

---

## Phase 8: CI/CD Integration

**Goal**: Integrate new tests into CI/CD pipeline

- [ ] T075 Update .github/workflows/ci.yml to add integration test stage
- [ ] T076 Update .github/workflows/ci.yml to add e2e test stage
- [ ] T077 Update tasks.py with test-integration invoke task
- [ ] T078 Update tasks.py with test-e2e invoke task
- [ ] T079 Update tasks.py with test-all invoke task
- [ ] T080 Update invoke ci task to include integration and e2e tests
- [ ] T081 Add pytest-bdd to CI/CD requirements
- [ ] T082 Configure pytest-xdist for parallel execution in CI

---

## Phase 9: Documentation & Polish

**Goal**: Document new testing infrastructure for contributors

- [ ] T083 Create TESTING.md guide in docs/ directory
- [ ] T084 Update README.md to mention comprehensive test coverage
- [ ] T085 Add integration test examples to CONTRIBUTING.md (if exists)
- [ ] T086 [P] Update pytest.ini with new test markers (integration, e2e, platform-specific)
- [ ] T087 [P] Add test coverage badge to README.md for integration tests
- [ ] T088 Verify all tests pass on all platforms (run full CI)

---

## Dependencies & Execution Strategy

### Story Dependency Graph

```
Setup (Phase 1) & Foundational (Phase 2)
            ↓
    ┌───────┼───────┬───────┐
    ↓       ↓       ↓       ↓
   US1     US2     US3     US4  ← Can execute in parallel
   (P1)    (P2)    (P3)    (P3)
```

**Independent User Stories**: US1, US2, US3, and US4 can all be developed and tested independently after foundational setup is complete.

### Parallel Execution Opportunities

**Within Each User Story** (highly parallelizable):

- **US1 (Setup Tests)**: T014-T027 can run in parallel (15 tasks, ~1-2 hours)
- **US2 (Update Tests)**: T033-T041 can run in parallel (9 tasks, ~1 hour)
- **US3 (Status/Doctor Tests)**: T046-T056 can run in parallel (11 tasks, ~1 hour)
- **US4 (Move Tests)**: T058-T064 can run in parallel (7 tasks, ~30 min)
- **Cross-Platform**: T066-T074 can run in parallel (9 tasks, ~1 hour)

**Total Parallel Work**: ~50 tasks across 4 stories = significant time savings

### MVP Scope (Minimum Viable Product)

**Recommended MVP**: Phase 1 + Phase 2 + Phase 3 (US1 only)

**Rationale**: US1 (Setup Flow Validation) is P1 and delivers immediate value by catching setup regressions. This represents ~31 tasks and provides:
- Complete setup command test coverage
- E2E validation of fresh installation
- Foundation for additional stories

**MVP Tasks**: T001-T031 (31 tasks)

---

## Implementation Strategy

### Recommended Approach

1. **Complete Phases 1-2 first** (T001-T012): 12 tasks, ~2-3 hours
   - Sets up all test infrastructure
   - Enables parallel story implementation

2. **Implement US1 (P1) for MVP** (T013-T031): 19 tasks, ~3-4 hours
   - Most critical user story
   - Deliverable increment
   - Independent test ready

3. **Add remaining stories in parallel** (T032-T074): 43 tasks, ~5-6 hours
   - US2, US3, US4 can be developed concurrently
   - Each story independently testable

4. **Finalize with CI/CD & docs** (T075-T088): 14 tasks, ~2 hours

**Total Estimated Effort**: ~12-15 hours for complete implementation

### Verification Steps

After each phase:
1. Run `pytest tests/integration/test_[module].py -v` to verify story tests pass
2. Run `invoke ci` to ensure no regressions
3. Check coverage: `pytest --cov=ai_journal_kit --cov-report=term-missing`
4. Commit with descriptive message referencing user story

---

## Task Summary

**Total Tasks**: 88 tasks

**By Phase**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundation): 6 tasks
- Phase 3 (US1 - P1): 19 tasks 🎯
- Phase 4 (US2 - P2): 13 tasks
- Phase 5 (US3 - P3): 12 tasks
- Phase 6 (US4 - P3): 8 tasks
- Phase 7 (Cross-Platform): 10 tasks
- Phase 8 (CI/CD): 8 tasks
- Phase 9 (Documentation): 6 tasks

**Parallelizable Tasks**: 62 tasks marked with [P] (70%)

**By User Story**:
- US1 (Setup): 19 tasks (P1) 🎯 MVP
- US2 (Update): 13 tasks (P2)
- US3 (Status/Doctor): 12 tasks (P3)
- US4 (Move): 8 tasks (P3)
- Infrastructure: 36 tasks (setup, foundation, cross-platform, CI/CD, docs)

---

## Expected Coverage Impact

**Current**: 29% (91 tests, mostly unit)

**After Implementation**: 40-50% coverage
- +40-50 integration tests
- +10-15 e2e tests
- Total: 140-155 tests (+54-70% growth)

**Coverage Breakdown** (estimated):
- CLI commands: 0% → 60%+ (setup, update, status, doctor, move)
- Core modules: 90% → 95%+ (already excellent)
- Overall: 29% → 45%+ target

---

## Next Steps

**Ready for implementation**: Run `/speckit.implement` to begin systematic task execution.

**Suggested approach**:
1. Start with MVP scope (T001-T031) for quick value
2. Expand to remaining stories incrementally
3. Leverage parallelization for faster completion

**Each task is granular and executable** - ready for LLM-assisted implementation! 🚀

