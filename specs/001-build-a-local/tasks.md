# Tasks: Local-first Resume Tailoring CLI

**Input**: `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/plan.md`, `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/research.md`, `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/data-model.md`, `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/contracts/`, `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/quickstart.md`, `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/spec.md`

**Prerequisites**: Python 3.13 via `uv`, Typst CLI, Ollama models per quickstart, offline environment enforced

## Phase 3.1: Setup
- [ ] T001 Update `/var/home/shyam/projects/resume-cli/pyproject.toml` to pin Python 3.13 with `uv` and declare core dependencies (`typer`, `pydantic`, `fastembed`, `outlines`, `sqlite-utils`, `typst`, test tool extras).
- [ ] T002 Configure tooling blocks in `/var/home/shyam/projects/resume-cli/pyproject.toml` for `ruff`, `mypy`, `pytest`, and `uv` scripts enforcing the offline governance gates.
- [ ] T003 Create package scaffolding under `/var/home/shyam/projects/resume-cli/src/resumecli/` (cli/, data/, models/, services/, templates/) with guarding `__init__.py` files and sample-data placeholders aligned to `quickstart.md`.

## Phase 3.2: Tests First (TDD)
- [ ] T004 [P] Author failing contract test at `/var/home/shyam/projects/resume-cli/tests/contract/test_build_contract.py` validating `resumecli build` offline artifact generation per `contracts/cli/build.contract.md`.
- [ ] T005 [P] Author failing contract test at `/var/home/shyam/projects/resume-cli/tests/contract/test_facts_contract.py` covering list/confirm/doctor flows per `contracts/cli/facts.contract.md`.
- [ ] T006 [P] Author failing contract test at `/var/home/shyam/projects/resume-cli/tests/contract/test_templates_contract.py` exercising list/show/render expectations per `contracts/cli/templates.contract.md`.
- [ ] T007 [P] Author failing contract test at `/var/home/shyam/projects/resume-cli/tests/contract/test_doctor_contract.py` asserting diagnostics, exit codes, and JSON output per `contracts/cli/doctor.contract.md`.
- [ ] T008 [P] Add prompt contract test at `/var/home/shyam/projects/resume-cli/tests/contract/test_jobreq_extractor_prompt.py` to lock schema adherence for `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/contracts/agents/jobreq_extractor.prompt.md`.
- [ ] T009 [P] Add prompt contract test at `/var/home/shyam/projects/resume-cli/tests/contract/test_bullet_composer_prompt.py` verifying provenance rules for `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/contracts/agents/bullet_composer.prompt.md`.
- [ ] T010 [P] Add prompt contract test at `/var/home/shyam/projects/resume-cli/tests/contract/test_validation_reviewer_prompt.py` enforcing guardrails from `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/contracts/agents/validation_reviewer.prompt.md`.
- [ ] T011 [P] Create integration test at `/var/home/shyam/projects/resume-cli/tests/integration/test_cli_build_quickstart.py` covering quickstart Step 5 offline build flow and 60-second budget.
- [ ] T012 [P] Create integration test at `/var/home/shyam/projects/resume-cli/tests/integration/test_cli_coverage_linking.py` asserting bullets cite facts/requirements per acceptance scenario 2.
- [ ] T013 [P] Create integration test at `/var/home/shyam/projects/resume-cli/tests/integration/test_cli_doctor_quickstart.py` mirroring quickstart Step 4 diagnostics expectations.
- [ ] T014 [P] Add model validation tests at `/var/home/shyam/projects/resume-cli/tests/unit/models/test_job_posting_jobreq.py` for `JobPosting` and `JobReq` constraints from `data-model.md`.
- [ ] T015 [P] Add model validation tests at `/var/home/shyam/projects/resume-cli/tests/unit/models/test_fact_and_bullet.py` for `CuratedFact`, embedded `Metric`/`DocumentRef`, and `ResumeBullet` rules.
- [ ] T016 [P] Add model validation tests at `/var/home/shyam/projects/resume-cli/tests/unit/models/test_coverage_tracking.py` for `CoverageEntry`, `EmbeddingCacheEntry`, and `RunLog` behaviors.

