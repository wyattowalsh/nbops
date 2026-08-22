# notebook-operations Specification

## Purpose

Domain-general Jupyter notebook operations: I/O, inspect, lint, clean,
transform, convert, diff, batch, CLI, and HTTP API, with optional execute.
`compute_stats` / `nbops stats` / `POST /notebooks/stats` remain the
stats-scaffold compatibility surface.

The change `generalize-notebook-operations` stays open until the original
dump `nbops-generalization-codex-kickoff-context-20260822` can be applied.

## Requirements

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
- **WHEN** a reader follows the README HTTP quickstart
- **THEN** both `nbops serve` and `uvicorn nbops.api:app` are documented, along with
  curl examples for `GET /health` and `POST /notebooks/stats`
- **WHEN** `nbops stats` prints a table for the original stats-scaffold fixture
- **THEN** the original seven rows are present (total/code/markdown/raw cells, code
  lines, kernel, language) and the output includes the `Notebook:` path prefix
- **WHEN** a caller constructs `HealthResponse()` with no arguments, or `GET /health`
  returns its body
- **THEN** `status` is `ok` and `version` is the installed package version
- **WHEN** a client reads the OpenAPI schema for `POST /notebooks/stats`
- **THEN** the request body model is named `StatsRequest` and its `notebook`
  field description is the original stats-scaffold text
- **WHEN** a caller opens `/docs`
- **THEN** FastAPI serves the interactive API documentation advertised in the README
- **WHEN** the original shipped `examples/demo.ipynb` from the stats scaffold is loaded
  and saved
- **THEN** omitted cell ids stay omitted, `language_info.version` remains `3.12`, and
  stats remain 4/2/4
- **WHEN** `uvicorn nbops.api:app` is started as in the original README
- **THEN** `GET /health` and `POST /notebooks/stats` succeed against the live process

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
nbformat schema. Concatenation SHALL uniquify duplicate *present* cell ids and
SHALL leave omitted ids omitted.

#### Scenario: Output inventory

- **WHEN** a caller invokes `list_outputs`, `nbops outputs`, or `POST /notebooks/outputs`
- **THEN** each code-cell output is returned with cell index, type, and size

#### Scenario: Schema validation

- **WHEN** a caller invokes `validate_notebook`, `nbops validate`, or
  `POST /notebooks/validate`
- **THEN** valid notebooks report success and invalid documents report an error

### Requirement: Percent-format tags and widget residue

Percent-format conversion SHALL round-trip cell tags, optional titles, present
cell ids, nbformat cell `attachments`, and other JSON-serializable cell metadata
encoded as `key=value` or a JSON object. Omitted cell ids SHALL stay omitted.
Cleaning outputs SHALL remove notebook-level widget state.

#### Scenario: Percent tag roundtrip

- **WHEN** a notebook with cell `metadata.tags` is converted to percent Python and back
- **THEN** the restored cells keep those tags

#### Scenario: Percent attachments roundtrip

- **WHEN** a markdown or raw cell has nbformat `attachments`
- **THEN** convert→from-py restores those attachments on the cell, not in `metadata`
- **WHEN** `attachments` is empty or absent
- **THEN** percent output does not include an `attachments=` header

#### Scenario: Percent generic metadata roundtrip

- **WHEN** a notebook cell has `collapsed`, `slideshow`, or other JSON-serializable
  metadata and is converted to percent Python and back
- **THEN** those metadata keys are restored and omitted cell ids stay omitted
- **WHEN** a percent header carries a JSON metadata object
- **THEN** `from_percent_python` restores those fields onto the cell

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
leading Jupytext `# ---` YAML header when `name` is present. When kernelspec language
is omitted, language SHALL be inferred from well-known names (`ir` → `r`) or from
`language_info.name`. `to_percent_python` SHALL emit that header when the notebook
has a kernelspec name, including an inferred language when the stored language is
missing, and SHALL emit `language_info.name` when there is no kernelspec name.

#### Scenario: Percent script kernelspec

