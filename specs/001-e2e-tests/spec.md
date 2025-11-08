# Feature Specification: Integration & End-to-End Test Suite

**Feature Branch**: `001-e2e-tests`  
**Created**: 2025-01-08  
**Status**: Draft  
**Input**: User description: "Add integration/e2e tests"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete Setup Flow Validation (Priority: P1)

**As a** quality engineer  
**I want** comprehensive end-to-end tests for the setup command  
**So that** users can confidently install and configure ai-journal-kit without errors

**Why this priority**: Setup is the first user experience and critical for adoption. Failed setups lead to immediate abandonment.

**Independent Test**: Can be fully tested by running `ai-journal-kit setup` with various configurations and verifying the journal structure, IDE configs, and config file are created correctly. Delivers immediate value by catching setup regressions.

**Acceptance Scenarios**:

1. **Given** no existing journal configuration, **When** user runs setup with default options, **Then** journal folder is created with all required subdirectories and templates
2. **Given** no existing journal configuration, **When** user runs setup selecting Cursor IDE, **Then** `.cursor/rules/` directory is created with all coaching instruction files
3. **Given** no existing journal configuration, **When** user runs setup with custom path, **Then** journal is created at specified location with correct configuration
4. **Given** existing journal configuration, **When** user attempts setup again, **Then** system warns about existing setup and prevents data loss
5. **Given** journal was manually deleted, **When** user runs setup, **Then** system detects missing journal and allows recreation

---

### User Story 2 - Update Command Validation (Priority: P2)

**As a** quality engineer  
**I want** end-to-end tests for the update command  
**So that** users can safely upgrade their journal without losing customizations

**Why this priority**: Updates are critical for maintenance but less frequent than setup. Template update safety is essential to preserve user data.

**Independent Test**: Can be tested by creating a configured journal, customizing templates, running update, and verifying core files are updated while customizations are preserved. Delivers value by preventing update-related data loss.

**Acceptance Scenarios**:

1. **Given** an existing journal installation, **When** user runs update command, **Then** core templates are refreshed while custom templates remain untouched
2. **Given** an outdated journal version, **When** user runs update, **Then** new IDE config files are added without breaking existing structure
3. **Given** user has custom AI instructions, **When** update is performed, **Then** custom instructions in `.ai-instructions/` are preserved
4. **Given** a journal with old template structure, **When** update runs, **Then** templates are migrated to new structure with user content intact

---

### User Story 3 - Status & Doctor Commands Validation (Priority: P3)

**As a** quality engineer  
**I want** end-to-end tests for status and doctor commands  
**So that** users can diagnose and verify their journal health

**Why this priority**: Diagnostic commands are helpful but not critical path. They provide support value but don't block core functionality.

**Independent Test**: Can be tested by creating journals in various states (healthy, corrupted, missing files) and verifying command output matches expected diagnostics. Delivers value by ensuring troubleshooting tools work correctly.

**Acceptance Scenarios**:

1. **Given** a healthy journal installation, **When** user runs status command, **Then** all health checks pass and configuration details are displayed
2. **Given** a journal with missing folders, **When** user runs status, **Then** missing components are identified with remediation suggestions
3. **Given** a journal with corrupted config, **When** user runs doctor command, **Then** issues are detected and repair options are offered
4. **Given** multiple IDE configurations installed, **When** status is checked, **Then** all IDE configs are validated and reported

---

### User Story 4 - Move Command Validation (Priority: P3)

**As a** quality engineer  
**I want** end-to-end tests for the move command  
**So that** users can safely relocate their journal without data loss

**Why this priority**: Move operations are infrequent but high-risk. Testing ensures data integrity during relocation.

**Independent Test**: Can be tested by creating a journal, adding content, moving it to a new location, and verifying all files and configurations are updated correctly. Delivers value by preventing data loss during relocation.

**Acceptance Scenarios**:

1. **Given** an existing journal at original location, **When** user runs move to new path, **Then** all journal files are relocated and config is updated
2. **Given** a journal with symlinks, **When** move is performed, **Then** symlink targets are updated to new location
3. **Given** IDE-specific configuration files, **When** journal is moved, **Then** IDE configs remain functional at new location
4. **Given** user cancels move operation mid-process, **When** cancellation occurs, **Then** original journal state is preserved

---

### Edge Cases

- What happens when user runs setup with insufficient disk space?
- How does system handle concurrent command executions (e.g., update while setup is running)?
- What occurs when journal path contains special characters or Unicode names?
- How does system behave when IDE config directory is write-protected?
- What happens when config file is manually edited with invalid JSON?
- How does system handle journal folders that are git repositories?
- What occurs when moving journal to a network drive or cloud sync folder?
- How does system behave on different platforms (Windows vs macOS vs Linux)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Test suite MUST validate complete setup flow including journal creation, template installation, IDE configuration, and config file generation
- **FR-002**: Test suite MUST verify all CLI commands (setup, update, status, doctor, move) execute successfully with valid inputs
- **FR-003**: Test suite MUST validate error handling for invalid inputs, missing dependencies, and permission issues
- **FR-004**: Test suite MUST verify data preservation during update operations (custom templates, user configurations, journal entries)
- **FR-005**: Test suite MUST test cross-platform compatibility (Windows, macOS, Linux) for all core commands
- **FR-006**: Test suite MUST validate symlink/junction creation and management on different platforms
- **FR-007**: Test suite MUST verify IDE configuration installation for all supported editors (Cursor, Windsurf, Claude Code, GitHub Copilot, All)
- **FR-008**: Test suite MUST test journal folder structure creation with all required subdirectories (daily, projects, areas, resources, people, memories, archive)
- **FR-009**: Test suite MUST validate config file operations (create, read, update) with proper error handling
- **FR-010**: Test suite MUST test template update scenarios including backup creation and rollback capabilities
- **FR-011**: Test suite MUST verify status command health checks including folder structure validation and IDE config detection
- **FR-012**: Test suite MUST validate doctor command diagnostics and repair recommendations
- **FR-013**: Test suite MUST test move command including file relocation, config updates, and symlink adjustments
- **FR-014**: Test suite MUST verify dry-run modes for destructive operations (setup, update, move)
- **FR-015**: Test suite MUST test user confirmation prompts and cancellation flows

### Key Entities

- **Test Fixture**: Temporary journal installations created for testing, including journal directory, config files, and IDE configurations
- **Test Scenario**: Individual test case covering specific command execution with expected inputs and outputs
- **Test Assertion**: Validation check verifying expected system state after command execution
- **Test Environment**: Isolated file system location for each test to prevent interference between tests
- **Platform Context**: Operating system and environment variables affecting test execution

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Test suite achieves 80%+ coverage of integration scenarios for all CLI commands
- **SC-002**: All end-to-end tests execute successfully on Windows, macOS, and Linux platforms
- **SC-003**: Test suite identifies regressions within 5 minutes of test execution
- **SC-004**: 100% of critical user flows (setup, update, status) have comprehensive e2e test coverage
- **SC-005**: Test suite validates data integrity for all file operations with zero false positives
- **SC-006**: End-to-end tests execute in under 10 minutes for full suite on CI/CD pipeline
- **SC-007**: Test failures provide actionable error messages identifying specific command and scenario that failed
- **SC-008**: Test suite can be run locally by developers with single command for rapid feedback
