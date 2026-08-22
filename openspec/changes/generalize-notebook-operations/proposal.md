## Why

The repository was an empty MIT Python stub plus a stats-only environment
scaffold. Notebook operations need a general, tested toolkit rather than a
single statistics helper.

## What Changes

- Add a `src/nbops` operations library: I/O, inspect, clean, transform, lint,
  convert, diff, batch, optional execute.
- Expose the same operations through Typer and FastAPI.
- Add CI, agent docs, and a coverage-gated pytest suite.

## Impact

- Affected specs: notebook-operations library, CLI, HTTP API
- Affected code: `src/nbops/**`, `tests/**`, `.github/workflows/ci.yml`
