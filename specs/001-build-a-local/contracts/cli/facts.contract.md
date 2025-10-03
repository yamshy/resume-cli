# CLI Contract: `resumecli facts`

## Purpose
Inspect and manage the curated fact database, including listing facts, verifying metadata, and confirming freshness.

## Subcommands

### `resumecli facts list`
```
resumecli facts list --facts-db /abs/path/facts.db [--format {table,json}] [--limit 50] [--filter verified]
```
- Outputs table/JSON of facts with `fact_id`, `summary`, `verification_status`, `validation_date`, `last_confirmed_at`.

### `resumecli facts confirm`
```
resumecli facts confirm --facts-db /abs/path/facts.db --fact-id F-123
```
- Prompts user to confirm relevance/freshness; updates `last_confirmed_at` and `verification_status`.

### `resumecli facts doctor`
```
resumecli facts doctor --facts-db /abs/path/facts.db
```
- Runs integrity checks: schema version, missing documents, stale facts (older than configurable threshold), index health.

## Preconditions
- SQLite DB accessible and matches schema version.
- Commands run offline; no network I/O.
- User must have permissions to modify DB when running confirm.

## Outputs
- Stdout tables/JSON for `list`.
- Confirmation prompts recorded in run log (shared across CLI).
- `facts_doctor.json` diagnostic report for doctor subcommand.

## Exit Codes
- `0`: Success.
- `1`: Validation error (schema mismatch, missing fact).
- `2`: DB connection failure.

## Guardrails
- `confirm` refuses to promote facts lacking supporting documents.
- `doctor` warns if FTS index missing and suggests rebuild command.

## Tests
- `tests/contract/test_facts_contract.py` covers list/confirm/doctor flows using sample DB.

