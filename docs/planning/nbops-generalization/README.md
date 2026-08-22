# Notebook operations generalization

The named artifact `nbops-generalization-codex-kickoff-context-20260822` was not
present in the GitHub `nbops` tree, Drive (unauthenticated in this environment),
Wyatt Walsh public repositories, gists (API 403/404), Linear/Gmail (MCP
unauthenticated), or prior nbops cloud-agent transcripts. This directory records
the exhaustive program derived from:

- the empty `main` tree (README / LICENSE / gitignore only)
- the `cursor/setup-dev-environment-a5a8` stats-only scaffold to generalize
- Wyatt conventions: `uv`, `ty`, `ruff`, `pytest`, Typer, FastAPI, Pydantic,
  Pydantic Settings, Loguru, Tenacity, tqdm
- nbadb/proxywhirl quality bar for a Python operations library

> [!IMPORTANT]
> Do not treat this recovered program as a substitute if the original kickoff
> file is later attached; rebase the remaining delta onto that document.

## Program

| ID | Requirement | Evidence |
| -- | ----------- | -------- |
| G1 | Domain-general notebook ops library (not NBA-specific, not stats-only) | `src/nbops/` package |
| G2 | Load/save/validate/new via nbformat | `src/nbops/io.py`; `nbops validate`; `POST /notebooks/validate` |
| G3 | Inspect: stats, outline, imports, outputs | `src/nbops/inspect.py`; CLI/API headings+imports+outputs |
| G4 | Clean outputs, counts, ids, empty cells | `src/nbops/clean.py` (widgets and output-linked cell keys stripped with outputs) |
| G5 | Transform: filter, concat, split, kernel, tags, cell ids | `src/nbops/transform.py` (`add_tags` / `remove_tags`) |
| G6 | Structural lint catalog NB000–NB011 | `src/nbops/lint.py` `ISSUE_CATALOG` |
| G7 | Convert to percent py, script, markdown, and percent roundtrip | `src/nbops/convert.py` (cell tags round-trip; `[md]` alias; Jupytext YAML kernelspec) |
| G8 | Cell-level diff | `src/nbops/diff.py` |
| G9 | Directory batch operations | `src/nbops/batch.py` + `nbops batch {stats,lint,clean,validate}` |
| G10 | Optional execute extra | `src/nbops/execute.py` + `[execute]` extra |
| G11 | Typer CLI covering every catalog operation | `src/nbops/cli.py`, `nbops ops` |
| G12 | FastAPI surface covering the operations | `src/nbops/api.py`, `GET /operations` |
| G13 | Compatibility with the stats scaffold | `src/nbops/core.py`, `stats`, `/notebooks/stats`; original seven-row CLI table; README `uvicorn nbops.api:app` and `/docs`; `HealthResponse()` defaults; OpenAPI `StatsRequest`; original shipped demo fixture; live uvicorn health/stats |
| G14 | Tests mirroring src, coverage gate | `tests/`, `--cov-fail-under=90` |
| G15 | Ruff + ty + pytest CI on 3.12/3.13 | `.github/workflows/ci.yml` |
| G16 | Agent/contributor docs | `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, `CODE_OF_CONDUCT.md` |
| G17 | uv lockfile and justfile | `uv.lock`, `justfile` (`check`, `quality-gates`, `smoke`) |
| G18 | Shared operations catalog | `src/nbops/operations.py` |
| G19 | Environment-backed settings (`NBOPS_`) | `src/nbops/settings.py`; `.env.example` |
| G20 | SECURITY.md | `SECURITY.md` |
| G21 | Dependabot for pip and GitHub Actions | `.github/dependabot.yml`; label names catalogued in `.github/labels.yml` |
| G22 | Pre-commit hooks + ruff | `.pre-commit-config.yaml` |
| G23 | Coverage gate 90% + actionlint CI | `pyproject.toml`, `.github/workflows/ci.yml` |

See [tasks.md](./tasks.md), [codex-kickoff-recovered.md](./codex-kickoff-recovered.md),
[validation.md](./validation.md), [validation-report.md](./validation-report.md),
and [audit.md](./audit.md).