- **WHEN** a percent script includes a Jupytext header with `kernelspec.name`
- **THEN** the restored notebook metadata uses that kernelspec
- **WHEN** a notebook with a named kernelspec is converted to percent Python and back
- **THEN** kernel name, display name, and language are restored
- **WHEN** a notebook has kernelspec name `ir` and omits language fields
- **THEN** convert→from-py restores `language` / `language_info.name` as `r`
- **WHEN** a notebook has only `language_info.name` and no kernelspec name
- **THEN** percent convert emits `language_info` YAML and from-py restores that name

### Requirement: New notebook display name

`nbops new` SHALL default the kernelspec display name to `Python 3` for `python3`,
matching `new_notebook` and `POST /notebooks/new`.

#### Scenario: CLI new display name

- **WHEN** a caller runs `nbops new path.ipynb` with the default kernel
- **THEN** the written notebook has `metadata.kernelspec.display_name` of `Python 3`

### Requirement: Id-preserving I/O

Load, save, and execute SHALL preserve omitted cell ids on nbformat 4 documents
so lint `NB009` and `clean` with `cell_ids=True` remain observable after a
roundtrip. Pre-v4 documents MAY be upgraded to v4. `nbformat` MAY insert ids
while talking to a kernel; the returned execute document SHALL restore omitted
ids by cell index.

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
- **WHEN** `execute_notebook` runs on a v4 document whose cells omit `id`
- **THEN** the returned cells still omit `id` and lint still reports `NB009`

### Requirement: Demo notebook contract

`examples/demo.ipynb` SHALL remain a valid nbformat v4.5 compatibility fixture:
four cells (markdown, code, code, markdown), stats 4/2/4, kernel display name
`Python 3`, and a `demo` tag on the first code cell.

#### Scenario: Demo layout

- **WHEN** the demo notebook is loaded and validated
- **THEN** cell ids are `title`, `area`, `print-area`, `done` and stats remain 4/2/4

### Requirement: Python-aware code parsing

`NB007` and `extract_imports` SHALL parse Python notebook code through
IPython-aware magics stripping, skip non-Python cell magics, and skip Python
AST checks when the notebook declares a non-Python language. Missing language
metadata SHALL keep the historical Python behavior, except that kernelspec names
`python*`, `ir`, `julia*`, and `rust` SHALL be inferred when language fields are
omitted. Top-level `await` is valid on the supported Python 3.12+ parsers.
`to_script` / `convert --to script` SHALL strip those magics on Python notebooks
and omit non-Python cell magics so the emitted file is parseable Python.
Percent-format conversion SHALL keep magics in cell source. Markdown conversion
SHALL fence code cells with the declared or inferred language id.

#### Scenario: IPython magics are not syntax errors

- **WHEN** a Python code cell starts with `%matplotlib inline` or uses top-level `await`
- **THEN** lint does not report `NB007` and `extract_imports` still finds following imports
- **WHEN** a code cell is a non-Python cell magic such as `%%bash`
- **THEN** lint does not report `NB007` and that cell contributes no imports
- **WHEN** a notebook declares kernelspec/language `r`
- **THEN** lint does not report `NB007` for R source and `extract_imports` returns no records
- **WHEN** a notebook has kernelspec name `ir` and omits language fields
- **THEN** lint does not report `NB007` for R source
- **WHEN** `compute_stats` runs on that notebook
- **THEN** `language` is `r` even if `language_info.name` is a leftover `python`

#### Scenario: Script conversion strips IPython magics

- **WHEN** a Python notebook code cell starts with `%matplotlib inline` then `import os`
- **THEN** `to_script` / `convert --to script` emits parseable Python without the magic
- **WHEN** a code cell is a non-Python cell magic such as `%%bash`
- **THEN** that cell is omitted from the script
- **WHEN** the same notebook is converted to percent Python
- **THEN** the magics remain in the percent source
- **WHEN** a notebook has kernelspec name `ir`
- **THEN** Markdown code fences use `r` and script conversion leaves R source unchanged
