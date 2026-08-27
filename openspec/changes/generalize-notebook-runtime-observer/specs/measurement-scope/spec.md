---
status: proposed
type: openspec-delta-spec
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - spec
  - measurement-scope
updated: 2026-08-22
cssclasses:
  - planning-doc
---


# Delta spec: measurement-scope

**Path:** `openspec/changes/generalize-notebook-runtime-observer/specs/measurement-scope/spec.md`  
**Purpose:** Observable behavior for the `measurement-scope` domain in the notebook-runtime generalization change.  
**Status:** Proposed

## ADDED Requirements

### Requirement: Explicit metric scope
**Trace ID:** `REQ-SCP-001`  
The system MUST identify the observable scope of each metric family or inherited profile default, including self process, process tree, kernel, container-visible, server-visible, host-visible, or unknown.

#### Scenario: Container-visible value is not called host-wide
- **GIVEN** a collector reads operating-system totals visible inside a container
- **WHEN** the value is displayed or exported
- **THEN** the resource scope is container-visible or unknown
- **AND** the value is not described as the physical host total

#### Scenario: Process-tree value remains distinct
- **GIVEN** process-tree evidence is collected
- **WHEN** the dashboard summarizes resource use
- **THEN** the summary labels the process-tree scope separately from system or container totals

### Requirement: Resource-limit provenance
**Trace ID:** `REQ-SCP-002`  
The system SHALL distinguish current usage from quotas or limits and preserve the evidence source for any reported limit.

#### Scenario: Missing limit is not unlimited
- **GIVEN** no cgroup, server, provider, or explicit limit evidence is available
- **WHEN** capacity information is rendered
- **THEN** the limit is unavailable or unknown
- **AND** the system does not claim unlimited capacity

#### Scenario: Limit source is retained
- **GIVEN** a cgroup or authenticated server source provides a limit
- **WHEN** the observation is exported
- **THEN** the limit source and applicable scope remain identifiable

### Requirement: Kernel and server boundary
**Trace ID:** `REQ-SCP-003`  
The system MUST NOT present kernel-local evidence as notebook-document, sibling-kernel, Jupyter Server, workspace, or host-wide evidence unless an authorized source directly supplies that scope.

#### Scenario: Kernel-only install remains kernel-scoped
- **GIVEN** the package runs only inside an IPython kernel
- **WHEN** no server integration is active
- **THEN** server and sibling-kernel metrics are unavailable
- **AND** the kernel-local observer remains usable

#### Scenario: Authorized server evidence is additive
- **GIVEN** an authenticated optional server provider supplies authorized server metrics
- **WHEN** the profile is composed
- **THEN** server-visible metrics are labeled separately from kernel metrics

## Notes
- These requirements describe observable behavior only.
- Internal classes, file paths, packages, registry mechanics, commands, and sequencing belong in design/tasks/planning docs.
