# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e` after the models/exceptions
mirror tests. GitHub run [32586919790](https://github.com/wyattowalsh/nbops/actions/runs/32586919790)
verified `e257f87` (107 tests) on CPython 3.12.14 and 3.13.15.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | files already formatted |
| `uv run ty check` | All checks passed |
| `uv run pytest` | **112 passed**, coverage **96.50%** (fail-under 90) |
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

Run [32586919790](https://github.com/wyattowalsh/nbops/actions/runs/32586919790)
on `e257f87` concluded **success** (all 5 jobs):

| Job | Result | Interpreter / notes |
| --- | ------ | ------------------- |
| `workflow-lint` | success | actionlint |
| `lint` | success | ruff check + format |
| `typecheck` | success | ty |
| `test (3.12)` | success | CPython **3.12.14**, 107 passed; Compatibility smoke includes `nbops validate` (`ok`) and `nbops outputs`; demo stats 4 / 2 / 4 |
| `test (3.13)` | success | CPython **3.13.15** (`sys.version` printed), 107 passed; same Compatibility smoke |

Earlier run [32585631217](https://github.com/wyattowalsh/nbops/actions/runs/32585631217) on `f4ded51` was also success (102 tests).
