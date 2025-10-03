# Feature Specification: Local-first Resume Tailoring CLI

**Feature Branch**: `[001-build-a-local]`  
**Created**: 2025-10-03  
**Status**: Draft  
**Input**: User description: "Build a local-first Python CLI that ingests a job posting, extracts structured requirements (JobReq), matches them against a curated fact database, and composes concise resume bullets that each cite their evidence. Output a Typst-rendered PDF and a coverage.json mapping every requirement to matched facts and emitted bullets, highlighting gaps. Why: produce trustworthy, fast (≤1 minute), fully verifiable resumes grounded entirely in my own data."

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints, provenance expectations
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → Include offline execution expectations and ATS-safe output needs
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Include provenance rules, agent involvement, performance/privacy constraints, conventional commit enforcement where applicable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved) and their required provenance fields
7. Specify Agent Responsibilities
   → Document which LLM agents perform complex analysis and required prompts/artifacts
8. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
9. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- ✅ Highlight agent vs. deterministic responsibilities and provenance expectations
- ✅ Note governance gates such as Conventional Commit compliance when relevant to feature scope
- 👥 Written for business stakeholders, not developers

### Section Requirements
- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this spec from a user prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the prompt doesn't specify something (e.g., "login system" without auth method), mark it
3. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
4. **Common underspecified areas**:
   - User types and permissions
   - Data retention/deletion policies  
   - Performance targets and scale
   - Error handling behaviors
   - Integration requirements
   - Security/compliance needs

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a job seeker who curates personal accomplishment facts, I want to run a local CLI that consumes a target job posting and produces a resume PDF plus traceable coverage data so I can confidently respond with evidence-backed bullets without relying on cloud services.

### Acceptance Scenarios
1. **Given** a sanitized job posting file and an approved local fact database, **When** the user runs the CLI with those inputs while offline, **Then** the tool must finish within 60 seconds and emit a Typst-rendered PDF resume, a `coverage.json`, and a summary of any uncovered requirements.
2. **Given** the generated outputs, **When** the user inspects any resume bullet, **Then** each bullet must cite at least one fact `source_id` and reference the corresponding requirement in `coverage.json`, enabling traceable verification back to the curated evidence.

### Edge Cases
- What happens when a job posting lacks explicit bullet-point requirements but includes implied competencies?
- How does the system handle facts that lack sufficient metadata to validate provenance or are older than a defined freshness threshold?

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST ingest a single job posting entirely offline and deliver resume outputs within 60 seconds when executed on a high-performance workstation baseline (8+ performance cores, 32 GB RAM, high-end GPU available) while the CLI session remains local-first.
- **FR-002**: System MUST extract structured JobReq entries via a designated "JobReq Extractor" agent that stores prompts, intermediate reasoning, and span references for auditability, including inferred requirements tagged as "implied" with reduced confidence when sourced from contextual cues.
- **FR-003**: Users MUST be able to select or confirm the curated fact database before generation; every emitted resume bullet must reference at least one validated fact `source_id`, stay ATS-safe, and render in Typst without introducing stylistic artifacts.
- **FR-004**: System MUST produce a `coverage.json` that maps each JobReq to matched fact IDs, generated bullets, coverage status (covered, partial, gap), and rationale notes for gaps.
- **FR-005**: System MUST enforce governance gates so that automated QA (ruff linting, mypy static analysis, pytest unit and integration suites) fail if any resume bullet lacks a linked fact `source_id` or if `coverage.json` reports gaps without documented rationale; provenance integrity and coverage completeness MUST be validated automatically before the feature can ship.
- **FR-006**: System MUST solicit user confirmation on any fact whose relevance or freshness is uncertain; unconfirmed facts are excluded from generation and flagged in session logs.

*Example of marking unclear requirements during drafting (remove before finalization):*
- System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities & Provenance *(include if feature involves data)*
- **Job Posting Input**: Represents the target role description; attributes include `source_path`, `ingestion_timestamp`, `sanitized_text`, and original provenance metadata (publisher, capture method). Requires `source_id` to track the origin of each extracted requirement.
- **Job Requirement (JobReq)**: Structured statement of employer expectations; attributes include `requirement_id`, `description`, `priority`, `evidence_confidence`, `source_span`, and `inference_type` (explicit or implied). Must retain link back to Job Posting `source_id` and extractor agent version.
- **Curated Fact**: User-verified achievement or metric stored locally in a SQLite database; attributes include `fact_id`, `narrative`, `metrics`, `validation_date`, supporting documents, table-level schema version, and `verification_status`. Requires provenance fields `source_id`, `owner_id`, and captures `last_confirmed_at` when a user approves uncertain facts during CLI execution.
- **Resume Bullet**: Output statement targeted to job requirements; attributes include `bullet_id`, `content`, `cited_fact_ids`, `target_requirement_ids`, and `confidence`. Must embed provenance to the JobReq and curated facts.
- **Coverage Entry**: JSON object linking requirements to matched facts and bullets; fields include `requirement_id`, `matched_fact_ids`, `bullet_ids`, `coverage_status`, `gap_reason`, and `last_evaluated_at`.

Additional clarifications needed:

---

## Clarifications

### Session 2025-10-03
- Q: What baseline hardware profile should the ≤60 second end-to-end runtime guarantee assume? → A: High-performance workstation with high-end GPU
- Q: Which storage format will the curated fact database use to feed the CLI? → A: Local SQLite database
- Q: How should the CLI flag curated facts that are outdated or unverifiable before bullet generation? → A: User confirmation on uncertain facts
- Q: Which automated QA gates must the feature pass before shipping? → A: Ruff + mypy + pytest (unit & integration)
- Q: How should the CLI treat job posting requirements that are implied but not explicitly stated (e.g., inferred soft skills)? → A: Allow inference tagged as implied with lower confidence

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous  
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [ ] Review checklist passed

---
