---
status: proposed
type: openspec-delta-spec
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - spec
  - platform-adapters
updated: 2026-08-22
cssclasses:
  - planning-doc
---


# Delta spec: platform-adapters

**Path:** `openspec/changes/generalize-notebook-runtime-observer/specs/platform-adapters/spec.md`  
**Purpose:** Observable behavior for the `platform-adapters` domain in the notebook-runtime generalization change.  
**Status:** Proposed

## ADDED Requirements

### Requirement: Capability composition
**Trace ID:** `REQ-ADP-001`  
The system SHALL compose runtime behavior from independent adapter evidence and capabilities instead of requiring one exclusive platform identity.

#### Scenario: Provider and frontend may differ
- **GIVEN** a Colab frontend connects to a locally controlled Jupyter runtime
- **WHEN** the profile is generated
- **THEN** frontend and execution-provider evidence can differ without collision

#### Scenario: Multiple adapters contribute safely
- **GIVEN** generic Python, IPython, and one provider detector all apply
- **WHEN** observation starts
- **THEN** their non-conflicting capabilities are composed deterministically

### Requirement: Adapter failure isolation
**Trace ID:** `REQ-ADP-002`  
The system MUST isolate adapter construction, detection, capability, collector, diagnostic, and cleanup failures so unrelated core behavior remains available.

#### Scenario: Broken provider detector does not abort
- **GIVEN** one provider detector raises or times out
- **WHEN** observation starts
- **THEN** the failure becomes bounded unavailable evidence
- **AND** generic collection and static output continue

#### Scenario: Cleanup failure is contained
- **GIVEN** an adapter cleanup step fails
- **WHEN** the observer stops
- **THEN** the failure is recorded without hiding other shutdown evidence

### Requirement: Passive detection
**Trace ID:** `REQ-ADP-003`  
Runtime and platform detection MUST NOT install packages, mount storage, change server configuration, call account APIs, allocate devices, restart kernels, or mutate notebook lifecycle.

#### Scenario: Detection is read-only
- **GIVEN** automatic profile detection runs
- **WHEN** the platform is unknown
- **THEN** the system returns a generic profile without attempting environment mutation

#### Scenario: Explicit platform override cannot fabricate scope
- **GIVEN** a user supplies a provider preference
- **WHEN** no direct evidence supports server or host scope
- **THEN** the preference may select behavior
- **AND** the system still reports unsupported scope as unknown

## Notes
- These requirements describe observable behavior only.
- Internal classes, file paths, packages, registry mechanics, commands, and sequencing belong in design/tasks/planning docs.
