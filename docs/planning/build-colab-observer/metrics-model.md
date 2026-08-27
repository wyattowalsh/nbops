---
status: proposed
type: data-model
change: build-colab-observer
tags:
  - metrics
  - schema
  - data
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Metrics and event model

## Design goals

- Preserve what was observed, when, by which provider, with which unit and quality.
- Make missing/unavailable distinct from zero.
- Keep labels bounded and queries efficient.
- Support live summaries and later forensic reports from the same evidence.
- Expose monitor overhead and lag.

## Run record

| Field | Type | Notes |
|---|---|---|
| `run_id` | UUID/string | Stable across artifacts |
| `project` | string | User label, sanitized |
| `started_at_utc` | timestamp | Wall-clock context |
| `started_monotonic_ns` | integer | Elapsed ordering |
| `ended_at_utc` | timestamp/null | Set at stop |
| `status` | enum | running/degraded/stopped/etc. |
| `package_version` | string | Producer compatibility |
| `schema_version` | string | Run metadata schema |
| `config_json` | object | Redacted effective config |
| `runtime_json` | object | Safe runtime/capability summary |

## Scalar observation envelope

| Field | Type | Constraint |
|---|---|---|
| `run_id` | string | Required |
| `sequence` | integer | Monotonic within run |
| `observed_at_utc` | timestamp | Required |
| `monotonic_ns` | integer | Required |
| `metric` | dotted string | Registry-defined |
| `value_number` | float/null | Mutually exclusive with text |
| `value_text` | string/null | Bounded and escaped |
| `unit` | string | Required for numeric values |
| `labels_json` | object | Bounded keys/values |
| `source` | string | e.g. `psutil`, `nvml`, `nvidia-smi` |
| `quality` | enum | exact/estimated/stale/unavailable |
| `collection_duration_ms` | float | Collector overhead evidence |

## Metric naming examples

```text
system.cpu.utilization
system.cpu.load.1m
system.memory.used
system.memory.available
system.swap.used
filesystem.capacity.used
filesystem.io.read_bytes_total
filesystem.io.read_bytes_per_second
network.io.rx_bytes_total
network.io.rx_bytes_per_second
process.self.rss
process.self.rss_growth_rate
process.top.cpu_percent
drive.capacity.percent
drive.io.metadata_latency
gpu.utilization
gpu.memory.used
gpu.memory.percent
gpu.temperature
gpu.power.draw
framework.pytorch.cuda.allocated
sampler.lag
sampler.queue.depth
observer.process.cpu_percent
```

Counters retain counter semantics; rates are computed with explicit monotonic time deltas. First samples, reset/wrap, non-monotonic time, and unavailable providers produce unavailable rate samples and bounded events rather than negative or fabricated values. Reports may include both raw counters and derived rates.

## Supporting records

### Capability

`capability_id`, requested, state, provider, reason, first_seen, last_checked, metadata.

### Process snapshot

`run_id`, snapshot_sequence, observed time, rank, PID, permitted name, CPU, RSS, I/O counters, optional redacted command-line state.

### Event

`event_id`, category, level, component, message code, bounded safe details, timestamp, related sequence.

### Diagnostic finding

`finding_id`, rule/version, lifecycle state, severity, confidence, first/last seen, evidence JSON, suggestion IDs, suppression state.

## Quality semantics

| Quality | Meaning | UI/report behavior |
|---|---|---|
| `exact` | Direct provider value with expected semantics | Normal display |
| `estimated` | Derived or provider-limited estimate | Show approximation label |
| `stale` | Last known value beyond freshness bound | Preserve with age warning |
| `unavailable` | Requested field cannot be obtained | Show reason, never zero |

## Aggregation and downsampling

- Raw samples remain in the database subject to configured retention.
- UI history queries return bounded bins with min/max/mean/last and sample count where meaningful.
- Counter-rate bins are computed from valid adjacent samples.
- Gaps remain gaps.
- Diagnostics use raw or explicitly configured window aggregates, not visually downsampled data.

## Cardinality controls

- Fixed metric registry for built-in collectors.
- Bounded device and mount labels.
- Top-N process rows rather than PID as an unbounded scalar label.
- No filenames, URLs, arbitrary environment keys, or notebook cell IDs as labels by default.
- Integration adapters map to their destination explicitly rather than exporting all labels blindly.

## Retention proposal

- Default live ring buffer: enough for the visible selected range, bounded by point count.
- Default SQLite history: full run until user deletes it.
- Optional max database size/age policy stops or rotates raw storage only with explicit, recorded behavior.
- Exports can select inclusive elapsed ranges, metric names, summary-only output, process/event/diagnostic detail, and raw-database inclusion to manage bundle size.
- The export manifest records the requested and resolved query, selected row counts, preflight estimate, intentional omissions, partial state, and schema version.
