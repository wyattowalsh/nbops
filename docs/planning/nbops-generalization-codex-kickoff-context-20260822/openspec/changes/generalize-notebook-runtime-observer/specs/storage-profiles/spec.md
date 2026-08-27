---
status: proposed
type: openspec-delta-spec
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - spec
  - storage-profiles
updated: 2026-08-22
cssclasses:
  - planning-doc
---


# Delta spec: storage-profiles

**Path:** `openspec/changes/generalize-notebook-runtime-observer/specs/storage-profiles/spec.md`  
**Purpose:** Observable behavior for the `storage-profiles` domain in the notebook-runtime generalization change.  
**Status:** Proposed

## ADDED Requirements

### Requirement: Storage capability classification
**Trace ID:** `REQ-STO-001`  
The system MUST classify known output locations by persistence expectation, locality, performance posture, and confidence without promising durability it cannot verify.

#### Scenario: Ephemeral and persistent locations differ
- **GIVEN** a platform exposes both fast ephemeral storage and a persistent workspace location
- **WHEN** the profile is generated
- **THEN** the locations receive distinct storage classes and guidance

#### Scenario: Unknown storage remains unknown
- **GIVEN** no trustworthy platform or filesystem evidence establishes persistence
- **WHEN** an output path is assessed
- **THEN** persistence is unknown rather than assumed

### Requirement: Working and artifact destinations
**Trace ID:** `REQ-STO-002`  
The system SHALL support a bounded working destination for active sampling and a separate artifact destination for finalized reports or bundles while preserving legacy single-output behavior.

#### Scenario: High-frequency writes stay local when configured
- **GIVEN** a platform storage profile identifies object-backed persistence and fast ephemeral local storage
- **WHEN** the user selects automatic storage policy
- **THEN** active SQLite writes use the safe working destination
- **AND** final artifacts target the configured persistent destination only at explicit finalization

#### Scenario: Legacy output remains compatible
- **GIVEN** an existing notebook supplies only the legacy output directory
- **WHEN** observation starts
- **THEN** that directory retains its documented behavior without requiring new fields

### Requirement: No automatic mount or transfer authority
**Trace ID:** `REQ-STO-003`  
The system MUST NOT mount cloud storage, authenticate accounts, or silently copy artifacts between storage classes.

#### Scenario: Unmounted destination fails safely
- **GIVEN** a requested persistent destination requires an unavailable mount
- **WHEN** observation preflight runs
- **THEN** the system reports the exact blocker without mounting the storage

#### Scenario: Final copy is explicit
- **GIVEN** a working and artifact destination differ
- **WHEN** observation stops
- **THEN** copy or publication occurs only through an explicit export/finalization action
- **AND** partial failure remains visible

## Notes
- These requirements describe observable behavior only.
- Internal classes, file paths, packages, registry mechanics, commands, and sequencing belong in design/tasks/planning docs.
