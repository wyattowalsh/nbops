# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e` at `afd8400`.
Local and GitHub gates are **118 passed**, coverage **97.83%**.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | files already formatted |
| `uv run ty check` | All checks passed |
| `uv run pytest` | **118 passed**, coverage **97.83%** (fail-under 90) |

## Runtime smoke

| Command | Result |
| ------- | ------ |
| `uv run nbops version` | `0.2.0` |
| `uv run nbops --version` | `0.2.0` |
| `uv run python -m nbops version` | `0.2.0` |
| `uv run nbops ops` | **20** operations listed (including `outputs` and `validate`) |
| `uv run nbops stats examples/demo.ipynb --json` | `total_cells` 4, `code_cells` 2, `code_lines` 4, `kernel` Python 3, `language` python |
| `uv run nbops lint examples/demo.ipynb` | 2 info `NB005` findings, 0 errors |
| `uv run nbops validate examples/demo.ipynb` | `ok` |
| `uv run nbops outputs examples/demo.ipynb --json` | `[]` (demo code cells have no outputs) |
| `uv run nbops batch validate examples` | succeeds in CI Compatibility smoke |

Compatibility invariants (`compute_stats`, `nbops stats`, `POST /notebooks/stats`) hold.

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found in this
repository, sibling Wyatt clones under `/tmp/research`, public GitHub search
(HTTP 429/empty), gists (API 403), Drive/Gmail/Linear/Tavily (MCP
unauthenticated), sibling nbops cloud-agent transcripts (role/text only), or this
run's transcript (filename only). Recovered TASK-001–023 live in
`codex-kickoff-recovered.md` and are **not** a substitute for the original dump.

## GitHub Actions

Run [32587917364](https://github.com/wyattowalsh/nbops/actions/runs/32587917364)
on `afd8400` concluded **success** (all 5 jobs):

| Job | Result | Interpreter / notes |
| --- | ------ | ------------------- |
| `workflow-lint` | success | actionlint |
| `lint` | success | ruff check + format |
| `typecheck` | success | ty |
| `test (3.12)` | success | CPython **3.12.14**, **118 passed**; Compatibility smoke includes `python -m nbops version`, `nbops --version`, `nbops validate`, `nbops outputs`, `nbops batch validate examples`; demo stats 4 / 2 / 4 |
| `test (3.13)` | success | CPython **3.13.15** (`sys.version` printed `3.13.15`), **118 passed**; same Compatibility smoke |

Prior verified runs on this branch: [32587289076](https://github.com/wyattowalsh/nbops/actions/runs/32587289076) (`b3045f3`, 113 tests) and [32587098439](https://github.com/wyattowalsh/nbops/actions/runs/32587098439) (`b22df3c`, 112 tests).
