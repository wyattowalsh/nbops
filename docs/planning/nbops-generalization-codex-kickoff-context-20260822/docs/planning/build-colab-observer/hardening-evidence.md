---
status: ready
type: implementation-evidence
change: build-colab-observer
tags:
  - implementation
  - hardening
  - validation
  - evidence
updated: 2026-07-11
cssclasses:
  - planning-doc
---
# Product-hardening evidence: `colab-observer`

> [!note] Historical evidence boundary
> This document records the prior CPU/storage hardening checkpoint. Current dashboard protocol, static UI, direct-comm candidate, 108-test result, and 88.97% coverage evidence live in [[docs/planning/build-colab-observer/evidence-gated-hardening|evidence-gated-hardening.md]] and [[docs/planning/build-colab-observer/validation|validation.md]].

**Scope:** local Linux/Python 3.13.5 evidence for the CPU-first package. This is not representative Google Colab, NVIDIA, TPU, mounted-Drive, browser-widget, or WCAG-conformance evidence.

## Outcome

The hardening loop completed the remaining locally testable collector, SQLite, diagnostics, and export behavior without installing dependencies or changing the unpublished/release posture.

| Surface | Material result |
|---|---|
| Counter-derived metrics | Reset/wrap and non-monotonic time produce explicit unavailable samples and bounded events rather than negative rates |
| Disk and network | Raw counters plus reset-safe rates; missing paths, invalid capacities, and unavailable providers remain explicit |
| Process and memory | Process-exit/permission failures are bounded; self CPU is not fabricated as zero; RSS-growth evidence is derived with monotonic baselines |
| Mounted Drive | Read-only mount, capacity, and metadata-latency evidence; no mount, auth, account API, or write probe |
| TPU | Presence detection is distinct from utilization; unavailable utilization remains null, never zero |
| NVIDIA providers | One malformed field does not erase valid device evidence; impossible values are unavailable; raw provider stderr is not exported |
| Diagnostics | Twelve deterministic rules support corroborating signals, freshness, activation duration, hysteresis, cooldown, stable IDs, recovery, limitations, and no automatic remediation |
| SQLite | Read-only readers do not create databases; backup is atomic, WAL-aware, path-safe, integrity-checked, and preserves existing destinations on failure |
| Exports | Inclusive elapsed ranges, metric selection, summary-only output, artifact inclusion controls, preflight size estimate, manifest schema 1.1.0, deterministic checksums and ZIP |
| Loss reporting | A run ending `stopped_with_loss` always produces a partial bundle rather than claiming completeness |

## Task-state impact

Promoted to complete after local acceptance evidence:

- `TASK-013-implement-sqlite-store`
- `TASK-024-tpu-drive-collectors`
- `TASK-031-implement-diagnostic-catalog`
- `TASK-034-implement-bundle-export`

Current OpenSpec implementation state: **16 complete, 20 partial, 9 blocked/deferred**.

`TASK-032-implement-tabular-exports` remains partial because range-aware CSV/JSONL and summaries are complete, while an optional DuckDB adapter is intentionally deferred until dependency, wheel-size, startup, and real-Colab evidence justify it.

## Automated validation

| Gate | Result |
|---|---|
| Full repository gate | Pass |
| Tests | 89 passed with `ResourceWarning` treated as an error |
| Combined branch-aware coverage | 89.57%, gate 85% |
| OpenSpec delta structure | 11 domains pass repository validator |
| Runtime imports | 42 modules pass without optional dependency imports |
| Public schemas | 3 schemas and 3 fixtures pass, including export manifest 1.1.0 |
| Pre-commit source contract | 16 local hooks, 14 commit-stage and 2 pre-push |
| Security/policy source checks | Pass, with no high-confidence secrets or executable prohibited behavior |

## Local runtime evidence

### Default 2-second interval

| Metric | Result |
|---|---:|
| Duration | 6.184653 s |
| Observations | 415 |
| Dropped batches | 0 |
| Incremental CPU signal | 1.9403% of one core |
| Peak RSS delta | 4,829,184 bytes |
| Maximum sampler lag | 0.051951 s |
| Final status | stopped |

### Aggressive 200-millisecond interval

| Metric | Result |
|---|---:|
| Duration | 3.393555 s |
| Observations | 1,627 |
| Dropped batches | 0 |
| Incremental CPU signal | 14.4391% of one core |
| Peak RSS delta | 5,922,816 bytes |
| Maximum sampler lag | 0.048034 s |
| Final status | stopped |

### Thirty-second bounded durability soak

| Metric | Result |
|---|---:|
| Duration | 30.0949 s |
| Interval | 0.2 s |
| Observations seen and persisted | 15,448 |
| Dropped batches | 0 |
| In-memory history | bounded at 2,000 |
| Reader failures | 0 |
| Lingering observer threads | 0 |
| Peak RSS delta | 11,145,216 bytes |
| Process CPU signal | 16.448% of one core |
| Sampler lag mean / p95 / max | 0.011832 / 0.021626 / 0.021823 s |
| Source and backup SQLite quick check | ok / ok |
| Summary-only range bundle | complete, schema 1.1.0, 10 entries |

These measurements are local regression signals. They are not release budgets or Colab performance claims.

## Reproducibility and toolchain blockers

| Gate | Local state | Required unblocker |
|---|---|---|
| `uv lock --offline` | Fails because `psutil` is absent from the cache | Approved dependency-resolution environment |
| Ruff | Executable unavailable | Approved environment with reviewed lock |
| ty | Executable unavailable | Approved environment with reviewed lock |
| pre-commit runner | Executable unavailable; static config contract passes | Approved environment with reviewed lock |
| Python matrix | Only Python 3.13.5 available | Python 3.11 and 3.12 environments or CI runners |
| pnpm/Fumadocs build | pnpm and dependency tree unavailable | Approved frozen web environment |
| OpenSpec CLI | Executable unavailable | Approved repo-native tooling |

## Deferred decisions

- Preserve SQLite as the only default durable write path.
- Keep DuckDB optional and unimplemented until measured value exceeds installation, wheel, startup, and maintenance cost.
- Keep the rich dashboard blocked until a real Colab local-asset transport spike proves the no-public-endpoint and no-runtime-CDN constraints.
- Preserve the static semantic-table surface as the correctness and accessibility baseline.

## Remaining evidence boundary

The next material loop requires at least one of:

1. a clean, approved dependency-resolution environment;
2. Python 3.11/3.12 runtimes;
3. real Colab CPU, NVIDIA, TPU, and mounted-Drive execution;
4. a safe local-only widget transport surface;
5. an owning repository plus license/release decisions.

Without one of those surfaces, additional code or documentation refinement has low marginal utility and risks unsupported claims.
