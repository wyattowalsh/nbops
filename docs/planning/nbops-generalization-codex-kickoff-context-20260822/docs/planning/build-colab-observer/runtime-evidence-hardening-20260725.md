---
status: implemented
kind: evidence
change: build-colab-observer
updated: 2026-07-25
tags:
  - colab-observer
  - runtime
  - lifecycle
  - collectors
  - validation
cssclasses:
  - planning-doc
---

# Runtime evidence hardening — 2026-07-25

**Path:** `docs/planning/build-colab-observer/runtime-evidence-hardening-20260725.md`  
**Purpose:** Record the evidence-gated product repairs performed after reconstructing the July 17 authoritative source bundle.  
**Status:** Implemented locally; managed-Colab and multi-version runtime evidence remain blocked.  
**Load/use when:** Reviewing lifecycle truthfulness, collector boundedness, export-query safety, validation evidence, or the next representative-runtime gate.

## Bottom line

The supplied source, validation, and distribution bundles were hash-verified and the source was reconstructed into an isolated working directory. No new managed-Colab, Python 3.11/3.12, lockfile, assistive-technology, or ownership surface was available. The explicit user request and a focused boundary audit nevertheless exposed material local defects that justified a narrow implementation loop.

The repaired package now:

- rejects post-terminal phase markers and user notes instead of queuing controls that can never drain;
- reports a fatal sampler worker as failed and non-running before explicit shutdown;
- clears stale globally registered observers after fatal or terminal state;
- rejects negative, boolean, non-finite, and otherwise invalid flush deadlines before waiting;
- contains store-close failures and records bounded loss-aware terminal evidence;
- preserves valid sibling observations when individual CPU, memory, disk, network, process, Drive, GPU, or framework fields are malformed;
- caps unreasonable per-core CPU and NVML device enumeration;
- rejects export elapsed ranges that exceed the supported timestamp or SQLite integer domain before writing artifacts.

## `/grill-me` preflight

| Question | Evidence inspected | Recommended/default answer | Decision | Artifact impact |
|---|---|---|---|---|
| Is there a new representative runtime, dependency, accessibility, or ownership surface? | Available binaries, uploaded bundles, local runtime, current Colab documentation | No. Preserve all unsupported claims and do not promote direct comm. | Accepted by evidence | Runtime matrix and blockers remain explicit. |
| Does another local source mutation have material value? | Baseline 240-test suite plus targeted lifecycle/provider boundary audit | Yes, but only for reproduced correctness and boundedness defects. | Accepted | Product source, tests, three delta specs, traceability, and validation ledgers updated. |
| Should docs/release surfaces become the work focus? | Product hierarchy and remaining blockers | No. Validate and package supporting artifacts only after product repairs settle. | Accepted | No Fumadocs, Vercel, publish, or identity expansion. |

No user question was required because the recommended defaults followed directly from the preserved product invariants and available evidence.

## Reproduced defects and repairs

### 1. Terminal control events could enter a dead queue

**Previous behavior:** `mark()` accepted events after clean stop and after a fatal sampler failure. With the writer already stopped, such events could never be persisted or drained.

**Repair:** phase markers and user notes now require an active observer and a healthy sampler. Terminal/fatal calls fail clearly and leave lifecycle evidence unchanged.

**Regression evidence:** `tests/integration/test_observer_controls.py`; `tests/unit/test_hardening.py`.

### 2. Fatal worker state could remain superficially running

**Previous behavior:** before an explicit `stop()`, a fatal sampler-thread infrastructure failure could leave `is_running` true and `status()` reporting `running` even though no future sample could occur.

**Repair:** sampler fatal state immediately makes the observer non-running and reports `failed`; explicit shutdown then finalizes `stopped_with_loss`, preserving bounded error evidence.

**Regression evidence:** `tests/unit/test_hardening.py`.

### 3. Stale active-observer registration survived fatal state

**Previous behavior:** the global active-observer helper could continue returning an observer whose sampler had failed.

**Repair:** retrieving the active observer now idempotently cleans terminal/fatal state and clears the stale registration.

