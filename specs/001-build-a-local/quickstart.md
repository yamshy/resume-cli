# Quickstart: Local-first Resume Tailoring CLI

This guide walks through preparing the environment, running the CLI offline, and validating outputs using bundled sample data.

## Prerequisites
- Linux workstation with high-performance CPU/GPU (per spec baseline)
- Python 3.13 managed via `uv`
- Typst (latest) installed and available on PATH
- Ollama running locally with required models (`mixtral-8x7b-instruct`, `mistral-7b-instruct`)
- Offline environment (disconnect network before generation)

## 1. Bootstrap Environment
```bash
uv python pin 3.13
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install typer fastembed outlines pydantic typst ruff mypy pytest
```

## 2. Prepare Models
```bash
ollama pull mixtral-8x7b-instruct
ollama pull mistral-7b-instruct
```
Confirm `ollama list` shows both models. Disable network afterward.

## 3. Inspect Sample Data
```bash
ls src/resumecli/templates/sample-data/
sqlite3 src/resumecli/templates/sample-data/facts.db ".tables"
```

## 4. Run Diagnostics
```bash
uv run python -m resumecli.cli.main doctor \
  --facts-db src/resumecli/templates/sample-data/facts.db \
  --template default.typ \
  --output json
```
Resolve any warnings/errors before proceeding.

## 5. Generate Resume (Sample Data)
```bash
uv run python -m resumecli.cli.main build \
  --job-posting src/resumecli/templates/sample-data/job_postings/sample_job.txt \
  --facts-db src/resumecli/templates/sample-data/facts.db \
  --template default.typ \
  --output-dir out/sample
```
Outputs:
- `out/sample/resume.pdf`
- `out/sample/coverage.json`
- `out/sample/run.json`

## 6. Review Coverage
```bash
jq '.' out/sample/coverage.json
```
Verify each requirement lists facts/bullets or gap reasons.

## 7. Confirm Facts (Optional)
```bash
uv run python -m resumecli.cli.main facts list --facts-db src/resumecli/templates/sample-data/facts.db --format table
uv run python -m resumecli.cli.main facts confirm --facts-db src/resumecli/templates/sample-data/facts.db --fact-id F-102
```

## 8. Template Operations
```bash
uv run python -m resumecli.cli.main templates list --json
uv run python -m resumecli.cli.main templates render --name default.typ --output-dir out/templates
```

## 9. Run Test Suite
```bash
uv run ruff check src tests
uv run mypy src
uv run pytest
```
All must pass before merging.

## 10. Performance Verification
Inspect `out/sample/run.json` for `duration_seconds <= 60`. Investigate slow stages with logged timings.

## Troubleshooting
- If Typst missing, install locally and ensure PATH includes binary.
- If Ollama unavailable, start service (`ollama serve`) and confirm models before going offline.
- Stale fact warnings → run `resumecli facts doctor` and confirm/update entries.

Maintain Conventional Commit messages and rerun diagnostics/tests after changes.

