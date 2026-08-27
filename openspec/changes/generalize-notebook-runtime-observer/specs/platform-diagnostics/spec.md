---
status: proposed
type: openspec-delta-spec
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - spec
  - platform-diagnostics
updated: 2026-08-22
cssclasses:
  - planning-doc
---


# Delta spec: platform-diagnostics

**Path:** `openspec/changes/generalize-notebook-runtime-observer/specs/platform-diagnostics/spec.md`  
**Purpose:** Observable behavior for the `platform-diagnostics` domain in the notebook-runtime generalization change.  
**Status:** Proposed

## ADDED Requirements

### Requirement: Evidence-gated diagnostics
**Trace ID:** `REQ-DIA-001`  
Platform-specific diagnostics MUST activate only when their required profile facets, metric scope, freshness, and evidence quality are present.

#### Scenario: Drive warning requires Drive evidence
- **GIVEN** the runtime is not Colab or no Drive mount is detected
- **WHEN** diagnostics run
- **THEN** Drive-specific findings do not activate

#### Scenario: Object-backed storage warning is scoped
- **GIVEN** a storage profile identifies object-backed workspace storage and observed metadata latency exceeds the rule threshold
- **WHEN** diagnostics run
- **THEN** the finding names the applicable path class and evidence limitations

### Requirement: Platform guidance and alternatives
**Trace ID:** `REQ-DIA-002`  
Every platform-specific finding SHALL explain its evidence, scope, confidence, alternative causes, limitations, and non-destructive user action without claiming control over provider allocation or policy.

#### Scenario: Provider limitation is not overclaimed
- **GIVEN** GPU utilization is unavailable in a managed environment
- **WHEN** a diagnostic is generated
- **THEN** the finding describes unavailable telemetry and alternatives
- **AND** it does not infer no GPU use

#### Scenario: Generic copy replaces unsupported platform copy
- **GIVEN** a platform cannot be established confidently
- **WHEN** a relevant generic pressure rule activates
- **THEN** the message uses provider-neutral remediation

## Notes
- These requirements describe observable behavior only.
- Internal classes, file paths, packages, registry mechanics, commands, and sequencing belong in design/tasks/planning docs.
