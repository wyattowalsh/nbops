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

### Requirement: Inspect outputs and schema validate

The library SHALL inventory code-cell outputs and validate notebooks against the
nbformat schema. Concatenation SHALL assign unique cell ids when source notebooks
share ids.

#### Scenario: Output inventory

- **WHEN** a caller invokes `list_outputs`, `nbops outputs`, or `POST /notebooks/outputs`
- **THEN** each code-cell output is returned with cell index, type, and size

#### Scenario: Schema validation

- **WHEN** a caller invokes `validate_notebook`, `nbops validate`, or
  `POST /notebooks/validate`
- **THEN** valid notebooks report success and invalid documents report an error

### Requirement: Percent-format tags and widget residue

Percent-format conversion SHALL round-trip cell tags. Cleaning outputs SHALL
remove notebook-level widget state.

#### Scenario: Percent tag roundtrip

- **WHEN** a notebook with cell `metadata.tags` is converted to percent Python and back
- **THEN** the restored cells keep those tags

#### Scenario: Clean widget metadata

- **WHEN** `clean_notebook` runs with `outputs=True` on a notebook that has `metadata.widgets`
- **WHEN** a caller adds or removes cell tags via `add_tags` / `remove_tags`,
  `nbops tag`, or `POST /notebooks/tag`
- **THEN** the returned notebook has the requested tags present or absent on that cell
