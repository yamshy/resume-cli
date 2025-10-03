# resumecli Constitution

## Core Principles

### I. Local Deterministic Execution
- All commands MUST execute entirely offline; network connectivity is disabled in development, CI, and runtime environments.
- Dependency management, build steps, and caching MUST be controlled by `uv`, producing reproducible lockfiles and deterministic builds across machines.
- CLI workflows MUST avoid machine-specific state; required fixtures and datasets live under version control with documented refresh procedures.
- Release artifacts MUST be reproducible by re-running documented steps; any deviation blocks publication until resolved.

Rationale: Guarantees local-first reliability and reproducibility for every resume build.

### II. Agent-Led Analysis
- Complex analysis, parsing, ranking, and narrative assembly MUST be delegated to approved LLM agents; handcrafted heuristics, bespoke scoring logic, or regex-driven pipelines beyond trivial parsing are prohibited.
- Python code MAY perform deterministic data transformations, file orchestration, and schema validation; ambiguous or knowledge-heavy logic MUST be escalated to agent workflows.
- Plans and specs MUST document the agent responsible for each complex step, including required prompts and expected artifacts.
- New automation MUST preserve the agent-first flow and document reproducibility controls before merging.

Rationale: Maintains clarity of responsibility, leverages LLM strengths, and keeps deterministic glue code simple.

### III. Schema & Provenance Integrity
- All structured data MUST use strict Pydantic models with runtime validation, explicit field constraints, and `validate_assignment` enabled to catch drift.
- Every resume bullet or narrative element MUST carry a `source_id` tying it back to verifiable evidence; missing provenance is a release blocker.
- Titles, dates, metrics, and counts MUST match provided sources exactly; invented or hallucinated values are forbidden.
- Pipelines MUST emit validation reports highlighting schema violations or missing sources before content exits the agent boundary.

Rationale: Ensures factual accuracy, traceability, and trust in generated resumes.

### IV. Quality Gates & Continuous Testing
- `ruff`, `mypy`, and `pytest` MUST all pass locally and in CI before merging; failures halt the pipeline.
- Tests MUST cover unit-level schema enforcement, integration-level CLI flows, and regression scenarios for offline execution.
- Test fixtures MUST remain deterministic and agent-agnostic, enabling repeatable runs without external dependencies.
- New functionality enters the repository alongside tests that fail without the implementation and pass once complete.

Rationale: Enforces a high bar for code quality and prevents regressions in the CLI.

### V. UX & Delivery Fidelity
- CLI UX MUST stay consistent: argument names, subcommands, and exit codes remain stable and documented in `resumecli --help` and offline guides.
- Output formats MUST be ATS-safe plain text by default, with Typst templates providing style-only formatting that never alters content order or wording.
- CLI help, README, and offline docs MUST stay synchronized; every new capability updates user-facing guidance within the repository.
- Error messages and progress indicators MUST remain deterministic and script-friendly, using structured JSON or plain text markers suitable for automation.

Rationale: Delivers predictable, professional resumes and tooling trusted by users and applicant tracking systems.

### VI. Performance & Privacy Discipline
- A full resume generation run on reference data MUST complete in ≤60 seconds (1 minute) on a typical laptop; performance regressions require remediation before release.
- Resource use (memory, disk) MUST remain bounded and documented; profiling accompanies major changes affecting runtime.
- All data stays local by default; logs and artifacts MUST avoid transmitting or embedding personal data beyond the user’s machine.
- Optional telemetry or analytics are disallowed; privacy reviews accompany every new data touchpoint or storage location.

Rationale: Provides a fast, private experience aligned with local-first expectations.

## Mandatory Standards

- Offline-only enforcement is mandatory: disable network interfaces in CI and document local stubs for any third-party data.
- Deterministic builds require `uv`-managed lockfiles, pinned Python versions, and reproducibility checks before releases.
- Provenance auditing: CI MUST fail if any bullet lacks a `source_id` or if referenced evidence is missing.
- Documentation MUST remain local-first: quickstart guides, CLI help, and Typst templates ship with the repo and never require online retrieval.
- Out-of-scope for v0: cloud deployments, hosted APIs, or web UIs are prohibited until expressly ratified by a new constitution version.
- Commit messages MUST follow Conventional Commits; CI MUST reject non-compliant messages before merge.

## Workflow & Execution Governance

- Development plans, specs, and tasks MUST include an explicit Constitution Check verifying compliance with Principles I–VI before implementation proceeds.
- Agent interactions (prompts, expected outputs, guardrails) MUST be versioned alongside code to ensure reproducibility and auditability.
- Python orchestration code MUST remain modular, well-typed, and focused on data transformation; complex decision-making requires agent workflows.
- Release candidates MUST document performance benchmarks, privacy considerations, and provenance audits before tagging.

## Governance

- This constitution supersedes other process documents; conflicts resolve in favor of the stricter rule.
- Amendments require a pull request referencing the impacted principles, updated templates, and a justification that passes maintainer review by consensus.
- Versioning follows semantic rules: MAJOR for principle removals or incompatible rewrites, MINOR for new principles or materially expanded guidance, PATCH for clarifications.
- Compliance reviews occur before each tagged release and during quarterly audits; findings MUST be logged with remediation owners and deadlines.
- Governance artifacts (constitution, plan/spec/tasks templates) MUST stay in sync; any change to one triggers review of the others within the same change set.

**Version**: 1.1.0 | **Ratified**: 2025-10-02 | **Last Amended**: 2025-10-03

