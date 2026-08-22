# Changelog

All notable changes to this project are documented in this file.

## 0.2.0 — 2026-08-22

General notebook operations toolkit (library, Typer CLI, FastAPI).

- Inspect, lint (`NB000`–`NB011`), clean, transform, convert, diff, batch
- Output inventory (`nbops outputs` / `POST /notebooks/outputs`)
- nbformat schema validation (`nbops validate` / `POST /notebooks/validate`)
- Directory batch: `nbops batch {stats,lint,clean,validate}` (fail-closed on errors)
- Percent-format roundtrip (`nbops convert --to py` / `nbops from-py`), including cell tags
  (`[md]` is accepted as markdown; tags with `]` inside quotes round-trip)
- Concatenation assigns unique cell ids
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
- Load/save preserve omitted v4 cell ids (`NB009` / `clean --strip-ids` survive a roundtrip)
- `load_notebook` stays schema-lenient by default, matching the original stats scaffold
- Demo notebook contract tests (`examples/demo.ipynb`) and `just quality-gates` / `just smoke`
