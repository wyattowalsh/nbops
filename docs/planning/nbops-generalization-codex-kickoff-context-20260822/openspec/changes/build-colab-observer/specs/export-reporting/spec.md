---
status: proposed
type: openspec-delta-spec
change: build-colab-observer
tags:
  - openspec
  - requirements
  - export-reporting
updated: 2026-07-25
cssclasses:
  - planning-doc
---

# Delta spec: Export and reporting

## ADDED Requirements

### Requirement: Local multi-format export
The observer MUST export supported observations to CSV and JSONL, preserve a queryable local database, and generate Markdown and self-contained HTML reports without requiring network access.

#### Scenario: Offline export
- GIVEN a completed or running local observation run with network unavailable
- WHEN the user exports supported formats
- THEN local artifacts are created or a specific local error is returned
- AND no upload is attempted

### Requirement: Portable report bundle
The observer MUST create a zip bundle with a machine-readable manifest, checksums, schema/package versions, redaction status, run configuration, reports, and available data artifacts.

#### Scenario: Bundle verification
- GIVEN a created bundle
- WHEN its manifest and checksum file are validated
- THEN every declared artifact is present and hash-matched
- AND the bundle identifies omitted or partial artifacts

### Requirement: Redacted-by-default output
Exports MUST exclude secrets, environment values, notebook content, full command lines, and disallowed path details by default, and MUST record which optional sensitive fields were enabled.

#### Scenario: Export preview
- GIVEN an export includes an opt-in field with privacy impact
- WHEN the user requests bundle creation
- THEN the export summary identifies the field category and redaction mode
- AND the artifact does not silently include unapproved sensitive data

### Requirement: Partial-failure integrity
A failure while creating one output MUST NOT corrupt already persisted observations or cause the system to claim a complete bundle.

#### Scenario: HTML generation fails
- GIVEN tabular data and the database are valid but HTML report generation fails
- WHEN bundle creation completes
- THEN the bundle is labeled partial
- AND the manifest names the HTML failure
- AND valid data artifacts remain accessible

### Requirement: Stable schema and compatibility metadata
Every exported artifact MUST identify its schema version and the producing package version, and incompatible readers MUST fail with an actionable message rather than silently reinterpret data.

#### Scenario: Newer schema opened by older reader
- GIVEN an older reader encounters a newer unsupported schema
- WHEN it attempts to parse the artifact
- THEN it reports the unsupported version and recommended upgrade path

### Requirement: Bounded export size controls
Users MUST be able to select time ranges, process detail, and optional raw artifacts for export and MUST receive an estimate or warning before creating unusually large bundles.

#### Scenario: Large raw history
- GIVEN a long observation run exceeds the configured bundle warning threshold
- WHEN the user requests a full raw bundle
- THEN the observer communicates expected size or a bounded estimate
- AND offers a time-range or summary-only alternative

#### Scenario: Requested elapsed range exceeds representable time
- GIVEN an elapsed-time filter would overflow the supported timestamp or persistence domain
- WHEN an export query is resolved
- THEN the query is rejected before any artifact is written
- AND the existing run database and prior completed artifacts remain unchanged

### Requirement: Filesystem-safe artifact naming
The observer MUST treat run identifiers as opaque data and MUST NOT interpret them as filesystem paths when creating reports, directories, databases, or bundle names.

#### Scenario: Run identifier contains path syntax
- GIVEN a valid persisted run whose identifier contains path separators, traversal segments, reserved names, or other unsafe filename syntax
- WHEN the user exports that run to a selected output directory
- THEN every created artifact remains inside the selected output directory
- AND each artifact uses a deterministic single-segment filesystem name
- AND the original logical run identifier remains unchanged in the artifact metadata

#### Scenario: Existing safe run identifier
- GIVEN a run identifier that is already safe as a single filesystem segment
- WHEN artifacts are exported
- THEN the exported metadata preserves the identifier exactly
- AND repeated exports derive the same artifact name

#### Scenario: Generated run directory is a path alias
- GIVEN the selected export root contains a pre-existing generated run path that is a symbolic link or non-directory collision
- WHEN a report or tabular export begins
- THEN the export is rejected before writing any artifact through that path
- AND the external alias target remains unchanged

### Requirement: Atomic artifact publication
The observer MUST publish each final export atomically where the active filesystem permits and MUST clean up temporary or partial artifacts after publication failure.

#### Scenario: Final rename or copy fails
- GIVEN an export has been staged successfully
- WHEN publication of the final artifact fails
- THEN no incomplete final artifact is reported as successful
- AND temporary or partial artifacts created by that attempt are removed where safe
- AND an existing valid destination artifact is not silently corrupted

#### Scenario: Pre-existing partial path is a symbolic link
- GIVEN an untrusted process pre-creates a conventional partial-publication path as a symbolic link to an unrelated file
- WHEN a portable bundle is published
- THEN publication uses an attempt-owned temporary artifact rather than following the pre-existing link
- AND the unrelated target remains unchanged

### Requirement: Offline schema identity
Public export schemas MUST use stable identifiers that can be recognized and compared without requiring network resolution or implying ownership of an external web domain.

#### Scenario: Schema inspected offline
- GIVEN a report or bundle is opened without network access
- WHEN a reader inspects the declared schema identifier and version
- THEN the reader can identify the schema family and version without fetching a remote resource
- AND compatibility decisions remain based on the bundled schema and declared version

