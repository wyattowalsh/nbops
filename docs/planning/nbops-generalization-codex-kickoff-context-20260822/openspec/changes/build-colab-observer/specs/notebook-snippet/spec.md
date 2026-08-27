---
status: proposed
type: openspec-delta-spec
change: build-colab-observer
tags:
  - openspec
  - requirements
  - notebook-snippet
updated: 2026-07-17
cssclasses:
  - planning-doc
---

# Delta spec: Notebook snippet

## ADDED Requirements

### Requirement: Three-cell quickstart
The project MUST provide a copyable install/start cell, a display cell, and a stop/export cell that work together in a clean supported Colab runtime.

#### Scenario: Clean runtime quickstart
- GIVEN a new supported Colab notebook
- WHEN the user runs the documented three cells in order
- THEN an observation run starts
- AND the dashboard or accessible fallback appears
- AND stopping returns local export paths

### Requirement: Safe defaults and rerun behavior
The quickstart MUST use bounded sampling, local persistence, redacted collection, and deterministic rerun behavior.

#### Scenario: Start cell rerun
- GIVEN the quickstart start cell already created a live observer in the notebook namespace
- WHEN the user reruns the cell
- THEN the documented behavior prevents an unreported duplicate sampler
- AND the user receives the active or replacement run identity

### Requirement: Mounted output option
The snippet MUST support an explicit mounted-Drive output directory while remaining functional with local `/content` storage and without requiring Drive APIs.

#### Scenario: Drive not mounted
- GIVEN the configured mounted output path is unavailable
- WHEN the observer starts
- THEN it reports the output-path problem before writing
- AND the snippet provides a local-output recovery path
- AND it does not mount or authenticate Drive without user action

#### Scenario: Drive path contains dot segments
- GIVEN a configured output path lexically resolves beneath `/content/drive` through `.` or `..` segments
- AND Google Drive is not mounted
- WHEN output preflight classifies the path
- THEN the normalized path is treated as a mounted-Drive target
- AND the observer rejects it before creating files
- AND the user receives the same local-output recovery guidance as for a direct Drive path

### Requirement: UI activation disclosure
If enhanced display requires a Colab-specific widget activation step, the snippet MUST disclose that step, allow the user to decline it, and retain a local fallback.

#### Scenario: Widget activation declined
- GIVEN the current runtime requires widget activation
- WHEN the user disables or declines enhanced widget support
- THEN monitoring and persistence continue
- AND the output cell renders a semantic static summary and tables

### Requirement: Policy-safe behavior
The snippet MUST contain no keepalive, anti-idle, reconnect, timeout-bypass, hidden activity, or quota-circumvention logic.

#### Scenario: Safety scan
- GIVEN the distributed notebook and snippet source
- WHEN automated and manual safety checks inspect executable cells
- THEN no prohibited runtime-extension behavior is present
- AND safety documentation is allowed to name prohibited terms only to explain the boundary
