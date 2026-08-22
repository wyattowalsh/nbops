# Changelog

All notable changes to this project are documented in this file.

## 0.2.0 — 2026-08-22

General notebook operations toolkit (library, Typer CLI, FastAPI).

- Inspect, lint (`NB000`–`NB011`), clean, transform, convert, diff, batch
- Optional `nbops[execute]` extra (nbclient)
- Compatibility with the stats-only scaffold: `compute_stats`, `nbops stats`,
  `POST /notebooks/stats`
- Operations catalog (`nbops ops`, `GET /operations`)
- `NBOPS_` environment settings
