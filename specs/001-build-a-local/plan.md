
# Implementation Plan: Local-first Resume Tailoring CLI

**Branch**: `001-build-a-local` | **Date**: 2025-10-03 | **Spec**: `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/spec.md`
**Input**: Feature specification from `/var/home/shyam/projects/resume-cli/specs/001-build-a-local/spec.md`

## Summary
- Build a Python-based local-first CLI that ingests a job posting, extracts structured `JobReq` data via an LLM agent workflow, cross-references a curated fact database, and composes Typst-rendered resume bullets with traceable coverage metadata.
- Outputs include a Typst-generated PDF resume, `coverage.json` mapping requirements to facts/bullets/gaps, and user-facing summaries that highlight uncovered requirements while enforcing provenance and schema integrity.
- Must complete runs within one minute on the reference workstation, operate offline, and pass governance gates (`uv`, `ruff`, `mypy`, `pytest`) before shipping.

## Technical Context
**Language/Version**: Python 3.13 (managed via `uv`)  
**Primary Dependencies**: Typer (CLI), SQLite with FTS5, fastembed (local embeddings), Outlines + Ollama (JobReq extraction and schema alignment), Pydantic (models/validation), Typst (rendering), `uv` toolchain, `ruff`, `mypy`, `pytest`  
**Storage**: Local SQLite database files (facts, caches) with associated Typst templates and artifact directories; no remote storage  
**Testing**: `pytest` for unit/integration, `ruff` for linting, `mypy` for typing; CI mirrors local commands via `uv` scripts  
**Target Platform**: Linux workstation (offline, GPU-enabled) with reproducible `uv` environment  
**Project Type**: Single CLI project (deterministic local-first tooling)  
**Performance Goals**: End-to-end resume build completes in ≤60 seconds; agent prompts and embeddings pipelined to stay within runtime budget  
**Constraints**: Offline-only execution, deterministic builds via `uv`, provenance preservation, no invented metrics/dates/titles, schema-first validation, Conventional Commit enforcement  
**Scale/Scope**: Single-user local CLI workflows with bundled sample datasets/templates, extensible to multiple job postings sequentially

## Constitution Check
- **Local Deterministic Execution**: Plan uses `uv`-managed Python 3.13 environment, locks dependencies, and stores all artifacts locally. Offline execution enforced; CI mirrors local offline workflows.
- **Agent-Led Analysis**: Outlines + Ollama powered JobReq extractor handles ambiguous parsing, implication handling, and schema-safe outputs. Deterministic Python orchestrates ingestion, validation, retrieval, and rendering without replacing agent reasoning.
- **Schema & Provenance Integrity**: Pydantic models with `validate_assignment` capture JobReq, Fact, Bullet, Coverage entities. Every bullet cites fact `source_id` and requirement links; validation pipeline rejects missing provenance before composing outputs.
- **Quality Gates & Continuous Testing**: `ruff`, `mypy`, `pytest` integrated via `uv` scripts; CI replicates offline runs. Tests cover schema integrity, agent contract mocks, hybrid retrieval correctness, Typst render checks.
- **UX & Delivery Fidelity**: Typer CLI subcommands (`build`, `facts`, `templates`, `doctor`) documented in `quickstart.md` and CLI help. Typst templates focus on presentation, keeping text ATS-safe and deterministic.
- **Performance & Privacy Discipline**: Embedding cache + FTS5 hybrid retrieval tuned for <60s runtime; logging includes timings and checkpoints without leaking personal data. No network calls; local GPU usage documented.
- **Governance Discipline**: Conventional Commit policy reiterated; plan documents governance gates (CI suite, offline enforcement). Agent prompt catalog versioned under `/contracts/`.

## Project Structure

### Documentation (this feature)
```
specs/001-build-a-local/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── agents/
│   │   ├── jobreq_extractor.prompt.md
│   │   ├── bullet_composer.prompt.md
│   │   └── validation_reviewer.prompt.md
│   └── cli/
│       ├── build.contract.md
│       ├── facts.contract.md
│       ├── templates.contract.md
│       └── doctor.contract.md
└── tasks.md
```

