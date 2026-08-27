---
status: proposed
type: openspec-delta-spec
change: build-colab-observer
tags:
  - openspec
  - requirements
  - dashboard-ux
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Delta spec: Dashboard UX

## ADDED Requirements

### Requirement: Notebook-local dashboard
The observer MUST provide a notebook-inline dashboard that requires no public share URL or hosted account and that communicates when enhanced rendering is unavailable.

#### Scenario: Enhanced dashboard unavailable
- GIVEN observation is running and the enhanced renderer cannot initialize
- WHEN the user invokes display
- THEN a local static status surface is rendered
- AND collection, diagnostics, and export remain functional

### Requirement: Operational overview
The dashboard MUST present current CPU, RAM, disk, network, accelerator, VRAM, uptime, sampler health, and active diagnostic status with units, freshness, and capability state.

#### Scenario: Stale metric
- GIVEN a metric has not updated within its freshness threshold
- WHEN the overview renders
- THEN the value is labeled stale or unavailable
- AND the previous value is not presented as current without qualification

### Requirement: Time-series exploration
The dashboard MUST let users inspect bounded time ranges, select series, reveal exact values, and switch to an equivalent tabular representation without disrupting sampling.

#### Scenario: Pause live presentation
- GIVEN the dashboard is receiving live observations
- WHEN the user pauses live updates
- THEN visible charts and announcements stop advancing
- AND the observer continues collecting unless the user separately stops it
- AND the dashboard communicates the distinction

### Requirement: Diagnostic drilldown
Each active or historical diagnostic MUST expose severity, confidence, duration, evidence, affected metrics, limitations, and non-destructive suggested actions.

#### Scenario: Open diagnostic detail
- GIVEN a diagnostic warning is visible
- WHEN the user opens its details
- THEN evidence values and time window are available
- AND the suggested action is framed as guidance rather than an automatic change

### Requirement: Export and copy controls
The dashboard MUST provide clear controls to copy a redacted diagnostics summary and create/download local report artifacts, with progress and failure feedback.

#### Scenario: Export failure
- GIVEN report creation fails because storage is full
- WHEN the export control completes
- THEN the user receives a specific failure message and recovery guidance
- AND the dashboard does not claim the report was created

### Requirement: Responsive and theme-aware presentation
The dashboard MUST remain operable in narrow Colab output areas and wide layouts and MUST support light, dark, and high-contrast presentation without hiding information.

#### Scenario: Narrow output
- GIVEN the notebook output width is narrow
- WHEN the dashboard renders
- THEN controls reflow without horizontal-only interaction
- AND primary status, warnings, and table access remain visible
