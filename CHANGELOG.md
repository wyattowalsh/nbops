# Changelog

All notable changes to this project are documented in this file.

## 0.2.0 — 2026-08-22

General notebook operations toolkit (library, Typer CLI, FastAPI).

- Inspect, lint (`NB000`–`NB011`), clean, transform, convert, diff, batch
- Output inventory (`nbops outputs` / `POST /notebooks/outputs`)
- nbformat schema validation (`nbops validate` / `POST /notebooks/validate`)
- Directory batch: `nbops batch {stats,lint,clean,validate}` (fail-closed on errors)
- Percent-format roundtrip (`nbops convert --to py` / `nbops from-py`)
- Concatenation assigns unique cell ids
- Optional `nbops[execute]` extra (nbclient)
- Compatibility with the stats-only scaffold: `compute_stats`, `nbops stats`,
  `POST /notebooks/stats`
- Operations catalog (`nbops ops`, `GET /operations`)
- `NBOPS_` environment settings (optional working-directory `.env`; see `.env.example`)
- CLI `--version` and `python -m nbops`
- CLI `--strip-metadata` for extra cell metadata keys (`CleanOptions.metadata_keys`)
- System command `nbops serve` (`--host`, `--port`, `--reload`); `just api` uses it
- `nbops kernel` and `nbops exec` require `--output` or `--in-place` (no implicit overwrite)