### Source Code (repository root)
```
src/
├── resumecli/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py           # Typer app entry
│   │   ├── build.py
│   │   ├── facts.py
│   │   ├── templates.py
│   │   └── doctor.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   ├── extraction.py
│   │   ├── retrieval.py
│   │   ├── composition.py
│   │   ├── validation.py
│   │   └── rendering.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── job_posting.py
│   │   ├── jobreq.py
│   │   ├── fact.py
│   │   ├── bullet.py
│   │   ├── coverage.py
│   │   ├── embedding_cache.py
│   │   └── run_log.py
│   ├── services/
│   │   ├── embeddings.py
│   │   ├── storage.py
│   │   └── logging.py
│   └── templates/
│       ├── default.typ
│       └── sample-data/
│           ├── facts.db
│           └── job_postings/
│               └── sample_job.txt
└── tests/
    ├── unit/
    │   ├── test_models.py
    │   ├── test_ingestion.py
    │   ├── test_extraction.py
    │   ├── test_retrieval.py
    │   ├── test_composition.py
    │   └── test_validation.py
    ├── integration/
    │   ├── test_cli_build.py
    │   ├── test_cli_facts.py
    │   ├── test_cli_templates.py
    │   └── test_cli_doctor.py
    └── contract/
        ├── test_build_contract.py
        ├── test_facts_contract.py
        ├── test_templates_contract.py
        └── test_doctor_contract.py
```

**Structure Decision**: Single-project CLI under `src/resumecli`, segregating functional modules (`ingestion`, `extraction`, `retrieval`, `composition`, `validation`, `rendering`) with Typer-driven CLI entrypoints; tests mirror module layout with unit, integration, and contract suites.

## Phase 0: Outline & Research
- Extract unknowns derived from Technical Context (e.g., best practices for fastembed offline usage, Outlines schema alignment with Ollama, Typst rendering optimizations, hybrid FTS5+embedding retrieval tuning, offline `uv` workflows).
- Dispatch research tasks covering: embedding caching strategies, Typer CLI UX patterns, SQLite FTS5 indexing with Python, Outlines schema guarantee patterns, Ollama local model selection/perf trade-offs, Typst templating for ATS-safe resumes, enforcement of ≤60s runtime with profiling checkpoints.
- Consolidate findings in `research.md` using decision/rationale/alternatives structure, ensuring all clarifications resolved and agent responsibilities documented.

## Phase 1: Design & Contracts
- Derive detailed entity schemas in `data-model.md` for JobReq, Curated Fact, Resume Bullet, Coverage Entry, and supporting cache/metadata structures with Pydantic models and validation logic including `validate_assignment`.
- Generate CLI contract specs under `contracts/cli/` for `build`, `facts`, `templates`, `doctor` commands (inputs, outputs, error states, JSON schemas), ensuring offline invariants noted.
- Create agent prompt catalog under `contracts/agents/`, documenting JobReq Extractor prompt template (Outlines+Ollama), Bullet Composer agent instructions, Validation Reviewer responsibilities, with guardrails for provenance, freshness confirmation, and implied requirement tagging.
- Author `quickstart.md` to cover prerequisites (`uv python pin`, dataset setup, CLI usage examples), expected runtime, offline guarantees, and Typst rendering instructions.
- Ensure design addresses hybrid retrieval (FTS5 scoring + embedding similarity), caching of embeddings, log timings, and fallback behaviors when facts are stale/unconfirmed.
- Re-run Constitution Check post-design; iterate if conflicts arise.

## Phase 2: Task Planning Approach
- `/tasks` command will use design artifacts to generate ~25-30 tasks covering tests-first workflow: contract tests, model implementations, service modules, agent integrations, Typst template finalization, CLI command wiring, validation/test coverage, and performance profiling steps.
- Ordering emphasizes TDD: create failing contract/unit tests, implement Pydantic models and storage, integrate Outlines/Ollama pipelines, finalize retrieval/composition, and render/coverage outputs. Mark parallelizable tasks `[P]` where modules are independent.

## Phase 3+: Future Implementation
- Phase 3 (`/tasks`) generates `tasks.md` from finalized design.
- Phase 4 executes implementation following tasks, ensuring offline agent workflows and provenance checks.
- Phase 5 runs validation suite (`uv run ruff`, `uv run mypy`, `uv run pytest`, Typst render check, timing benchmarks).
- Governance QA introduces automated `uv` scripts (e.g., `uv run qa-provenance`, `uv run qa-coverage`) that fail builds when bullets lack fact links or when `coverage.json` reports undocumented gaps, satisfying FR-005 enforcement.

## Complexity Tracking
| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|---------------------------------------|
| *None* | | |

## Progress Tracking
**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Conventional Commit policy documented
- [x] Complexity deviations documented
