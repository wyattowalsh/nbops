# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e` at `b884224`.
Local and GitHub gates are **128 passed**, coverage **98.64%**.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | files already formatted |
| `uv run ty check` | All checks passed |
| `uv run pytest` | **128 passed**, coverage **98.64%** (fail-under 90) |

## Runtime smoke

| Command | Result |
| ------- | ------ |
| `uv run nbops version` | `0.2.0` |
| `uv run nbops --version` | `0.2.0` |
| `uv run python -m nbops version` | `0.2.0` |
| `uv run nbops serve --help` | `Usage: nbops serve [OPTIONS]` |
| `uv run nbops ops` | **20** operations listed (including `outputs` and `validate`); `serve`/`version` are not catalog ops |
| `uv run nbops stats examples/demo.ipynb --json` | `total_cells` 4, `code_cells` 2, `code_lines` 4, `kernel` Python 3, `language` python |
| `uv run nbops lint examples/demo.ipynb` | 2 info `NB005` findings, 0 errors |
| `uv run nbops validate examples/demo.ipynb` | `ok` |
| `uv run nbops outputs examples/demo.ipynb --json` | `[]` (demo code cells have no outputs) |
| `uv run nbops batch validate examples` | succeeds in CI Compatibility smoke |

Compatibility invariants (`compute_stats`, `nbops stats`, `POST /notebooks/stats`) hold.
Mutating CLI (`clean`, `filter`, `tag`, `ids`, `kernel`, `exec`) requires `--output` or `--in-place`.

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found in this
repository, sibling Wyatt clones under `/tmp/research` (`nbadb`, `proxywhirl`,
`riso`, `agents`, `prompts`, `dotfiles`, `template`), public GitHub search
(empty), gists (API 404), Drive/Gmail/Linear/Tavily (MCP `needsAuth`), sibling
nbops cloud-agent transcripts (role/text only), or this run's transcript
(filename only). Recovered TASK-001–023 live in `codex-kickoff-recovered.md`
and are **not** a substitute for the original dump.

## GitHub Actions

Run [32588732104](https://github.com/wyattowalsh/nbops/actions/runs/32588732104)
on `b884224` concluded **success** (all 5 jobs):

| Job | Result | Interpreter / notes |
| --- | ------ | ------------------- |
| `workflow-lint` | success | actionlint |
| `lint` | success | ruff check + format |
| `typecheck` | success | ty |
| `test (3.12)` | success | CPython **3.12.14**, **128 passed**; Compatibility smoke includes `python -m nbops version`, `nbops --version`, `nbops validate`, `nbops outputs`, `nbops batch validate examples`, `nbops serve --help`; demo stats 4 / 2 / 4 |
| `test (3.13)` | success | CPython **3.13.15** (`sys.version` printed `3.13.15`), **128 passed**; same Compatibility smoke |

Prior verified runs on this branch include [32588626150](https://github.com/wyattowalsh/nbops/actions/runs/32588626150) (`24290d8`, serve + fail-closed writes), [32587917364](https://github.com/wyattowalsh/nbops/actions/runs/32587917364) (`afd8400`, 118 tests), and [32588007650](https://github.com/wyattowalsh/nbops/actions/runs/32588007650) (`6756640`).
