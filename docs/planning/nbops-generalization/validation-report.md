# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e` after the validate and
output-inventory catalog pass.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | 36 files already formatted |
| `uv run ty check` | All checks passed |
| `uv run pytest` | **107 passed**, coverage **96.38%** (fail-under 90) |
| `uvx pre-commit run --all-files` | Passed (whitespace/EOF hygiene + ruff) |

## Runtime smoke

| Command | Result |
| ------- | ------ |
| `uv run nbops version` | `0.2.0` |
| `uv run nbops ops` | **20** operations listed (including `outputs` and `validate`) |
| `uv run nbops stats examples/demo.ipynb --json` | `total_cells` 4, `code_cells` 2, `code_lines` 4, `kernel` Python 3, `language` python |
| `uv run nbops lint examples/demo.ipynb` | 2 info `NB005` findings, 0 errors |
| `uv run nbops validate examples/demo.ipynb` | `ok` |
| `uv run nbops outputs examples/demo.ipynb --json` | `[]` (demo code cells have no outputs) |

Compatibility invariants (`compute_stats`, `nbops stats`, `POST /notebooks/stats`) hold.

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found in this
repository, sibling Wyatt clones under `/tmp/research`, public GitHub search,
gists (API 403), Drive/Gmail/Linear (MCP unauthenticated), or this run's
transcript (filename only). Recovered TASK-001–023 live in
`codex-kickoff-recovered.md` and are **not** a substitute for the original dump.

## GitHub Actions

Prior verified runs on this branch:

- [32585631217](https://github.com/wyattowalsh/nbops/actions/runs/32585631217) on `f4ded51`: success (actionlint, ruff, ty, pytest 3.12.14 and 3.13.15)
- [32585580529](https://github.com/wyattowalsh/nbops/actions/runs/32585580529): Compatibility smoke including demo stats 4 / 2 / 4 on both interpreters

A later push after this report should re-run CI with `nbops validate` and
`nbops outputs` in the Compatibility smoke step.
