# Changelog

All notable changes to this project are documented in this file.

## 0.2.0 — 2026-08-22

General notebook operations toolkit (library, Typer CLI, FastAPI).

- Inspect, lint (`NB000`–`NB011`), clean, transform, convert, diff, batch
- Output inventory (`nbops outputs` / `POST /notebooks/outputs`)
- nbformat schema validation (`nbops validate` / `POST /notebooks/validate`)
- Directory batch: `nbops batch {stats,lint,clean,validate}` (fail-closed on errors)
- Percent-format roundtrip (`nbops convert --to py` / `nbops from-py`), including cell tags
  (`[md]` is accepted as markdown; tags with `]` inside quotes round-trip), cell ids
  (header `id=`; omitted ids stay omitted), and Jupytext optional cell titles
- Concatenation uniquifies duplicate present cell ids and leaves omitted ids omitted
- Tag CLI/API can add or remove cell tags
- Optional `nbops[execute]` extra (nbclient)
- Compatibility with the stats-only scaffold: `compute_stats`, `nbops stats`,
  `POST /notebooks/stats`
- Operations catalog (`nbops ops`, `GET /operations`)
- `NBOPS_` environment settings (optional working-directory `.env`; see `.env.example`)
- CLI `--version` and `python -m nbops`
- CLI `--strip-metadata` for extra cell metadata keys (`CleanOptions.metadata_keys`)
- `clean_notebook` strips notebook-level `metadata.widgets` when stripping outputs
- System command `nbops serve` (`--host`, `--port`, `--reload`); `just api` uses it
- `nbops kernel` and `nbops exec` require `--output` or `--in-place` (no implicit overwrite)
- Wyatt baseline `.editorconfig` and OpenSpec `openspec/config.yaml`
- `nbops new` defaults kernelspec display name to `Python 3` (optional `--display-name`)
- `from_percent_python` applies Jupytext YAML `kernelspec` when `name` is present
- Output-linked cell metadata (`collapsed`, `scrolled`, `ExecuteTime`) is stripped only with outputs
- Load/save/execute preserve omitted v4 cell ids (`NB009` / `clean --strip-ids` survive a roundtrip)
- `load_notebook` stays schema-lenient by default, matching the original stats scaffold
- Demo notebook contract tests (`examples/demo.ipynb`) and `just quality-gates` / `just smoke`
- Original scaffold API start remains documented: `uvicorn nbops.api:app` plus curl
  `GET /health` and `POST /notebooks/stats`
- `nbops stats` reports invalid JSON through the same fail-closed CLI error path as
  inspect/validate (no unhandled traceback)
- Original `GET /health` still constructs `HealthResponse()` with `status="ok"` and
  the installed package version as the default
- `POST /notebooks/stats` keeps the original OpenAPI request name `StatsRequest`
- GitHub labels referenced by Dependabot and `.github/release.yml` are catalogued in
  `.github/labels.yml`
- Original README interactive-docs sentence (`/docs`) and OpenAPI `HealthResponse`
  defaults remain the stats-scaffold contract
- `StatsRequest.notebook` keeps the original nbformat v4 field description
- Pytest ignores Starlette's TestClient `httpx`/`httpx2` UserWarning so CI logs stay clean
- Original shipped demo (`language_info.version` 3.12, omitted cell ids) is a fixture;
  live `uvicorn nbops.api:app` is tested for `GET /health` and `POST /notebooks/stats`
- Frozen original stats-scaffold pytest suite under `tests/original_scaffold/`
- Dependabot uses the `uv` ecosystem so `uv.lock` is updated with `pyproject.toml`
- `execute_notebook` restores omitted v4 cell ids after the nbclient roundtrip so
  lint `NB009` remains observable
- `concat_notebooks` no longer fills omitted cell ids (explicit `nbops ids` does)
- `nbops batch lint` honors `NBOPS_MAX_OUTPUT_CHARS` like `nbops lint` and HTTP lint
- Percent convert emits/parses Jupytext `id=` cell headers; `from-py` does not assign missing ids
- Percent convert parses Jupytext optional cell titles (`# %% Title [markdown]`) and round-trips `metadata.title`
- Percent convert emits/parses Jupytext cell metadata beyond `id`/`tags`/`title`
  (`key=value` pairs and JSON objects, including dotted keys and `collapsed`/`slideshow`)
- Percent convert emits Jupytext `kernelspec` YAML so convert→from-py keeps kernel
  name, display name, and language
- `NB007` and `extract_imports` parse IPython line magics, shell bangs, help suffixes,
  assignment magics, and top-level `await` (accepted by Python 3.12+ `ast.parse`);
  non-Python cell magics and non-Python kernels (for example `ir` / `R`) are skipped
  instead of being treated as invalid Python
- `convert --to script` / `to_script` strips those IPython magics (and omits non-Python
  cell magics) so the emitted file is parseable Python; percent format still keeps magics
- Markdown conversion fences code cells with the declared or inferred language (`r` for
  `ir`, `julia` for `julia-*`); kernelspec names `ir` / `julia*` / `rust` are treated as
  non-Python when language fields are omitted
- Percent convert infers missing kernelspec language from well-known names (`ir` → `r`),
  round-trips `language_info.name` when there is no kernelspec name, and does not let a
  default Python `language_info` hide a non-Python kernelspec name
- `compute_stats` / `nbops stats` report that same inferred language (so `ir` is `r`,
  not a leftover `python`)
- Percent convert round-trips nbformat cell `attachments` as header JSON and restores
  them on the cell, not in `metadata`
- Markdown conversion (`to_markdown` / `convert --to md`) inlines `attachment:` and
  `attachment://` links as `data:` URIs from cell attachments
- Markdown conversion also inlines code-cell `image/*` display/execute outputs as
  `data:` images after the fenced source
