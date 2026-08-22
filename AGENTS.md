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
uv run nbops --version
uv run python -m nbops version
uv run nbops serve --host 0.0.0.0 --port 8000
# equivalent: uv run uvicorn nbops.api:app --host 0.0.0.0 --port 8000
just check
just quality-gates
# If just is not installed: uvx --from rust-just just quality-gates
```

Use `uv add` / `uv add --group dev` for dependencies. Do not hand-edit `uv.lock`.

## Conventions

- Package code lives in `src/nbops/` with absolute `nbops.*` imports.
- Unit tests mirror the package layout under `tests/`.
- Mock optional extras and kernels in unit tests; do not start Jupyter kernels
  in the default suite.
- Keep `compute_stats`, `nbops stats`, and `POST /notebooks/stats` as a
  compatibility surface for the original scaffold.
- `load_notebook` is schema-lenient by default (`validate=False`), matching the
  original scaffold's `json.loads` loader. Use `validate=True` or `nbops validate`
  for nbformat schema checks.
- Coverage gate is `--cov-fail-under=90`.
- Runtime settings use the `NBOPS_` prefix (`NBOPS_LOG_LEVEL`, `NBOPS_EXECUTE_TIMEOUT`,
  `NBOPS_MAX_OUTPUT_CHARS`, `NBOPS_PROGRESS`). See `.env.example`.
- Lint codes `NB000`–`NB011` are defined in `nbops.lint.ISSUE_CATALOG`.
- Inspect: stats, outline, imports, and output inventory (`nbops outputs` /
  `POST /notebooks/outputs`).
- Validate notebooks against the nbformat schema (`nbops validate` /
  `POST /notebooks/validate`).
- Directory batch operations: `nbops batch {stats,lint,clean,validate}`.
- The operations catalog (`nbops ops` / `GET /operations`) is the shared CLI/API inventory.
- Mutating CLI commands (`clean`, `filter`, `tag`, `ids`, `kernel`, `exec`)
  require `--output` or `--in-place` and do not overwrite the input by default.
- Load/save preserve omitted cell ids on v4 notebooks (`NB009`, `clean --strip-ids`).
- `nbops serve` and `nbops version` are system commands, not catalog operations.

## Out of scope unless explicitly requested

- Full nbconvert HTML/PDF pipelines
- JupyterHub / Binder orchestration
- Kaggle kernel publishing (that stays in nbadb)
- Undocumented notebook provider APIs
