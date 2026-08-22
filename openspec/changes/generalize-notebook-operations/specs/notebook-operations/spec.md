## ADDED Requirements

### Requirement: Notebook operations library

The project SHALL provide a domain-general Jupyter notebook operations library
under `src/nbops/` covering I/O, inspect, lint, clean, transform, convert, diff,
batch, and optional execute.

#### Scenario: Stats compatibility

- **WHEN** a caller invokes `compute_stats`, `nbops stats`, or `POST /notebooks/stats`
- **THEN** the original stats-only scaffold contract remains available
- **WHEN** a caller invokes `nbops.core.load_notebook(path)` on a v4 JSON notebook
  that would fail nbformat schema checks (for example a kernelspec without `name`)
- **THEN** the document loads and stats can still be computed

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
- **THEN** `metadata.widgets` is absent on the cleaned copy and present on the original
- **WHEN** `outputs=False`
- **THEN** widget state and output-linked cell keys (`collapsed`, `scrolled`, `ExecuteTime`) remain

### Requirement: Add or remove cell tags

The library SHALL add and remove cell tags on a chosen cell index.

#### Scenario: Tag add and remove

- **WHEN** a caller adds or removes cell tags via `add_tags` / `remove_tags`,
  `nbops tag`, or `POST /notebooks/tag`
- **THEN** the returned notebook has the requested tags present or absent on that cell

### Requirement: Jupytext percent kernelspec

`from_percent_python` SHALL apply `kernelspec` name, display name, and language from a
leading Jupytext `# ---` YAML header when `name` is present.

#### Scenario: Percent script kernelspec

- **WHEN** a percent script includes a Jupytext header with `kernelspec.name`
- **THEN** the restored notebook metadata uses that kernelspec

### Requirement: New notebook display name

`nbops new` SHALL default the kernelspec display name to `Python 3` for `python3`,
matching `new_notebook` and `POST /notebooks/new`.

#### Scenario: CLI new display name

- **WHEN** a caller runs `nbops new path.ipynb` with the default kernel
- **THEN** the written notebook has `metadata.kernelspec.display_name` of `Python 3`

### Requirement: Id-preserving I/O

Load and save SHALL preserve omitted cell ids on nbformat 4 documents so lint
`NB009` and `clean` with `cell_ids=True` remain observable after a roundtrip.
Pre-v4 documents MAY be upgraded to v4.

#### Scenario: Missing ids survive load and save

- **WHEN** a v4 notebook cell has no `id` and is loaded or saved with
  `validate=False`
- **THEN** the cell still has no `id`
- **WHEN** `nbops lint` is run on that file
- **THEN** it reports `NB009`
- **WHEN** `POST /notebooks/lint` is given that document
- **THEN** the report includes `NB009`
- **WHEN** `nbops clean --strip-ids` writes an output file
- **THEN** the written cells have no `id`
- **WHEN** `POST /notebooks/clean` is given `options.cell_ids=true`
- **THEN** the returned cells have no `id`

### Requirement: Demo notebook contract

`examples/demo.ipynb` SHALL remain a valid nbformat v4.5 compatibility fixture:
four cells (markdown, code, code, markdown), stats 4/2/4, kernel display name
`Python 3`, and a `demo` tag on the first code cell.

#### Scenario: Demo layout

- **WHEN** the demo notebook is loaded and validated
- **THEN** cell ids are `title`, `area`, `print-area`, `done` and stats remain 4/2/4
