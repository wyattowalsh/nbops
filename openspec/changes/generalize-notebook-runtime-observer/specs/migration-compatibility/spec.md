---
status: proposed
type: openspec-delta-spec
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - spec
  - migration-compatibility
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Delta spec: migration-compatibility

**Path:** `openspec/changes/generalize-notebook-runtime-observer/specs/migration-compatibility/spec.md`  
**Purpose:** Observable API, artifact, and provenance compatibility during the `nbops` migration.  
**Status:** Proposed

## ADDED Requirements

### Requirement: Canonical `nbops` API compatibility
**Trace ID:** `REQ-MIG-001`  
The change MUST preserve the supported observer lifecycle, configuration, diagnostics, display, report, and export behavior through the canonical `nbops` API unless a separately approved breaking change is introduced.

#### Scenario: Canonical three-cell notebook works
- **GIVEN** a user follows the current `nbops` notebook quickstart
- **WHEN** the generalized implementation is installed
- **THEN** the start, display, stop, report, and bundle flow works without an adapter argument

#### Scenario: Runtime profile is additive
- **GIVEN** a caller ignores runtime-profile metadata
- **WHEN** observation and export run
- **THEN** the supported lifecycle and return behavior remain usable

### Requirement: Legacy artifact compatibility
**Trace ID:** `REQ-MIG-002`  
Readers MUST continue to open supported prior run databases, reports, and bundles that lack runtime-profile fields and MUST represent absent new metadata as legacy or unknown.

#### Scenario: Prior bundle remains readable
- **GIVEN** a bundle from the pre-generalization schema is opened
- **WHEN** the `nbops` reader loads it
- **THEN** prior observations and reports remain available
- **AND** new profile fields are unknown rather than fabricated

#### Scenario: New artifact declares compatibility version
- **GIVEN** a generalized run is exported
- **WHEN** the artifact is inspected
- **THEN** schema versions, runtime scope, and compatibility limitations are explicit

### Requirement: Historical provenance remains stable
**Trace ID:** `REQ-MIG-003`  
The migration MUST preserve stable historical OpenSpec IDs and evidence paths while ensuring that new current product surfaces identify `nbops`.

#### Scenario: Historical change ID remains resolvable
- **WHEN** a reviewer follows a reference to `build-colab-observer`
- **THEN** the baseline proposal, tasks, and evidence remain resolvable
- **AND** the identifier is clearly treated as historical provenance

#### Scenario: New execution evidence uses `nbops`
- **WHEN** the migrated implementation produces a new report, bundle, package artifact, or notebook snippet
- **THEN** its current product identity is `nbops`
- **AND** any legacy metadata is explicitly labeled as legacy
