---
status: proposed
type: openspec-delta-spec
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - spec
  - notebook-display
updated: 2026-08-22
cssclasses:
  - planning-doc
---


# Delta spec: notebook-display

**Path:** `openspec/changes/generalize-notebook-runtime-observer/specs/notebook-display/spec.md`  
**Purpose:** Observable behavior for the `notebook-display` domain in the notebook-runtime generalization change.  
**Status:** Proposed

## ADDED Requirements

### Requirement: Universal static baseline
**Trace ID:** `REQ-DSP-001`  
The system MUST provide text and semantic script-free static output that remains usable when JavaScript, comms, widgets, server extensions, or provider-specific APIs are unavailable.

#### Scenario: Unknown frontend remains usable
- **GIVEN** no supported rich frontend is detected
- **WHEN** display is requested
- **THEN** a text snapshot is produced without crashing

#### Scenario: Compatible IPython renders static output
- **GIVEN** an IPython frontend accepts rich display
- **WHEN** display is requested
- **THEN** semantic static HTML/SVG/tables are emitted without remote assets

### Requirement: Capability-negotiated transport
**Trace ID:** `REQ-DSP-002`  
Enhanced display transport MUST be selected only from directly available, user-approved capabilities and MUST fall back without changing observation correctness.

#### Scenario: Unavailable enhanced transport falls back
- **GIVEN** a requested comm or widget transport is unavailable
- **WHEN** display activates
- **THEN** the static baseline remains usable
- **AND** observation and export continue

#### Scenario: Experimental transport is explicit
- **GIVEN** a transport lacks representative platform evidence
- **WHEN** the capability is exposed
- **THEN** it is labeled experimental and is not activated by default

### Requirement: Semantic parity across transports
**Trace ID:** `REQ-DSP-003`  
Every promoted chart or interactive view MUST retain an equivalent human-readable summary, semantic table, and export path.

#### Scenario: Chart failure preserves data access
- **GIVEN** a chart transport fails after observations exist
- **WHEN** the user views the monitor
- **THEN** the summary and table remain available
- **AND** the same range can be exported

#### Scenario: Transport does not change metric meaning
- **GIVEN** the same snapshot is shown in static and enhanced surfaces
- **WHEN** the values are compared
- **THEN** units, scope, quality, unavailable states, and limitations agree

## Notes
- These requirements describe observable behavior only.
- Internal classes, file paths, packages, registry mechanics, commands, and sequencing belong in design/tasks/planning docs.
