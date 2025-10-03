# CLI Contract: `resumecli templates`

## Purpose
Manage Typst templates bundled with the CLI and allow preview/export of sample renders.

## Subcommands

### `resumecli templates list`
```
resumecli templates list
```
- Prints available template names, descriptions, and path references.

### `resumecli templates show`
```
resumecli templates show --name default.typ
```
- Displays template metadata plus key sections (header, bullet styles).

### `resumecli templates render`
```
resumecli templates render --name default.typ --output-dir /abs/path/output
```
- Renders template with sample data to confirm Typst toolchain functions offline.

## Preconditions
- Typst binary installed locally; CLI locates via env var or config.
- Template files stored under `src/resumecli/templates/`.

## Outputs
- `list` prints table/JSON (optionally `--json`).
- `show` prints template excerpt and metadata.
- `render` produces sample PDF in output dir.

## Exit Codes
- `0`: Success.
- `1`: Template missing or invalid.
- `2`: Typst render failure.

## Guardrails
- `render` uses bundled sample facts/job posting to avoid leaking user data.
- Failing render surfaces actionable message (check Typst version, run `resumecli doctor`).

## Tests
- `tests/contract/test_templates_contract.py` ensures list/show/render behave with sample data.

