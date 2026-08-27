---
status: proposed
type: openspec-delta-spec
change: build-colab-observer
tags:
  - openspec
  - requirements
  - diagnostics
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Delta spec: Diagnostics

## ADDED Requirements

### Requirement: Evidence-bearing findings
Every diagnostic finding MUST identify its rule, status, severity, confidence, activation duration, relevant evidence, limitations, and suggested next actions.

#### Scenario: Finding export
- GIVEN a diagnostic activates
- WHEN it appears in the dashboard or export
- THEN the same finding identifier and evidence window are present
- AND the user can determine why it activated

### Requirement: Stable activation and recovery
Diagnostic rules MUST use sustained evidence, separate activation and recovery conditions where appropriate, and cooldown or deduplication to avoid rapid alert flapping.

#### Scenario: Threshold oscillation
- GIVEN a metric oscillates around a rule threshold
- WHEN the rule evaluates repeated samples
- THEN it does not create a new warning for every crossing
- AND state changes are recorded only after the configured evidence condition is met

### Requirement: Common bottleneck coverage
The initial release MUST evaluate supported evidence for accelerator idle with CPU pressure, accelerator memory pressure, RAM pressure or sustained growth, disk pressure, mounted-Drive I/O risk, allocated-but-underused accelerator memory, top resource processes, checkpoint/storage growth, sampler lag, and degraded telemetry.

#### Scenario: GPU idle while CPU is saturated
- GIVEN sustained high CPU utilization and sustained low GPU utilization during an accelerator-enabled run
- WHEN sufficient valid samples exist
- THEN the observer may emit a likely input/preprocessing bottleneck finding
- AND it lists the evidence window and alternative explanations

### Requirement: Uncertainty-aware language
Diagnostics MUST NOT label an inferred cause as certain when the observations support only correlation or a heuristic.

#### Scenario: Possible memory leak
- GIVEN process memory grows over a configured evidence window
- WHEN no direct object-retention evidence exists
- THEN the finding is described as sustained growth consistent with a possible leak
- AND suggested checks are provided
- AND the system does not state that a leak is proven

### Requirement: No automatic remediation
Diagnostics MUST NOT change batch size, workers, runtime type, files, checkpoints, framework settings, or notebook code automatically.

#### Scenario: Disk pressure action
- GIVEN disk pressure is critical
- WHEN suggested actions are displayed
- THEN destructive cleanup actions require the user to choose and execute them outside the diagnostic engine
- AND no file is deleted by the observer

### Requirement: Configurable and suppressible rules
Users MUST be able to disable a rule, adjust documented thresholds within safe bounds, or acknowledge/suppress repeated display without deleting underlying evidence.

#### Scenario: Suppressed presentation
- GIVEN a user suppresses an active rule for the run
- WHEN the evidence remains true
- THEN the underlying diagnostic state remains exportable
- AND repeated prominent notifications are suppressed according to the documented scope