**Regression evidence:** `tests/unit/test_api_events_memory.py`.

### 4. Flush deadlines accepted ambiguous or non-terminating values

**Previous behavior:** booleans, negative values, and non-finite timeouts could reach queue/wait primitives with ambiguous or unbounded behavior.

**Repair:** public flush deadlines must be finite, non-negative real numbers and must not be booleans.

**Regression evidence:** `tests/integration/test_observer_controls.py`.

### 5. Provider-field failure could erase valid sibling evidence

**Previous behavior:** malformed values from `psutil`, Drive, NVML, or framework adapters could fail an entire collector or be coerced into misleading values.

**Repair:** shared strict numeric helpers reject booleans, strings, non-finite values, negative counters, and unreasonable values. Narrow provider boundaries preserve valid sibling fields as exact evidence and represent only the malformed field as unavailable.

**Material paths:**

```text
src/colab_observer/collectors/values.py
src/colab_observer/collectors/cpu.py
src/colab_observer/collectors/memory.py
src/colab_observer/collectors/disk.py
src/colab_observer/collectors/network.py
src/colab_observer/collectors/process.py
src/colab_observer/collectors/drive.py
src/colab_observer/collectors/frameworks.py
src/colab_observer/collectors/gpu_nvml.py
src/colab_observer/collectors/runtime.py
```

### 6. Provider cardinality could drive excessive work

**Previous behavior:** an untrusted NVML device count was used directly as an iteration bound, and an unreasonable per-core CPU response could produce excessive observations.

**Repair:** NVML device enumeration is capped at 64 devices and rejects malformed counts; per-core CPU evidence is capped at 4,096 rows with bounded truncation evidence while aggregate CPU evidence remains available.

**Regression evidence:** `tests/unit/test_optional_providers.py`; `tests/unit/test_collectors.py`.

### 7. Export elapsed-range arithmetic could overflow late

**Previous behavior:** extreme elapsed-time filters could overflow datetime or persistence integer arithmetic while resolving an export query.

**Repair:** export query resolution catches arithmetic overflow and validates the resolved timestamp domain before any artifact is written.

**Regression evidence:** `tests/unit/test_export_queries.py`.

### 8. Writer close failures could escape daemon cleanup

**Previous behavior:** a store close failure in the writer thread could escape cleanup as an uncaught daemon exception.

**Repair:** close failure is sanitized through the existing error sink and produces loss-aware terminal status without leaking provider internals.

**Regression evidence:** `tests/integration/test_observer_controls.py`.

## Preserved boundaries

The loop did not:

- install or resolve dependencies;
- mutate Git or any remote repository;
- run a managed Colab session;
- claim Python 3.11/3.12 execution;
- activate or promote direct comm;
- add telemetry, a public service, hosted backend, runtime CDN, or remote code;
- add keepalive, anti-idle, reconnect automation, timeout bypass, or quota circumvention;
- publish packages or deploy the docs site.

## Validation snapshot

After the source repairs and before planning reconciliation:

| Gate | Result |
|---|---:|
| Hermetic repository gate | 249 tests pass |
| Branch-aware combined coverage | 87.4176% |
| Coverage requirement | 85% |
| Runtime modules imported without optional framework imports | 47 |
| Python 3.11 grammar parse | 104 source/test/script files |
| OpenSpec structural domains | 11 |
| Public schemas and fixtures | 4 + 4 |

Full browser, Jupyter, smoke, benchmark, soak, framework, package, and archive evidence is recorded in `validation.md`, `validation-evidence.json`, and the final delivery evidence bundle after reconciliation.

## Reassessment

The local repairs have positive product value and close reproduced correctness/boundedness defects. No currently available local task justifies promoting direct comm, changing public release identity, or shifting focus to deployment/docs. The next material release-evidence loop still requires at least one of:

- a managed Google Colab CPU/NVIDIA/TPU/Drive session;
- Python 3.11 or 3.12 execution;
- an approved isolated dependency-resolution environment;
- representative browser/assistive-technology testing;
- public ownership, licensing, namespace, or release decisions;
- a newly reproduced material defect or failed validation.
