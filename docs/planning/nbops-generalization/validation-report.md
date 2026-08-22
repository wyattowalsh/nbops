# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e` after Jupytext kernelspec,
`nbops new` display-name, and output-linked clean-key completeness. Local gates:
**151 passed**, coverage **99.19%**.

GitHub-verified HEAD: `29abc7d` (run
[32590811203](https://github.com/wyattowalsh/nbops/actions/runs/32590811203),
**151 passed**, coverage **99.19%** on CPython 3.12.14 and 3.13.15).

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | All checks passed |
| `uv run ruff format --check src tests` | files already formatted |
| `uv run ty check` | All checks passed |
| `uv run pytest` | **151 passed**, coverage **99.19%** (fail-under 90); `src/nbops/convert.py`, `clean.py`, `cli.py`, `transform.py` at **100%** |

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
| `uv run nbops convert examples/demo.ipynb --to py` | percent script includes `tags=["demo"]` |
| `uv run nbops batch validate examples` | succeeds in CI Compatibility smoke |

Compatibility invariants (`compute_stats`, `nbops stats`, `POST /notebooks/stats`) hold.
Mutating CLI (`clean`, `filter`, `tag`, `ids`, `kernel`, `exec`) requires `--output` or `--in-place`.
`nbops new` defaults `kernelspec.display_name` to `Python 3`.

## Kickoff artifact

`nbops-generalization-codex-kickoff-context-20260822` was not found in this
repository, sibling Wyatt clones under `/tmp/research` (`nbadb`, `proxywhirl`,
`riso`, `agents`, `prompts`, `dotfiles`, `template`), public GitHub search
(empty), gists (API 404), Drive/Gmail/Linear/Tavily (MCP `needsAuth`), sibling
nbops cloud-agent transcripts (role/text only), or this run's transcript
(filename only). Recovered TASK-001–023 live in `codex-kickoff-recovered.md`
and are **not** a substitute for the original dump.

## GitHub Actions

Run [32590811203](https://github.com/wyattowalsh/nbops/actions/runs/32590811203)
on `29abc7d` concluded **success** (all 5 jobs):

| Job | Result | Interpreter / notes |
| --- | ------ | ------------------- |
| `workflow-lint` | success | actionlint |
| `lint` | success | ruff check + format |
| `typecheck` | success | ty |
| `test (3.12)` | success | CPython **3.12.14**, **151 passed**, coverage **99.19%**; Compatibility smoke includes `python -m nbops version`, `nbops --version`, `nbops validate`, `nbops outputs`, `nbops batch validate examples`, `nbops serve --help` |
| `test (3.13)` | success | CPython **3.13.15**, **151 passed**, coverage **99.19%**; same Compatibility smoke |

Prior verified runs: [32590702886](https://github.com/wyattowalsh/nbops/actions/runs/32590702886) (`77e94a3`), [32590114562](https://github.com/wyattowalsh/nbops/actions/runs/32590114562) (`46cbd35`, 144 tests).
