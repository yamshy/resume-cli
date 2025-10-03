# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure, constitution compliance notes
2. Load optional design documents:
   → data-model.md: Extract entities & required provenance → model tasks
   → contracts/: Each file → contract test task (ensure offline datasets)
   → research.md: Extract decisions → setup tasks, confirm agent workflows
   → agent prompt catalog: Derive tasks to version prompts and guardrails
   → commit policy docs: Identify Conventional Commit enforcement tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests, provenance enforcement tests
   → Core: models, services, CLI commands with strict Pydantic schemas
   → Integration: deterministic pipelines, agent orchestration glue
   → Polish: performance benchmark verification, offline docs, ATS validation, Conventional Commit verification
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
   → Validate offline execution, provenance, agent prompt updates, and Conventional Commit enforcement before feature completion
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
   → All agent workflows documented and versioned?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools (`ruff`, `mypy`, `pytest`, typst lint, Conventional Commit hook)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T004 [P] Contract test resume build flow in tests/contract/test_resume_cli.py (offline fixtures only)
- [ ] T005 [P] Provenance validation test ensuring every bullet includes `source_id`
- [ ] T006 [P] Integration test CLI end-to-end run completes ≤60 seconds (1 minute) using reference data
- [ ] T007 [P] Agent prompt contract tests verifying expected outputs recorded in agent catalog

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T008 [P] Resume models with strict Pydantic schemas in src/models/resume.py
- [ ] T009 [P] Agent orchestration service in src/services/agent_orchestrator.py
- [ ] T010 [P] CLI `resumecli build` command orchestrating agent workflows
- [ ] T011 Deterministic Typst render pipeline preserving ATS-safe content
- [ ] T012 Provenance enforcement pipeline rejecting missing `source_id`
- [ ] T013 Privacy-safe local storage for evidence artifacts
- [ ] T014 Structured error handling with script-friendly output

## Phase 3.4: Integration
- [ ] T015 Offline data source synchronization scripts using versioned fixtures
- [ ] T016 Agent prompt catalog versioning and provenance link updates
- [ ] T017 Performance profiling scripts ensuring ≤60 seconds (1 minute) execution
- [ ] T018 Privacy review checklist updates stored locally

## Phase 3.5: Polish
- [ ] T019 [P] Unit tests for Pydantic schema validation in tests/unit/test_schema.py
- [ ] T020 Performance regression test verifying ≤60 seconds (1 minute) end-to-end
- [ ] T021 [P] Update offline docs & CLI help to reflect feature
- [ ] T022 Remove duplication and confirm determinism in outputs
- [ ] T023 Run manual-testing.md with offline checklist and privacy verification

## Dependencies
- Tests (T004-T007) before implementation (T008-T014)
- T008 blocks T009, T015
- T016 blocks T018
- Implementation before polish (T019-T023)

## Parallel Example
```
# Launch T004-T007 together:
Task: "Contract test resume build flow in tests/contract/test_resume_cli.py"
Task: "Provenance validation test ensuring every bullet includes source_id"
Task: "Integration test CLI end-to-end run completes ≤60 seconds (1 minute)"
Task: "Agent prompt contract tests verifying expected outputs"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task