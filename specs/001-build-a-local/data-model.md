# Data Model: Local-first Resume Tailoring CLI

## Overview
All structured data uses Pydantic v2 models with `validate_assignment=True`, strict field types, and provenance enforcement. IDs follow UUIDv7 unless noted.

## Entities

### JobPosting
- **Fields**:
  - `source_id: str` – unique identifier for provenance (e.g., hash of sanitized input)
  - `source_path: Path` – absolute path to job posting file
  - `ingestion_timestamp: datetime`
  - `sanitized_text: str`
  - `publisher: str | None`
  - `capture_method: Literal["manual", "scrape", "email", "other"]`
  - `hardware_profile: str` (optional metadata about system used during extraction)
- **Constraints**: `sanitized_text` non-empty; `ingestion_timestamp` timezone-aware; `capture_method` enumerated.
- **Relationships**: Owns JobReqs.

### JobReq
- **Fields**:
  - `requirement_id: str`
  - `description: str`
  - `priority: Literal["must", "nice-to-have", "implied"]`
  - `evidence_confidence: Literal["high", "medium", "low"]`
  - `source_span: tuple[int, int]` (start, end indices in `sanitized_text`)
  - `inference_type: Literal["explicit", "implied"]`
  - `source_id: str` – references `JobPosting.source_id`
  - `extractor_version: str`
  - `created_at: datetime`
- **Constraints**: `description` ≥ 10 characters; `source_span` within text range; `inference_type` aligns with `priority`; `evidence_confidence` downgraded for implied requirements by validator.
- **Relationships**: Linked to CoverageEntry and Bullet via IDs.

### CuratedFact
- **Fields**:
  - `fact_id: str`
  - `narrative: str`
  - `metrics: list[Metric]`
  - `validation_date: date`
  - `supporting_documents: list[DocumentRef]`
  - `schema_version: str`
  - `verification_status: Literal["verified", "unverified", "stale"]`
  - `source_id: str`
  - `owner_id: str`
  - `last_confirmed_at: datetime | None`
- **Constraints**: `narrative` non-empty; `validation_date` ≤ today; metrics validated for numeric integrity; `verification_status` transitions guard against skipping confirmation (stale → verified requires confirmation event).
- **Relationships**: Many-to-many with JobReq via CoverageEntry and Bullet.

#### Metric (embedded)
- `name: str`
- `value: Decimal`
- `unit: str | None`
- `confidence: Literal["high", "medium", "low"]`
- Validators enforce no novel metrics (must exist in fact references) and `value` precision ≤ 2 decimal places.

#### DocumentRef (embedded)
- `doc_id: str`
- `description: str`
- `path: Path`
- Validators ensure `path` exists at runtime (checked lazily during CLI run) and is within repo data directories.

### ResumeBullet
- **Fields**:
  - `bullet_id: str`
  - `content: str`
  - `cited_fact_ids: list[str]`
  - `target_requirement_ids: list[str]`
  - `confidence: Literal["high", "medium", "low"]`
  - `source_id: str` – aggregated hash of `cited_fact_ids` + `target_requirement_ids`
  - `render_order: int`
- **Constraints**: `content` 1–280 chars, ATS-safe (validator ensures ASCII + limited punctuation); at least one `cited_fact_id`; `confidence` ≤ min confidence of referenced facts; `render_order` non-negative.
- **Relationships**: Many-to-many with CuratedFact and JobReq.

### CoverageEntry
- **Fields**:
  - `requirement_id: str`
  - `matched_fact_ids: list[str]`
  - `bullet_ids: list[str]`
  - `coverage_status: Literal["covered", "partial", "gap"]`
  - `gap_reason: str | None`
  - `last_evaluated_at: datetime`
  - `notes: str | None`
- **Constraints**: Validators ensure gap reasoning provided when `coverage_status == "gap"`; `matched_fact_ids` subset of facts; `bullet_ids` subset of bullet registry; `last_evaluated_at` updated after each run.
- **Relationships**: Links JobReq to facts/bullets; used in coverage.json.

### EmbeddingCacheEntry
- **Fields**:
  - `embedding_id: str`
  - `fact_id: str | None`
  - `jobreq_id: str | None`
  - `vector: list[float]`
  - `model_name: str`
  - `created_at: datetime`
- **Constraints**: Exactly one of `fact_id` or `jobreq_id` populated; `vector` length matches model spec; stored locally in SQLite or binary file.
- **Relationships**: Supports hybrid retrieval.

### RunLog
- **Fields**:
  - `run_id: str`
  - `started_at: datetime`
  - `completed_at: datetime | None`
  - `duration_seconds: float | None`
  - `timings: dict[str, float]`
  - `warnings: list[str]`
  - `facts_confirmed: list[str]`
  - `facts_rejected: list[str]`
- **Constraints**: `duration_seconds` auto-computed; timings keyed by pipeline stage; warnings include stale/unconfirmed fact notices.

## Relationships Summary
- JobPosting 1..* JobReq
- JobReq *..* CuratedFact via CoverageEntry/Bullet
- CuratedFact *..* ResumeBullet (via citations)
- ResumeBullet *..* JobReq (via `target_requirement_ids`)
- EmbeddingCacheEntry optional relation to JobReq/CuratedFact
- RunLog traces each CLI invocation

## Validation Rules
- No bullet can cite facts with `verification_status != "verified"` unless user confirmed within session → enforced by validator referencing RunLog.
- Metrics cannot introduce new numerics compared to `CuratedFact` baseline → content validator cross-checks digits.
- Date/titles must match curated facts exactly → compose stage prevents modifications, validated before render.
- Coverage must mark explicit gaps; missing bullet or fact triggers `coverage_status="gap"` and note.

## Storage Mapping
- SQLite tables: `job_postings`, `job_requirements`, `facts`, `metrics`, `documents`, `bullets`, `coverage`, `embedding_cache`, `run_logs`
- FTS5 virtual table (`facts_fts`) for narrative search with rowid referencing `facts`
- JSON artifacts: `coverage.json`, `run_{timestamp}.json` (logs)
- Typst templates under `src/resumecli/templates`

## Agent Responsibilities (Data Touchpoints)
- JobReq Extractor Agent writes JobReq records (schema contract).
- Bullet Composer Agent consumes JobReq + facts, outputs bullet drafts with citations (validated via Pydantic before acceptance).
- Validation Reviewer Agent checks gaps, freshness justifications, ensures ATS safety recommendations.

## Notes
- All datetime fields stored in UTC.
- IDs generated deterministically (UUIDv5 with namespace per entity) to allow reproducible runs.
- Data model keeps to ASCII to maintain Typst compatibility and ATS safety.

