---
status: proposed
type: openspec-delta-spec
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - spec
  - runtime-profiles
updated: 2026-08-22
cssclasses:
  - planning-doc
---


# Delta spec: runtime-profiles

**Path:** `openspec/changes/generalize-notebook-runtime-observer/specs/runtime-profiles/spec.md`  
**Purpose:** Observable behavior for the `runtime-profiles` domain in the notebook-runtime generalization change.  
**Status:** Proposed

## ADDED Requirements

### Requirement: Versioned runtime profile
**Trace ID:** `REQ-RTP-001`  
The system MUST produce a versioned runtime profile that separately represents provider, frontend, kernel, execution scope, resource scope, limit provenance, storage capabilities, display transports, support tier, evidence, and limitations.

#### Scenario: Profile is composed from available evidence
- **GIVEN** a Python runtime starts observation
- **WHEN** the runtime profile is generated
- **THEN** the profile exposes each supported facet independently
- **AND** an unknown facet remains explicitly unknown rather than inferred from another facet

#### Scenario: Profile survives portable export
- **GIVEN** a run is exported for later diagnosis
- **WHEN** the report or bundle is opened outside the originating notebook
- **THEN** the profile schema version, evidence summary, support tier, and limitations remain available

### Requirement: Detection evidence and conflicts
**Trace ID:** `REQ-RTP-002`  
The system SHALL preserve bounded detection evidence, confidence, and conflicts without exporting sensitive raw values or silently choosing between contradictory high-confidence claims.

#### Scenario: Conflicting evidence remains visible
- **GIVEN** two detectors produce contradictory high-confidence claims for the same facet
- **WHEN** the runtime profile is resolved
- **THEN** both claims are retained as a conflict
- **AND** the affected facet is not presented as certain

#### Scenario: Sensitive raw evidence is minimized
- **GIVEN** a detector observes a value that may contain an account, workspace, host, path, or credential identifier
- **WHEN** profile evidence is serialized
- **THEN** only an allowlisted bounded classification or redacted value is retained

### Requirement: Generic fallback profile
**Trace ID:** `REQ-RTP-003`  
The system MUST provide a generic Python runtime profile when no provider-specific environment can be established.

#### Scenario: Unknown notebook provider does not block observation
- **GIVEN** the package runs in a Python process with no recognized provider
- **WHEN** observation starts
- **THEN** core collection, persistence, text output, reports, and exports remain usable

#### Scenario: IPython does not imply a hosted provider
- **GIVEN** an IPython display capability is present without provider evidence
- **WHEN** the profile is generated
- **THEN** IPython display is represented independently
- **AND** the provider remains generic or unknown

## Notes
- These requirements describe observable behavior only.
- Internal classes, file paths, packages, registry mechanics, commands, and sequencing belong in design/tasks/planning docs.
