# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e`. Local follow-up adds lint
output-size edges and HTTP demo stats. Last GitHub-verified HEAD `09a0069`
(run [32591070323](https://github.com/wyattowalsh/nbops/actions/runs/32591070323)):
**155 passed**, coverage **99.24%** on CPython 3.12.14 and 3.13.15.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed on `09a0069` |
| `uv run ty check` | All checks passed on `09a0069` |
| `uv run pytest` | GitHub: **155 passed**, **99.24%**; local follow-up pending on this revision |

## Runtime smoke

Compatibility invariants (`compute_stats`, `nbops stats`, `POST /notebooks/stats`)
hold for `examples/demo.ipynb` (4 / 2 / 4, kernel Python 3, tag `demo`).

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found. Recovered
TASK-001–023 are **not** a substitute.

## GitHub Actions

Run [32591070323](https://github.com/wyattowalsh/nbops/actions/runs/32591070323)
on `09a0069` concluded **success** (all 5 jobs): **155 passed**, **99.24%** on
3.12.14 and 3.13.15. Product commit [32591008820](https://github.com/wyattowalsh/nbops/actions/runs/32591008820)
on `d417178` matched those counts.
