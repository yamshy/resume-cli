# Phase 0 Research: Local-first Resume Tailoring CLI

## Overview
This document captures Phase 0 research findings for the local-first resume tailoring CLI. All decisions prioritize offline execution, provenance integrity, and sub-60-second runtimes on the reference workstation.

## Research Log

### Decision: Python 3.13 via uv
- **Rationale**: Aligns with user directive to use Python 3.13 and `uv`; latest Python features improve typing (PEP 695, |None syntax) and performance. `uv` provides reproducible offline lockfiles.
- **Alternatives Considered**: Python 3.12 (stable today) but rejected due to requirement for latest (3.13) and desire for cutting-edge typing/runtime upgrades. Conda discouraged due to constitution (uv mandated).

### Decision: Typer for CLI Architecture
- **Rationale**: Typer offers modern, type-friendly CLI building with async support, deterministic arg parsing, and good docstring integration for `resumecli --help`. Works well with subcommands (build, facts, templates, doctor).
- **Alternatives Considered**: Click (Typer’s foundation) rejected for less ergonomic type hints; argparse too manual; Rich CLI adds unnecessary dependencies.

### Decision: SQLite + FTS5 for Facts Storage
- **Rationale**: Embedded, offline-friendly DB with FTS5 for full-text search; supports deterministic file-based distribution. Matches user requirement and clarifications. Allows shipping sample database.
- **Alternatives Considered**: DuckDB (good analytics but heavier and less standard), plain JSON/YAML (no FTS, poor concurrency), Postgres (requires server, violates offline simplicity).

### Decision: fastembed for Local Embeddings
- **Rationale**: Provides efficient local embedding generation with GPU support; integrates with Python and supports incremental caching. Works offline and has permissive licensing. Configurable for hybrid search.
- **Alternatives Considered**: sentence-transformers (heavier dependencies), llama-index embedding modules (overkill), BGE models without tooling (more manual). fastembed balances speed and reliability.

### Decision: Outlines + Ollama for JobReq Extraction
- **Rationale**: Outlines enforces schema-safe generation with Pydantic integration; Ollama offers local LLM hosting, matching constitution (offline). Schema-constrained extraction ensures reproducible JobReq parsing with confidence tagging.
- **Alternatives Considered**: OpenAI APIs (no, violates offline), manual heuristics (violates agent-led principle), LangChain (less strict schema control, heavier dependencies).

### Decision: Pydantic (v2) for Data Models
- **Rationale**: Enforces strong validation, `validate_assignment`, JSON serialization, and integrates with Outlines. Latest version aligns with user request. Supports dataclass-like ergonomics.
- **Alternatives Considered**: attrs/dataclasses (less validation), Marshmallow (less type integration). Pydantic is constitutionally mandated.

### Decision: Typst for Rendering
- **Rationale**: Latest Typst enables reproducible PDF generation with deterministic layout while keeping text ATS-safe. Template files can ship with repo.#
- **Alternatives Considered**: LaTeX (heavier, less accessible), WeasyPrint (HTML-based, more dependencies). Typst meets requirement.

### Decision: Logging Timings & Performance Envelope
- **Rationale**: Must enforce ≤60-second build; plan includes instrumentation around ingestion, extraction, retrieval, composition, rendering. Use monotonic timers and structured logs saved locally.
- **Alternatives Considered**: Post-hoc profiling only (insufficient), ignoring logging (violates requirement).

### Decision: Hybrid Retrieval (FTS5 + Embeddings)
- **Rationale**: Combine FTS5 keyword search with cosine similarity from fastembed for robust matching. Pipeline: run FTS query, fetch embedding candidates, unify results via weighted scoring.
- **Alternatives Considered**: Embeddings-only (slow, heavy), FTS-only (misses semantic matches). Hybrid approach best meets accuracy/performance tradeoff.

### Decision: Agent Prompt Catalog Structure
- **Rationale**: Store under `specs/001-build-a-local/contracts/agents/`, markdown prompts with guardrails and expected outputs. Satisfies constitution’s agent versioning requirement.
- **Alternatives Considered**: In-code strings (harder to audit), JSON (less readable). Markdown fosters documentation.

### Decision: CLI Subcommands
- **Rationale**: `build` for resume generation, `facts` for managing fact DB, `templates` to list/render templates, `doctor` to run diagnostics and performance checks. Aligns with user request and ensures modular CLI.
- **Alternatives Considered**: Single command with flags (less discoverable), splitting into multiple binaries (overkill).

### Decision: Offline QA & CI Pipeline
- **Rationale**: Use `uv` scripts to run `ruff`, `mypy`, `pytest`, and Typst smoke tests. Mirror locally and in CI with network disabled, caching dependencies via `uv`.
- **Alternatives Considered**: Manual command sequences (less consistent), other linters (not mandated).

### Decision: Validation Guardrails
- **Rationale**: Build validation layer that rejects bullets without evidence, ensures no new numbers/dates/titles, and surfaces unconfirmed facts. Use Pydantic validators and additional deterministic checks.
- **Alternatives Considered**: Trust agent output; rejected per constitution.

### Decision: Sample Dataset & Templates Bundling
- **Rationale**: Ship curated sample facts DB, job posting examples, Typst templates under `src/resumecli/templates/sample-data/`. Ensures offline quickstart and deterministic tests.
- **Alternatives Considered**: Download on-demand (violates offline), user-provided only (hurts testing & docs).

### Decision: Coverage Reporting (`coverage.json`)
- **Rationale**: Structured JSON capturing requirement coverage, matching facts/bullets, statuses, and gap rationales. Enables tests to assert completeness and ensures auditing.
- **Alternatives Considered**: Plain text logs (less machine-checkable), PDF-only annotations (hard to parse).

### Decision: Freshness Confirmation Flow
- **Rationale**: CLI prompts user to confirm stale facts; unconfirmed facts excluded and logged. Use interactive prompts or config flags; ensure deterministic logs for tests.
- **Alternatives Considered**: Automatic heuristics (violates agent-led analysis), ignoring freshness (violates requirement).

## Unresolved Items
None — Clarifications satisfied by spec (Session 2025-10-03).

