# Requirement audit (2026-08-22)

Authoritative current branch: `cursor/nbops-generalization-673e`.
HEAD at last local inspection is recorded in `validation-report.md`.

> [!IMPORTANT]
> The named dump `nbops-generalization-codex-kickoff-context-20260822` has **not**
> been found. Every G/TASK row below is the **recovered** program, not the
> original kickoff. Completion of the user objective remains **unproven**.

## Original named artifact

| Requirement | Evidence inspected | Status |
| ----------- | ------------------ | ------ |
| Execute every item in `nbops-generalization-codex-kickoff-context-20260822` | Filename only in the run transcript (`/goal … \` nbops-generalization-codex-kickoff-context-20260822 \``); schema is `role`/`text` with no attachment body. Absent from `/workspace`, GitHub `wyattowalsh/nbops` (`main` + feature branches), Wyatt public repo trees (`agents`, `prompts`, `nbadb`, `dotfiles`, `cwa`, `proxywhirl`, `riso`, `template`), gists (404), Drive/Gmail/Linear/Tavily MCP (`needsAuth`), `/tmp/research/*` clones, and all five nbops cloud-agent transcripts | **missing** |

## Recovered program (not a substitute)

| ID | Requirement | Evidence | Status |
| -- | ----------- | -------- | ------ |
| G1 / TASK-001 | Domain-general `src/nbops` package | `src/nbops/` modules; package name `nbops`; no NBA-specific code | verified (recovered) |
| G2 / TASK-002 | I/O load/save/validate/new | `src/nbops/io.py`; `nbops validate`; `POST /notebooks/validate`; `tests/test_io.py` | verified (recovered) |
| G3 / TASK-003 | Inspect stats/outline/imports/outputs | `list_outputs`; CLI/API `outputs`; inspect payload includes outputs | verified (recovered) |
| G4 / TASK-004 | Clean outputs/counts/ids/empty | `src/nbops/clean.py`; widgets and output-linked cell keys stripped with outputs; `tests/test_clean.py` | verified (recovered) |
| G5 / TASK-005 | Transform filter/concat/split/kernel/tags/ids | concat uniquifies cell ids; `add_tags` / `remove_tags`; `tests/test_transform.py` | verified (recovered) |
| G6 / TASK-006 | Lint NB000–NB011 | `ISSUE_CATALOG` length 12; tests cover NB000–NB011 | verified (recovered) |
| G7 / TASK-007 | Convert py/script/md + percent roundtrip | `to_percent_python` / `from_percent_python`; tags round-trip including `[md]` and bracket-safe lists; Jupytext YAML kernelspec | verified (recovered) |
| G8 / TASK-008 | Cell-level diff | `src/nbops/diff.py`; `tests/test_diff.py` | verified (recovered) |
| G9 / TASK-009 | Batch directory + tqdm | `src/nbops/batch.py`; `nbops batch {stats,lint,clean,validate}`; stats/clean fail-closed | verified (recovered) |
| G10 / TASK-010 | Optional execute extra | `pyproject.toml` `[execute]`; extra mocked in default tests | verified (recovered) |
| G11 / TASK-011 | Typer CLI for every catalog op | `test_catalog_cli_and_api_surfaces_exist` (20 ops); `nbops serve`/`version` are system commands | verified (recovered) |
| G12 / TASK-012 | FastAPI covering catalog + `GET /operations` | same invariant test | verified (recovered) |
| G13 / TASK-013 | Stats scaffold compatibility | demo 4/2/4 via CLI, library, HTTP, CI | verified (recovered) |
| G14 / TASK-014 | Tests mirroring src, coverage ≥90% | `tests/` mirrors modules plus `test_demo_notebook.py`; **155 passed**, **99.24%** | verified (recovered) |
| G15 / TASK-015 | CI ruff + ty + pytest 3.12/3.13 + actionlint | Run [32590811203](https://github.com/wyattowalsh/nbops/actions/runs/32590811203) on `29abc7d`: **151 passed**, **99.19%** on CPython **3.12.14** and **3.13.15**, including `nbops serve --help` | verified (recovered) |
| G16 / TASK-016 | AGENTS, CONTRIBUTING, README, CHANGELOG | plus `CODE_OF_CONDUCT.md`, `CLAUDE.md` → AGENTS.md, issue/PR templates, CODEOWNERS, FUNDING.yml, `.editorconfig`, `openspec/config.yaml` | verified (recovered) |
| G17 / TASK-017 | uv lockfile + justfile | `uv.lock`, `justfile` (`check`, `quality-gates`, `smoke`) | verified (recovered) |
| G18 / TASK-018 | Shared operations catalog | `src/nbops/operations.py`; **20** ops | verified (recovered) |
| G19 / TASK-019 | `NBOPS_` pydantic-settings | `src/nbops/settings.py`; `.env.example`; optional `.env`; `tests/test_settings.py` | verified (recovered) |
| G20 / TASK-020 | SECURITY.md | `SECURITY.md` | verified (recovered) |
| G21 / TASK-021 | Dependabot pip + github-actions | `.github/dependabot.yml` | verified (recovered) |
| G22 / TASK-022 | Pre-commit | `.pre-commit-config.yaml`; `uvx pre-commit run --all-files` passed | verified (recovered) |
| G23 / TASK-023 | Coverage 90 + actionlint + Ruff TCH | `--cov-fail-under=90`; actionlint CI job; ruff `select` includes `TCH` | verified (recovered) |

## Gates

| Gate | Local | GitHub |
| ---- | ----- | ------ |
| `uv sync --locked --group dev` | passed | passed in prior CI jobs |
| `uv run ruff check src tests` | passed | passed (`lint` job) |
| `uv run ruff format --check src tests` | passed | passed (`lint` job) |
| `uv run ty check` | passed | passed (`typecheck` job) |
| `uv run pytest` | 155 passed, 99.24% locally | last dual-interpreter GitHub proof 151 passed at `29abc7d` ([32590811203](https://github.com/wyattowalsh/nbops/actions/runs/32590811203)); demo-contract HEAD pending |
| `uv run nbops stats examples/demo.ipynb --json` | 4/2/4 | CI smoke on both interpreters |
| `uv run nbops validate examples/demo.ipynb` | `ok` | CI Compatibility smoke on 3.12.14 and 3.13.15 |
| `uv run nbops --version` / `python -m nbops version` | `0.2.0` | Compatibility smoke |
| `uv run nbops serve --help` | passed locally | Compatibility smoke on 3.12.14 and 3.13.15 |

## External

| Item | Status |
| ---- | ------ |
| Pull request into `main` | Not created (user settings block auto-PR). Compare: https://github.com/wyattowalsh/nbops/pull/new/cursor/nbops-generalization-673e |
| Drive/Gmail/Linear for original dump | MCP unauthenticated (`needsAuth`) |
