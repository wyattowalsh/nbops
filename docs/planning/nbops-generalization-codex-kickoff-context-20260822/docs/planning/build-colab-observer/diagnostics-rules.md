---
status: proposed
type: diagnostics-design
change: build-colab-observer
tags:
  - diagnostics
  - rules
  - observability
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Diagnostics rules catalog

## Rule philosophy

Diagnostics are reproducible interpretations of bounded evidence, not automatic root-cause proof. Each rule has a version, required metrics, minimum valid sample coverage, activation/recovery conditions, confidence logic, alternative explanations, suggestions, cooldown, and tests.

The numerical defaults below are **provisional design seeds**. TASK-070 benchmarks and representative runs must tune them before a stable release.

## Finding schema

| Field | Meaning |
|---|---|
| Rule ID/version | Stable docs and compatibility link |
| Lifecycle | inactive/pending/active/acknowledged/suppressed/resolved |
| Severity | info/notice/warning/critical |
| Confidence | low/medium/high with basis |
| Window | first/last seen and evidence duration |
| Evidence | metric, aggregate, threshold, sample coverage, provider/quality |
| Limitations | missing evidence and plausible alternatives |
| Suggestions | ordered, manual, non-destructive next checks |
| Recovery | condition and timestamp |

## Proposed initial rules

| ID | Finding | Provisional evidence | Recovery | Important alternatives |
|---|---|---|---|---|
| `GPU_IDLE_CPU_BUSY` | Likely input/preprocessing bottleneck | GPU utilization <10% and host CPU >80% for ≥60 s, adequate valid samples | GPU >25% or CPU <65% for ≥30 s | workload phase, compilation, small model, sync point |
| `GPU_MEMORY_PRESSURE` | Sustained VRAM pressure | VRAM used/total >90% for ≥30 s or framework OOM event | <80% for ≥30 s | caching allocator, reserved-but-reusable memory |
| `RAM_PRESSURE` | Host memory risk | available memory <10% or used >90% for ≥30 s | available >20% for ≥30 s | filesystem cache semantics, short load spike |
| `POSSIBLE_MEMORY_GROWTH` | Sustained process growth consistent with possible leak | robust positive RSS/USS trend over ≥5 min and material growth floor | trend stabilizes over a comparable window | dataset cache, expected model/checkpoint load |
| `DISK_CAPACITY_PRESSURE` | Local/mounted storage risk | free <10% or below absolute reserve; critical at stronger bound | free >15% and reserve restored | expected temporary archive, mounted quota semantics |
| `SLOW_MOUNTED_IO` | Mounted Drive/path I/O may be limiting throughput | repeated measured write/read latency or backlog above runtime baseline | latency/backlog below recovery bound | network variability, provider throttling, small writes |
| `GPU_ALLOCATED_UNDERUSED` | Framework holds VRAM while GPU is mostly idle | material framework allocation + GPU <5–10% for ≥60 s | utilization recovers or allocation released | interactive pause, evaluation, compilation |
| `RESOURCE_HEAVY_PROCESS` | Another process dominates a resource | bounded top process exceeds relative/absolute share for sustained window | process share falls | legitimate data prep/subprocess |
| `CHECKPOINT_GROWTH_RISK` | Checkpoint/output growth threatens capacity | observed output-root growth projects below reserve before run horizon | growth slows or reserve increases | one-time checkpoint, retention cleanup outside observer |
| `SAMPLER_LAG` | Monitor cannot keep configured cadence | lag exceeds fraction of interval or queue near capacity for sustained samples | lag and queue recover | overloaded runtime; monitor itself too expensive |
| `TELEMETRY_DEGRADED` | Requested evidence unavailable/degraded | provider failure/backoff or required field unavailable | provider recovers | unsupported hardware/driver/runtime |

## Confidence calculation

Confidence is rule-specific and explainable. Common inputs:

- valid sample coverage and quality;
- duration beyond the minimum window;
- presence of corroborating metrics;
- absence of key alternative evidence;
- provider stability;
- whether the workload phase is known through user markers.

Example:

```text
GPU_IDLE_CPU_BUSY
low: GPU idle only
medium: GPU idle + CPU high with good coverage
high: above + data-loader queue/starvation evidence or repeated training-step stalls
```

The first release should avoid “high” confidence where it lacks a direct corroborating signal.

## Hysteresis and cooldown

- Pending state starts when activation evidence begins.
- Activation occurs only after duration and coverage requirements.
- Recovery uses a meaningfully different threshold/window.
- Repeated active updates append evidence without creating new IDs.
- Resolved findings use cooldown before reactivation unless severity escalates.
- Acknowledgement affects presentation, not raw state.
- Suppression is scoped to rule/run or configured duration and recorded in exports.

## Suggested-action copy rules

Good guidance:

- “Inspect data loading time and CPU preprocessing; consider caching or parallel workers after confirming notebook memory limits.”
- “Copy frequently accessed data to `/content` before training, then write checkpoints to the mounted path in larger batches.”
- “Reduce batch size or enable a framework memory-saving technique after confirming the high-water mark and model requirements.”

Prohibited guidance:

- automatic deletion or moving of files;
- automatic batch/worker/framework changes;
- claims that Colab will disconnect because a metric is low;
- anti-idle or reconnect suggestions;
- one-size-fits-all “increase workers” advice without memory/CPU context.

## Rule test matrix

Every rule requires:

- exact activation fixture;
- just-below-threshold negative fixture;
- missing/stale/estimated data fixture;
- short spike that must not activate;
- oscillation/flapping fixture;
- recovery/cooldown fixture;
- alternative-explanation fixture;
- export/dashboard copy snapshot;
- suppression/acknowledgement behavior;
- performance test for long histories.

## Hardened implementation status

The default catalog now contains twelve deterministic rules:

```text
RAM_PRESSURE
POSSIBLE_MEMORY_GROWTH
DISK_CAPACITY_PRESSURE
CHECKPOINT_GROWTH_RISK
SLOW_MOUNTED_IO
GPU_MEMORY_PRESSURE
GPU_IDLE_CPU_BUSY
GPU_ALLOCATED_UNDERUSED
RESOURCE_HEAVY_PROCESS
SAMPLER_LAG
QUEUE_PRESSURE
TELEMETRY_DEGRADED
```

Every default rule has fixture coverage for a quiet/alternative-cause path, activation after its minimum duration, evidence export, confidence and limitations, and recovery. Correlated rules require fresh companion evidence and do not resolve an active finding merely because companion telemetry becomes missing. Thresholds remain provisional until representative Colab evidence exists.
