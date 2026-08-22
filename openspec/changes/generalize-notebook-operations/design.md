## Context

The repository started as an empty MIT Python stub. A sibling environment-setup
branch invented a stats-only CLI/API. This change generalizes that scaffold into
a domain-general notebook operations toolkit with one catalog driving library,
CLI, and HTTP surfaces.

## Goals / Non-Goals

**Goals**

- Inspect, lint, clean, transform, convert, diff, batch, and optional execute
- Preserve `compute_stats` / `nbops stats` / `POST /notebooks/stats`
- Wyatt Python contract: `uv`, `ruff`, `ty`, `pytest`, Typer, FastAPI, Loguru

**Non-Goals**

- Full nbconvert HTML/PDF pipelines
- JupyterHub / Binder orchestration
- Kaggle kernel publishing (stays in nbadb)

## Decisions

- nbformat v4.5 cell ids are linted (`NB009`) and repairable (`ensure_cell_ids`)
- Load/save/execute of v4 notebooks preserve omitted cell ids; `nbformat` must
  not silently reinsert them on returned documents (that would hide `NB009` and
  undo `clean --strip-ids`). The kernel client may see temporary ids internally.
- Optional execution is an extra so the default install stays kernel-free
- Batch walks skip `.ipynb_checkpoints`
- Settings load from `NBOPS_*` environment variables via pydantic-settings

## Risks / Trade-offs

- The original Codex kickoff file was not available; rebase if it appears
- Execute depends on a local kernel and is mocked in the default test suite
