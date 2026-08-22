# Notebook operations generalization

The named artifact `nbops-generalization-codex-kickoff-context-20260822` was not
present in the GitHub `nbops` tree, Drive (unauthenticated in this environment),
or Wyatt Walsh public repositories. This directory records the exhaustive
program derived from:

- the empty `main` tree (README / LICENSE / gitignore only)
- the `cursor/setup-dev-environment-a5a8` stats-only scaffold to generalize
- Wyatt conventions: `uv`, `ty`, `ruff`, `pytest`, Typer, FastAPI, Pydantic, Loguru
- nbadb/proxywhirl quality bar for a Python operations library

## Program

| ID | Requirement | Evidence |
| -- | ----------- | -------- |
| G1 | Domain-general notebook ops library (not NBA-specific, not stats-only) | `src/nbops/` package |
| G2 | Load/save/validate/new via nbformat | `src/nbops/io.py` |
| G3 | Inspect: stats, outline, imports, outputs | `src/nbops/inspect.py` |
| G4 | Clean outputs, counts, ids, empty cells | `src/nbops/clean.py` |
| G5 | Transform: filter, concat, split, kernel, tags | `src/nbops/transform.py` |
| G6 | Structural lint with issue codes | `src/nbops/lint.py` |
| G7 | Convert to percent py, script, markdown | `src/nbops/convert.py` |
| G8 | Cell-level diff | `src/nbops/diff.py` |
| G9 | Directory batch operations | `src/nbops/batch.py` |
| G10 | Optional execute extra | `src/nbops/execute.py` + `[execute]` extra |
| G11 | Typer CLI covering the operations | `src/nbops/cli.py` |
| G12 | FastAPI surface covering the operations | `src/nbops/api.py` |
| G13 | Compatibility with the stats scaffold | `src/nbops/core.py`, `stats`, `/notebooks/stats` |
| G14 | Tests mirroring src, coverage gate | `tests/`, `--cov-fail-under=85` |
| G15 | Ruff + ty + pytest CI on 3.12/3.13 | `.github/workflows/ci.yml` |
| G16 | Agent/contributor docs | `AGENTS.md`, `CONTRIBUTING.md`, `README.md` |
| G17 | uv lockfile and justfile | `uv.lock`, `justfile` |

Do not treat this recovered program as a substitute if the original kickoff file
is later attached; rebase the remaining delta onto that document.
