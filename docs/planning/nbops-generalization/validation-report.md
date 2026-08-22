# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e` after the catalog/settings
parity pass.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | 36 files already formatted |
| `uv run ty check` | All checks passed |
| `uv run pytest` | 82 passed, coverage 91.53% (fail-under 85) |

## Runtime smoke

| Command | Result |
| ------- | ------ |
| `uv run nbops version` | `0.2.0` |
| `uv run nbops ops` | 17 operations listed (stats through ops) |
| `uv run nbops stats examples/demo.ipynb --json` | `total_cells` 4, `code_cells` 2, `code_lines` 4 |
| `uv run nbops lint examples/demo.ipynb` | 2 info `NB005` findings, 0 errors |

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found in git,
GitHub, Drive/Gmail/Linear MCP (unauthenticated), or prior nbops cloud-agent
transcripts. This report does not claim that original document is complete.
