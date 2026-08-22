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

## GitHub Actions

Run [32585325015](https://github.com/wyattowalsh/nbops/actions/runs/32585325015)
on `b3606f2` concluded **success** for:

| Job | Result | Note |
| --- | ------ | ---- |
| `workflow-lint` | success | actionlint |
| `lint` | success | ruff check + format |
| `typecheck` | success | ty |
| `test (3.12)` | success | 102 passed, 95.58% coverage, Python 3.12.14 |
| `test (3.13)` | success | **not a 3.13 interpreter** — `uv` honored `.python-version` (3.12.3) |

The matrix is being fixed so `UV_PYTHON` / `--python` override `.python-version`
and the 3.13 job actually runs 3.13.
