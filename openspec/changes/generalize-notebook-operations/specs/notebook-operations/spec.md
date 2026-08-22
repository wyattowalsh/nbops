## ADDED Requirements

### Requirement: Notebook operations library

The project SHALL provide a domain-general Jupyter notebook operations library
under `src/nbops/` covering I/O, inspect, lint, clean, transform, convert, diff,
batch, and optional execute.

#### Scenario: Stats compatibility

- **WHEN** a caller invokes `compute_stats`, `nbops stats`, or `POST /notebooks/stats`
- **THEN** the original stats-only scaffold contract remains available

### Requirement: Lint catalog

The library SHALL emit structural findings using codes `NB000` through `NB011`
as defined in `nbops.lint.ISSUE_CATALOG`.

#### Scenario: Missing cell id

- **WHEN** a cell has no string `id`
- **THEN** lint reports `NB009`

### Requirement: Shared operations catalog

Library, CLI, and HTTP surfaces SHALL be inventoried in `nbops.operations.OPERATIONS`,
exposed as `nbops ops` and `GET /operations`. Every catalog `cli` value SHALL exist on
the Typer app, and every catalog `api` value SHALL exist on the FastAPI app.

#### Scenario: Catalog listing

- **WHEN** a caller requests the catalog
- **THEN** every implemented operation includes its library path and CLI/API names
  and those names resolve on the live CLI and HTTP surfaces
