# CLI Contract: `resumecli build`

## Purpose
Generate a resume package (PDF via Typst, `coverage.json`, run log) for a given job posting and fact database while operating offline.

## Invocation
```
resumecli build --job-posting /abs/path/job.txt --facts-db /abs/path/facts.db --template default.typ --output-dir /abs/path/output [--profile minimal]
```

### Arguments
- `--job-posting PATH` (required): Absolute path to sanitized job posting text/Markdown. Must exist and be readable.
- `--facts-db PATH` (required): Absolute path to SQLite database containing curated facts with required schema.
- `--template PATH|NAME` (optional, default `default.typ`): Typst template to render output; resolved relative to shipped templates if not absolute.
- `--output-dir PATH` (optional, default `./out`): Absolute path for generated artifacts; created if missing.
- `--profile {minimal,verbose}` (optional, default `minimal`): Controls logging verbosity and additional diagnostics.
- `--confirm-stale` (flag): Auto-confirm stale facts without prompting (intended for CI; flagged as unsafe for production if unspecified).
- `--no-cache` (flag): Ignore existing embedding cache.

## Preconditions
- Python environment managed by `uv` with dependencies installed locally.
- CLI must run without network access; command fails if network calls detected.
- Fact DB must match expected schema version; mismatches trigger validation error.
- Job posting input sanitized (no PII, consistent encoding).

## Outputs
- Typst-rendered PDF file (`resume.pdf`) in `output-dir`.
- `coverage.json`: Structured coverage map with requirements, facts, bullets, status, gap rationales.
- `run.json`: Execution metadata including timings, prompts used, confirmations.
- Logs to stdout/stderr reflecting stage progress and warnings; optionally `output-dir/log.txt` when verbose.

## Exit Codes
- `0`: Success (resume generated, coverage validated).
- `1`: Validation failure (schema mismatch, provenance gaps, stale facts unconfirmed, runtime >60s envelope breach).
- `2`: Configuration error (missing files, template not found, unsupported Typst version).
- `3`: Agent failure (Ollama/Outlines error, schema mismatch).

## Structured Output Schema (JSON on `--profile verbose`)
```json
{
  "run_id": "uuid",
  "duration_seconds": 42.15,
  "requirements_total": 18,
  "requirements_covered": 14,
  "requirements_partial": 3,
  "requirements_gaps": 1,
  "gap_ids": ["REQ-017"],
  "warnings": ["fact F-102 stale, excluded"]
}
```

## Errors & Guardrails
- Reject if runtime exceeds 60 seconds (soft warning at 45s, hard failure at 60s with exit code 1 unless `--profile verbose` invoked for diagnostic run).
- Prompt user interactively for each stale or unverifiable fact unless `--confirm-stale` is set; record responses in run log.
- Abort if any bullet lacks provenance or introduces new metrics/dates/titles.
- Typst rendering errors surface as configuration errors; include instructions to run `resumecli templates doctor`.

## Logging
- Stage markers: `INGEST`, `EXTRACT`, `RETRIEVE`, `COMPOSE`, `VALIDATE`, `RENDER` with timing metrics.
- Logs recorded in JSON lines when `--profile verbose`.

## Tests (Contract Suite)
- `tests/contract/test_build_contract.py` asserts CLI invocation with sample data returns exit code 0 and expected artifacts.
- Negative tests for missing files, stale fact rejection, agent schema mismatch.

