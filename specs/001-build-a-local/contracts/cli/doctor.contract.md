# CLI Contract: `resumecli doctor`

## Purpose
Run diagnostics ensuring environment, dependencies, and datasets meet requirements for offline resume builds.

## Invocation
```
resumecli doctor [--facts-db /abs/path/facts.db] [--template default.typ] [--output json]
```

## Checks
- `env`: Confirms Python 3.13 via `uv`, dependency versions, Typst availability, Ollama running locally.
- `performance`: Executes dry-run pipeline with cached sample data to estimate runtime; warns if >45s.
- `db`: Validates fact DB schema, FTS5 index presence, row counts, stale facts summary.
- `templates`: Renders quick Typst smoke test (optional).

## Outputs
- Human-readable summary; optional JSON via `--output json` containing check results and durations.
- Logs stored under `output/doctor-report.json` when JSON requested.

## Exit Codes
- `0`: All checks pass.
- `1`: Non-critical warnings (performance borderline, stale data) but user attention required.
- `2`: Critical failure (missing dependency, schema mismatch, Typst absent).

## Guardrails
- Doctor never modifies data; read-only unless user opts into `--fix` (future extension).
- Performance check uses sample dataset; no sensitive user data touched.

## Tests
- `tests/contract/test_doctor_contract.py` mocks environment to exercise pass/fail states.

