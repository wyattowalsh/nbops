# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e` after demo notebook
contract tests and `just quality-gates`. Local gates: **155 passed**, coverage
**99.24%**. `uvx --from rust-just just quality-gates` passed (ruff, ty, pytest,
demo smoke).

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | files already formatted |
| `uv run ty check` | All checks passed |
| `uv run pytest` | **155 passed**, coverage **99.24%** (fail-under 90) |
| `just quality-gates` | passed via `uvx --from rust-just` |

## Runtime smoke

| Command | Result |
| ------- | ------ |
| `uv run nbops version` | `0.2.0` |
| `uv run nbops --version` | `0.2.0` |
| `uv run python -m nbops version` | `0.2.0` |
| `uv run nbops serve --help` | `Usage: nbops serve [OPTIONS]` |
| `uv run nbops ops` | **20** operations listed; `serve`/`version` are not catalog ops |
| `uv run nbops stats examples/demo.ipynb --json` | `total_cells` 4, `code_cells` 2, `code_lines` 4, `kernel` Python 3, `language` python, `tags` `["demo"]` |
| `uv run nbops validate examples/demo.ipynb` | `ok` |
| `uv run nbops outputs examples/demo.ipynb --json` | `[]` |

Compatibility invariants (`compute_stats`, `nbops stats`, `POST /notebooks/stats`) hold.
`examples/demo.ipynb` cell ids are `title`, `area`, `print-area`, `done`.

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found. Recovered
TASK-001–023 are **not** a substitute for the original dump.

## GitHub Actions

Last fully recorded dual-interpreter proof: [32590811203](https://github.com/wyattowalsh/nbops/actions/runs/32590811203)
on `29abc7d` (**151 passed**, **99.19%** on 3.12.14 and 3.13.15). CI for the
demo-contract HEAD is pending.
