# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e`.

GitHub-verified HEAD `acc442f` (run
[32591701982](https://github.com/wyattowalsh/nbops/actions/runs/32591701982)):
**164 passed**, coverage **100.00%** on CPython 3.12.14 and 3.13.15.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | passed |
| `uv run ty check` | All checks passed |
| `uv run pytest` | **164 passed**, **100.00%** (`--cov-fail-under=90`) |
| `uvx --from rust-just just quality-gates` | passed (`just check` + `just smoke`; host `just` is not installed in this cloud image) |
| GitHub Actions `CI` on `cursor/nbops-generalization-673e` @ `acc442f` | **success** — workflow-lint, lint, typecheck, test **3.12.14** and **3.13.15** (**164 passed**, **100.00%** each) |

## Runtime smoke

Compatibility invariants (`compute_stats`, `nbops stats`, `POST /notebooks/stats`)
hold for `examples/demo.ipynb` (4 / 2 / 4, kernel Python 3, tag `demo`).

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found. Recovered
TASK-001–023 are **not** a substitute.
