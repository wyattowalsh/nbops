# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e` after the percent-format
roundtrip and catalog CLI/API parity pass.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | 36 files already formatted |
| `uv run ty check` | All checks passed |
| `uv run pytest` | **102 passed**, coverage **95.58%** (fail-under 90) |
| `uvx pre-commit run --all-files` | Passed (whitespace/EOF hygiene + ruff) |

## Runtime smoke

| Command | Result |
| ------- | ------ |
| `uv run nbops version` | `0.2.0` |
| `uv run nbops ops` | **18** operations listed (including `from-py`) |
| `uv run nbops stats examples/demo.ipynb --json` | `total_cells` 4, `code_cells` 2, `code_lines` 4, `kernel` Python 3, `language` python |
| `uv run nbops lint examples/demo.ipynb` | 2 info `NB005` findings, 0 errors |

## Live HTTP (uvicorn `127.0.0.1:8000`)

| Request | Result |
| ------- | ------ |
| `GET /health` | `{"status":"ok","version":"0.2.0"}` |
| `GET /operations` | 18 catalog entries |
| `POST /notebooks/stats` (demo notebook) | 4 / 2 / 4 |
| `POST /notebooks/headings` (demo notebook) | `nbops demo notebook` |
| `POST /notebooks/from-py` | markdown + code cells |

Compatibility invariants (`compute_stats`, `nbops stats`, `POST /notebooks/stats`) hold.

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found in this
repository, sibling Wyatt clones under `/tmp/research`, public GitHub search,
gists (API 403), or this run's transcript (filename only). Recovered
TASK-001–023 live in `codex-kickoff-recovered.md` and are **not** a substitute
for the original dump.

GitHub Actions is defined in `.github/workflows/ci.yml` (actionlint + ruff + ty +
pytest 3.12/3.13). Workflows run on `main`, `cursor/**` pushes, and pull requests
into `main`.
