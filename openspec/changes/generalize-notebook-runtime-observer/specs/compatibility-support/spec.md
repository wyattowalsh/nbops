---
status: proposed
type: openspec-delta-spec
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - spec
  - compatibility-support
updated: 2026-08-22
cssclasses:
  - planning-doc
---


# Delta spec: compatibility-support

**Path:** `openspec/changes/generalize-notebook-runtime-observer/specs/compatibility-support/spec.md`  
**Purpose:** Observable behavior for the `compatibility-support` domain in the notebook-runtime generalization change.  
**Status:** Proposed

## ADDED Requirements

### Requirement: Evidence-backed support tiers
**Trace ID:** `REQ-SUP-001`  
The system MUST assign a support tier to each platform and transport from captured representative evidence rather than product priority or detection alone.

#### Scenario: Detected platform is not automatically supported
- **GIVEN** a Deepnote or Jupyter signal is detected
- **WHEN** no representative smoke evidence is registered
- **THEN** the support tier remains unverified or preview

#### Scenario: Support evidence is inspectable
- **GIVEN** a platform is labeled validated
- **WHEN** the support record is inspected
- **THEN** runtime, package, display, persistence, failure, and accessibility evidence identifiers are available

### Requirement: Promotion and downgrade gates
**Trace ID:** `REQ-SUP-002`  
A support tier SHALL be promoted only when its defined evidence matrix passes and SHALL be downgraded or blocked when required evidence becomes stale or fails.

#### Scenario: Promotion requires all mandatory gates
- **GIVEN** a platform passes import and basic display only
- **WHEN** the support matrix still lacks persistence or export evidence
- **THEN** the platform is not promoted to validated

#### Scenario: Stale evidence is visible
- **GIVEN** a platform runtime changes beyond the recorded recheck trigger
- **WHEN** support metadata is generated
- **THEN** the tier is marked stale, blocked, or due for revalidation

### Requirement: Truthful platform fallback
**Trace ID:** `REQ-SUP-003`  
A platform-specific capability failure MUST degrade to the strongest validated generic capability without relabeling the platform as fully supported.

#### Scenario: Deepnote-specific profile fails
- **GIVEN** Deepnote detection succeeds but its storage-profile probe fails
- **WHEN** observation starts
- **THEN** generic Python/IPython behavior remains available
- **AND** the Deepnote capability is degraded and explained

#### Scenario: Jupyter server provider absent
- **GIVEN** a Jupyter frontend is used without a server extension
- **WHEN** the monitor runs
- **THEN** kernel-local static support continues
- **AND** server-wide metrics remain unavailable

## Notes
- These requirements describe observable behavior only.
- Internal classes, file paths, packages, registry mechanics, commands, and sequencing belong in design/tasks/planning docs.