## Phase 3.3: Core Implementation
- [ ] T017 [P] Implement `JobPosting` Pydantic model in `/var/home/shyam/projects/resume-cli/src/resumecli/models/job_posting.py` with provenance validators.
- [ ] T018 [P] Implement `JobReq` Pydantic model in `/var/home/shyam/projects/resume-cli/src/resumecli/models/jobreq.py` with span and confidence logic.
- [ ] T019 [P] Implement `CuratedFact` model plus `Metric` and `DocumentRef` classes in `/var/home/shyam/projects/resume-cli/src/resumecli/models/fact.py` with freshness constraints.
- [ ] T020 [P] Implement `ResumeBullet` model in `/var/home/shyam/projects/resume-cli/src/resumecli/models/bullet.py` enforcing ATS-safe content and provenance hashes.
- [ ] T021 [P] Implement `CoverageEntry` model in `/var/home/shyam/projects/resume-cli/src/resumecli/models/coverage.py` ensuring gap rationales and linkage checks.
- [ ] T022 [P] Implement `EmbeddingCacheEntry` model in `/var/home/shyam/projects/resume-cli/src/resumecli/models/embedding_cache.py` with vector length validation.
- [ ] T023 [P] Implement `RunLog` model in `/var/home/shyam/projects/resume-cli/src/resumecli/models/run_log.py` computing durations and warnings capture.
- [ ] T024 [P] Build ingestion and extraction pipelines across `/var/home/shyam/projects/resume-cli/src/resumecli/data/ingestion.py` and `/var/home/shyam/projects/resume-cli/src/resumecli/data/extraction.py`, wiring sanitization and JobReq agent calls.
- [ ] T025 [P] Implement hybrid retrieval in `/var/home/shyam/projects/resume-cli/src/resumecli/data/retrieval.py` blending SQLite FTS5 with embedding scoring.
- [ ] T026 [P] Implement composition and validation stages across `/var/home/shyam/projects/resume-cli/src/resumecli/data/composition.py` and `/var/home/shyam/projects/resume-cli/src/resumecli/data/validation.py`, integrating bullet composer and reviewer agents.
- [ ] T027 [P] Implement Typst rendering stage in `/var/home/shyam/projects/resume-cli/src/resumecli/data/rendering.py` producing PDF and assets offline.
- [ ] T028 [P] Implement embeddings service in `/var/home/shyam/projects/resume-cli/src/resumecli/services/embeddings.py` with caching strategy for fastembed.
- [ ] T029 [P] Implement storage service in `/var/home/shyam/projects/resume-cli/src/resumecli/services/storage.py` managing SQLite connections, migrations, and FTS indices.
- [ ] T030 [P] Implement logging service in `/var/home/shyam/projects/resume-cli/src/resumecli/services/logging.py` emitting structured stage timings.
- [ ] T031 Implement Typer app entrypoint in `/var/home/shyam/projects/resume-cli/src/resumecli/cli/main.py` registering subcommands and global options.
- [ ] T032 [P] Implement `build` command orchestration in `/var/home/shyam/projects/resume-cli/src/resumecli/cli/build.py` aligning with contract outputs.
- [ ] T033 [P] Implement `facts` command workflows in `/var/home/shyam/projects/resume-cli/src/resumecli/cli/facts.py` for list/confirm/doctor subcommands.
- [ ] T034 [P] Implement `templates` command workflows in `/var/home/shyam/projects/resume-cli/src/resumecli/cli/templates.py` handling metadata and rendering.
- [ ] T035 [P] Implement `doctor` command diagnostics in `/var/home/shyam/projects/resume-cli/src/resumecli/cli/doctor.py` covering env, performance, and schema checks.

## Phase 3.4: Integration
- [ ] T036 Compose build pipeline orchestrator with logging and coverage export in `/var/home/shyam/projects/resume-cli/src/resumecli/pipeline/build_runner.py`, invoking services/data stages and producing `coverage.json` plus `run.json`.

## Phase 3.5: Polish
- [ ] T037 [P] Add performance regression test at `/var/home/shyam/projects/resume-cli/tests/performance/test_build_runtime.py` asserting end-to-end runtime ≤ 60 seconds using sample data.
- [ ] T038 [P] Update documentation in `/var/home/shyam/projects/resume-cli/README.md` and `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/quickstart.md` to reflect finalized offline workflows, coverage review steps, and Conventional Commit reminders.

## Dependencies
- T004–T016 depend on T001–T003 for project scaffolding.
- T017 depends on T014; T018 depends on T014; T019 and T020 depend on T015; T021, T022, and T023 depend on T016.
- T024 depends on T011, T014, and T018; T025 depends on T011, T015, and T019; T026 depends on T012, T015, and T020; T027 depends on T011 and T026.
- T028 depends on T025; T029 depends on T025 and T022; T030 depends on T011, T023, and T029.
- T031 depends on T004–T010 and T024–T030; T032 depends on T011, T024–T030; T033 depends on T005, T015, and T029; T034 depends on T006, T027, and T029; T035 depends on T007, T029, T030.
- T036 depends on T031–T035.
- T037 depends on T032 and T036; T038 depends on T032–T035 and T037.

## Parallel Execution Examples
- Run contract tests together once setup is complete:
  - `cursor-task run --id T004`
  - `cursor-task run --id T005`
  - `cursor-task run --id T006`
  - `cursor-task run --id T007`
- Develop independent model implementations in parallel after their tests:
  - `cursor-task run --id T019`
  - `cursor-task run --id T020`
  - `cursor-task run --id T021`
  - `cursor-task run --id T022`
  - `cursor-task run --id T023`

