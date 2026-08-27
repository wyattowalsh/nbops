---
status: proposed
type: openspec-delta-spec
change: build-colab-observer
tags:
  - openspec
  - requirements
  - metrics-collectors
updated: 2026-07-25
cssclasses:
  - planning-doc
---

# Delta spec: Metrics collectors

## ADDED Requirements

### Requirement: Core resource observations
The observer MUST collect runtime identity, CPU, memory, swap, disk capacity, disk I/O, network I/O, and current-process observations on supported CPU-only runtimes.

#### Scenario: Core sample
- GIVEN a supported runtime with no accelerator
- WHEN a scheduled core sample completes
- THEN each available core metric is recorded with a value, unit, source, timestamp, and quality
- AND unavailable metrics are not represented as zero

#### Scenario: Provider returns impossible core evidence
- GIVEN a core provider returns a non-finite, negative, out-of-range, missing, or structurally invalid field
- WHEN the affected collector records the sample
- THEN that field is represented as unavailable rather than fabricated
- AND valid sibling fields remain available
- AND unrelated collectors continue

#### Scenario: Oversized per-core response is bounded
- GIVEN a CPU provider reports an unreasonable number of per-core values
- WHEN the CPU collector builds the sample
- THEN the retained per-core observations are capped at a documented safe bound
- AND the truncation is represented by bounded structured evidence
- AND aggregate CPU and unrelated metrics remain available where valid

### Requirement: Bounded process visibility
The observer MUST provide a bounded top-process view by resource use while excluding full command lines and sensitive process metadata by default.

#### Scenario: Default process snapshot
- GIVEN process collection is enabled with default privacy settings
- WHEN a process snapshot is taken
- THEN only the configured number of process rows is retained
- AND each row contains only permitted identifiers, process name, and resource counters
- AND command-line arguments are absent

### Requirement: NVIDIA provider fallback
On an NVIDIA runtime, the observer MUST attempt a primary provider for utilization, memory, temperature, power, and active-process observations and MUST use a safe fallback when the primary provider is unavailable and the fallback is supported.

#### Scenario: Primary provider unavailable
- GIVEN an NVIDIA device is visible but the primary provider cannot initialize
- WHEN the GPU collector probes capability
- THEN the observer attempts the supported fallback
- AND each GPU observation identifies its provider
- AND degraded fields are marked unavailable or estimated rather than fabricated

#### Scenario: Provider reports unreasonable device enumeration
- GIVEN an NVIDIA provider returns a non-integral, boolean, negative, or excessive device count
- WHEN capability probing or collection begins
- THEN the provider is rejected or reported unavailable before unbounded device iteration
- AND unrelated collectors continue
- AND provider-private exception text is not exported

### Requirement: Optional framework observations
The observer MUST support best-effort PyTorch, TensorFlow, and JAX device or memory observations without requiring all frameworks or importing disabled frameworks solely for monitoring.

#### Scenario: Framework not installed
- GIVEN a framework collector is enabled but the framework is not importable
- WHEN capability detection runs
- THEN the collector reports unavailable without installing the framework
- AND unrelated collectors continue

#### Scenario: One framework field is malformed
- GIVEN a loaded framework exposes one malformed, non-finite, or coercive telemetry field while another field is valid
- WHEN its optional collector records evidence
- THEN the malformed field is unavailable
- AND valid sibling framework evidence is retained
- AND the collector does not mutate framework or device state

### Requirement: Honest TPU detection
The observer MUST distinguish TPU/device detection from utilization telemetry and MUST clearly identify fields that the active runtime cannot expose.

#### Scenario: TPU detected without utilization
- GIVEN a TPU device is detected but utilization data is unavailable
- WHEN the dashboard and report render TPU status
- THEN they display detected topology or device information
- AND they label utilization as unavailable
- AND no utilization percentage is inferred

### Requirement: Versioned observation envelope
Every observation MUST conform to a versioned schema that preserves metric identity, value type, unit, labels, source, quality, run identity, sequence, wall time, monotonic time, and collection duration.

#### Scenario: Schema round trip
- GIVEN observations from different enabled collectors
- WHEN they are persisted and exported
- THEN each record can be parsed using the declared schema version
- AND semantic units and unavailable states survive the round trip

#### Scenario: Unavailable evidence has no value
- GIVEN a collector cannot obtain a metric value
- WHEN it emits an unavailable observation
- THEN the observation retains its metric identity, unit, source, timestamp, and quality
- AND it contains neither a numeric value nor a textual value
- AND downstream consumers do not reinterpret the missing value as zero

### Requirement: Independent collector cadence
The observer MUST support different safe cadences for fast and expensive collectors and MUST expose effective cadence and skipped samples.

#### Scenario: Expensive process collection
- GIVEN core metrics use a shorter interval than process snapshots
- WHEN the run proceeds for multiple core intervals
- THEN process collection occurs only at its configured cadence
- AND the exported configuration records both cadences
