# Validation report (2026-08-22)

Recorded on branch `cursor/nbops-generalization-673e`. Last fully GitHub-verified
SHA before this completeness revision is `46cbd35` (run
[32590114562](https://github.com/wyattowalsh/nbops/actions/runs/32590114562),
**144 passed** on CPython 3.12.14 and 3.13.15). This revision adds Jupytext
kernelspec application, `nbops new` display-name parity, and output-linked clean
keys; local/CI counts for the new HEAD are recorded after the gates run.

## Tooling

| Gate | Result |
| ---- | ------ |
| `uv sync --locked --group dev` | lockfile resolved; editable `nbops==0.2.0` |
| `uv run ruff check src tests` | pending on this HEAD (last green: `46cbd35`) |
| `uv run ruff format --check src tests` | pending on this HEAD |
| `uv run ty check` | pending on this HEAD |
| `uv run pytest` | last GitHub-verified: **144 passed**, coverage **98.87%** at `a9672fe`; `46cbd35` succeeded with the same 144-test suite |

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

Run [32590114562](https://github.com/wyattowalsh/nbops/actions/runs/32590114562)
on `46cbd35` concluded **success** (all 5 jobs). Prior verified run
[32589716713](https://github.com/wyattowalsh/nbops/actions/runs/32589716713) on
`a9672fe` reported **144 passed** on CPython **3.12.14** and **3.13.15**.
