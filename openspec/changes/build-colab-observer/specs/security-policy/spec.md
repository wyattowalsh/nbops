---
status: proposed
type: openspec-delta-spec
change: build-colab-observer
tags:
  - openspec
  - requirements
  - security-policy
updated: 2026-07-17
cssclasses:
  - planning-doc
---

# Delta spec: Security and policy boundary

## ADDED Requirements

### Requirement: Local-first and no telemetry by default
The package MUST operate without an account or hosted backend and MUST NOT transmit observations, reports, identifiers, or usage telemetry unless the user explicitly configures a documented integration.

#### Scenario: Default network observation
- GIVEN default configuration
- WHEN the observer runs and exports
- THEN it performs no product telemetry upload
- AND any subprocess or widget behavior is local or explicitly disclosed

### Requirement: Data minimization and redaction
Default collection and exports MUST omit secrets, environment values, notebook source, file contents, shell history, full process command lines, and unnecessary identity fields.

#### Scenario: Secret-like environment value
- GIVEN a runtime contains secret-like environment variables
- WHEN runtime metadata and reports are generated
- THEN variable values are absent
- AND the report does not enumerate sensitive names unless explicitly safe and necessary

### Requirement: Safe subprocess execution
Any external provider invocation MUST use a fixed executable, argument array, timeout, output-size bound, and strict parser without invoking a shell or interpolating user-controlled command text.

#### Scenario: Malformed provider output
- GIVEN an external provider returns malformed or unexpectedly large output
- WHEN it is parsed
- THEN the collector records a bounded error
- AND no command is retried indefinitely
- AND the observation run continues where safe

### Requirement: No runtime-extension behavior
The package, notebooks, docs examples, dashboard, and integrations MUST NOT automate activity, reconnection, keepalive, anti-idle, timeout bypass, quota circumvention, or resource-allocation manipulation.

#### Scenario: Policy audit
- GIVEN a release candidate
- WHEN policy checks and manual review inspect executable surfaces
- THEN no prohibited behavior is present
- AND the security docs explain the boundary without shipping executable bypass examples

### Requirement: Local frontend assets and bounded rendering
Runtime dashboard assets MUST be packaged or generated locally, and untrusted metric, process, path, or diagnostic text MUST be escaped before rendering into HTML or reports.

#### Scenario: Process name contains markup
- GIVEN a process name contains HTML-like text
- WHEN it appears in the dashboard or report
- THEN it is rendered as data rather than executable markup

### Requirement: Explicit sensitive opt-ins
Optional command-line capture, package inventories, third-party integrations, public endpoints, or expanded path reporting MUST require explicit configuration and MUST describe data exposure and disable/recovery behavior.

#### Scenario: Integration enabled
- GIVEN the user enables an external tracking integration
- WHEN observations are forwarded
- THEN the integration names the data fields and destination
- AND core local monitoring remains usable when the integration is disabled

### Requirement: Supply-chain and release integrity
Release artifacts MUST be built from reviewed locks and pinned automation, include provenance/checksum evidence where supported, and exclude secrets, caches, development-only files, and unreviewed executable assets.

#### Scenario: Wheel content audit
- GIVEN a release candidate wheel and source distribution
- WHEN artifact inspection runs
- THEN only intended package code, schemas, templates, licenses, and bundled dashboard assets are present
- AND no environment file, notebook output cache, or credential is included

### Requirement: Responsible vulnerability handling
The repository MUST publish a private security-reporting path and a supported-version policy without asking reporters to disclose sensitive vulnerability details publicly.

#### Scenario: Security report
- GIVEN a user discovers a potential vulnerability
- WHEN they consult repository guidance
- THEN they can identify a private reporting route and expected scope

### Requirement: Export path containment
All export operations MUST confine generated artifacts to the user-selected output location, even when stored identifiers or user-provided labels contain path syntax, reserved names, Unicode, control characters, or traversal segments.

#### Scenario: Opaque identifier attempts traversal
- GIVEN a persisted run identifier contains traversal or separator syntax
- WHEN reports or a portable bundle are generated
- THEN no file is created outside the selected output location
- AND the identifier is treated as data rather than an output path
- AND the exported metadata retains the original logical identifier for traceability

#### Scenario: Package-generated export root is a symbolic link
- GIVEN the package-generated export directory exists as a symbolic link to another location
- WHEN a report or portable bundle is requested
- THEN the operation fails before writing an artifact
- AND the symbolic-link target remains unchanged
- AND the configured output root remains the only allowed publication boundary

### Requirement: Local persistence path containment
The observer MUST reject pre-existing symbolic links, non-regular files, and hard-link aliases for its SQLite database or SQLite-managed sidecars before reading or mutating run evidence.

#### Scenario: Database path is a symbolic link
- GIVEN the configured database path is a symbolic link to an unrelated local database
- WHEN the observer starts persistence
- THEN startup fails with a bounded local error before adding or changing product schema
- AND the unrelated target remains unchanged

#### Scenario: SQLite sidecar path is an alias
- GIVEN a database sidecar path is a symbolic link, non-regular file, or hard-link alias
- WHEN persistence, query, backup, or export preflight inspects the run database
- THEN the operation fails without following the alias
- AND unrelated local content is neither modified nor represented as observer evidence

