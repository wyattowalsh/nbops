# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e`.

Last GitHub-verified HEAD `b871503` (run
[32591170814](https://github.com/wyattowalsh/nbops/actions/runs/32591170814)):
**157 passed**, coverage **99.55%** on CPython 3.12.14 and 3.13.15.

This working tree adds remaining defensive-branch tests (API lifespan / split
`ValueError`, successful `nbclient` import, nbformat schema
`NotebookValidationError`, inspect unknown cell/output types, diff insert/unknown
opcodes). Local `uv run pytest` on that follow-up: **164 passed**, coverage
**100.00%**.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | passed |
| `uv run ty check` | All checks passed |
| `uv run pytest` | Local: **164 passed**, **100.00%**. GitHub last verified: **157 passed**, **99.55%** on `b871503` |
| `uvx --from rust-just just quality-gates` | passed (`just check` + `just smoke`; host `just` is not installed in this cloud image) |

## Runtime smoke

Compatibility invariants (`compute_stats`, `nbops stats`, `POST /notebooks/stats`)
hold for `examples/demo.ipynb` (4 / 2 / 4, kernel Python 3, tag `demo`).

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found. Recovered
TASK-001–023 are **not** a substitute.

## GitHub Actions

Run [32591170814](https://github.com/wyattowalsh/nbops/actions/runs/32591170814)
on `b871503` concluded **success** (all 5 jobs): **157 passed**, **99.55%** on
3.12.14 and 3.13.15.
