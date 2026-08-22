# nbops — Agent Instructions

## Overview

`nbops` is a general Jupyter notebook operations toolkit: inspect, lint, clean,
transform, convert, diff, batch, CLI, and HTTP API. Optional execution lives
behind the `nbops[execute]` extra.

## Stack

- Python `>=3.12`, `uv`, hatchling
- Runtime: typer, fastapi, uvicorn, pydantic, loguru, nbformat, tenacity, tqdm
- Dev: pytest, pytest-cov, ruff, ty, httpx
- Type checker is `uv run ty check` (not mypy)

## Commands

```bash
uv sync
uv run ruff check src tests
uv run ruff format src tests
uv run ty check
uv run pytest
uv run nbops --help
uv run uvicorn nbops.api:app --host 0.0.0.0 --port 8000
```

Use `uv add` / `uv add --group dev` for dependencies. Do not hand-edit `uv.lock`.

## Conventions

- Package code lives in `src/nbops/` with absolute `nbops.*` imports.
- Unit tests mirror the package layout under `tests/`.
- Mock optional extras and kernels in unit tests; do not start Jupyter kernels
  in the default suite.
- Keep `compute_stats`, `nbops stats`, and `POST /notebooks/stats` as a
  compatibility surface for the original scaffold.
- Coverage gate is `--cov-fail-under=90`.
- Runtime settings use the `NBOPS_` prefix (`NBOPS_LOG_LEVEL`, `NBOPS_EXECUTE_TIMEOUT`).
- Lint codes `NB000`–`NB011` are defined in `nbops.lint.ISSUE_CATALOG`.
- The operations catalog (`nbops ops` / `GET /operations`) is the shared CLI/API inventory.

## Out of scope unless explicitly requested

- Full nbconvert HTML/PDF pipelines
- JupyterHub / Binder orchestration
- Kaggle kernel publishing (that stays in nbadb)
- Undocumented notebook provider APIs
