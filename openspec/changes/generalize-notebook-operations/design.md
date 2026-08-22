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
- Load/save/execute/concat of v4 notebooks preserve omitted cell ids; `nbformat`
  must not silently reinsert them on returned documents (that would hide `NB009`
  and undo `clean --strip-ids`). Concat uniquifies colliding present ids only.
  Percent convert emits/parses header `id=`, optional titles, other cell
  metadata (`key=value` or a JSON object), nbformat cell `attachments`, and a
  kernelspec YAML front matter
  (inferred language when omitted; `language_info.name` when there is no
  kernelspec name); `from-py` does not fill omitted ids.
  Markdown conversion inlines `attachment:` links as `data:` URIs and appends
  code-cell `image/*` outputs as Markdown images. Stream, error, and text
  outputs are included (indented / markdown) after fenced source.
  Optional Jupytext cell titles (`# %% Title [markdown]`) are parsed so the
  bracketed type is not dropped. The kernel client may see temporary ids internally.
- `NB007` / `extract_imports` parse Python as IPython notebook code (line magics,
  shell, help, assignment magics). Python 3.12+ `ast.parse` accepts top-level await.
  Non-Python cell magics and declared non-Python kernels are skipped. IPython is
  not a runtime dependency.
- Optional execution is an extra so the default install stays kernel-free
- Batch walks skip `.ipynb_checkpoints`
- Settings load from `NBOPS_*` environment variables via pydantic-settings

## Risks / Trade-offs

- The original Codex kickoff file was not available; rebase if it appears
- Execute depends on a local kernel and is mocked in the default test suite
