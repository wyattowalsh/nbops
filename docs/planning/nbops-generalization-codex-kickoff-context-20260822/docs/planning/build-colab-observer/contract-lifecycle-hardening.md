---
status: active
type: implementation-evidence
change: build-colab-observer
tags:
  - evidence
  - contracts
  - lifecycle
  - failure-isolation
  - validation
updated: 2026-07-13
cssclasses:
  - planning-doc
---

# Contract and lifecycle hardening

**Path:** `docs/planning/build-colab-observer/contract-lifecycle-hardening.md`  
**Purpose:** Record the evidence-gated repairs made after the representative-runtime bundle was re-audited on 2026-07-13.  
**Status:** Local repair slice complete; representative release gates remain open.

## `/grill-me` result

The declared workspace was partial while the source ZIP and companion hash were intact. The complete 308-file source was reconstructed into `/mnt/data/colab-observer-next-evidence-20260713` only after verifying the declared SHA-256. No question was needed because the default was evidence-determined: preserve the prior bundle and work in a separate recovered directory.

The newly available local surface did not include managed Colab, Python 3.11/3.12, dependency locks, Ruff, ty, executable pre-commit, pnpm, or OpenSpec CLI. The material path was therefore a public-contract and lifecycle-failure audit using the existing Python 3.13, JSON Schema, Node/TypeScript, Chromium, Jupyter, package, and local-runtime surfaces.

## Material defects found

| Defect | Prior behavior | Risk | Repair |
|---|---|---|---|
| Observation value-mode drift | Public JSON Schema accepted combinations that `Observation.from_dict()` rejected | Portable artifacts could pass schema validation but fail in the package | Root and wheel schemas now use mutually exclusive numeric, text, and unavailable value modes |
| Numeric evidence without units | Schema accepted numeric observations with `unit: null` while Python rejected them | Readers could disagree about valid observations | Numeric schema branch now requires a bounded string unit |
| Offset-naive timestamps | Python accepted some naive datetimes that public schemas reject | Wall-time evidence could be ambiguous or non-portable | Public decoders and model construction now require offset-aware timestamps and normalize to UTC |
| Empty dashboard snapshots | Python accepted an empty snapshot payload that the schema rejects | Malformed comm messages could enter the kernel/UI boundary | Dependency-free payload validation now enforces message-type-specific required fields |
| Duplicate dashboard metrics | Python silently deduplicated filters while schema and TypeScript reject duplicates | Browser/kernel control semantics could diverge | Python now rejects duplicate filters exactly like schema and TypeScript |
| Optional GPU probe escape | NVML/provider probe exceptions could escape registry resolution | One unavailable provider could abort observer setup | Probe and construction failures now become bounded unavailable capability evidence; rejected providers are closed |
| Non-transactional startup | A descriptor or initialization failure could leave the observer in `starting` and retain resources | Notebook reruns could inherit leaked collectors or ambiguous state | Startup now cleans sampler/writer/collectors best-effort, clears owned handles, records bounded error, and ends in `failed` |
| Fatal sampler-thread escape | A non-collector infrastructure failure could terminate the daemon without durable evidence | The run could appear active or complete after observation stopped | Fatal worker failures are contained, emitted as bounded critical events, persisted best-effort, and converted into loss-aware terminal status |

The before/after executable audit is stored externally in:

```text
/mnt/data/colab-observer-contract-lifecycle-validation-20260713/contract-and-lifecycle-drift-before.json
/mnt/data/colab-observer-contract-lifecycle-validation-20260713/contract-and-lifecycle-drift-after.json
```

## Observable behavior after repair

- Untrusted observation and dashboard payloads either satisfy the versioned public contract or fail closed with a bounded error.
- Missing units, incompatible value modes, naive timestamps, duplicate metric filters, empty snapshots, and invalid typed fields are not silently normalized into valid evidence.
- Optional GPU provider discovery cannot terminate CPU-only observation merely because one provider constructor or probe fails.
- Observer startup is atomic from the public caller’s perspective: it returns a running observer or raises with state `failed` after best-effort resource cleanup.
- A fatal sampler infrastructure error cannot escape the daemon as raw exception text. It produces sanitized loss evidence and the observer stops as `stopped_with_loss`.
- Normal collectors, persistence, exports, static dashboard, and experimental direct comm behavior remain unchanged outside the repaired boundaries.

## Design alignment

These repairs implement existing behavior requirements rather than widening scope:

- `runtime-observability`: non-blocking lifecycle, capability-aware status, failure isolation, and bounded structured events.
- `metrics-collectors`: versioned observation envelopes and truthful unavailable states.
- `security-policy`: bounded malformed-provider handling and no raw provider detail leakage.
- `dashboard-ux`: versioned local message behavior and recoverable invalid-message handling.

No delta-spec implementation detail was added. Internal cleanup order, validation helpers, schema branches, and thread mechanics remain in design, tasks, source, and tests.

## Validation evidence

| Check | Result |
|---|---:|
| Final repository suite | 142 passed |
| Combined line-and-branch coverage | 87.5430%, gate 85% |
| Covered lines / statements | 3,264 / 3,618 |
| Covered branches | 812 / 1,038 |
| Contract/lifecycle after-audit | All enumerated contract cases aligned; GPU probe isolated; startup transactional |
| TypeScript/Node protocol | 9/9 pass |
| Local Chromium | 21/21 pass, zero remote requests/errors/dialogs |
| Local Jupyter kernel | 10/10 pass, 950 observations, zero drops |
| Local lifecycle/export smoke | 2,198 observations, zero drops, 17 bundle entries, 16 verified checksums |
| Default local benchmark | 415 observations, zero drops, 1.4486% one-core signal |
| Stress local benchmark | 1,627 observations, zero drops, 13.1242% one-core signal |
| Isolated 30-second soak | 15,448 persisted observations, zero drops, bounded 2,000-row history, source/backup SQLite `ok` |

Two earlier outer command wrappers stopped after test progress reached 100%. Direct and repeated suites completed, and a fresh settled-source `make check` later returned exit code 0 with `142 passed`. No product deadlock or lingering observer thread was reproduced; the earlier anomaly remains recorded as execution-wrapper instability.

## Boundaries that remain open

- Managed Colab CPU, NVIDIA, TPU, mounted Drive, iframe, and direct comm.
- Python 3.11 and 3.12 execution.
- Reviewed `uv.lock` and `pnpm-lock.yaml`, dependency licenses/advisories, Ruff, ty, executable pre-commit, and frozen docs build.
- Manual screen-reader, zoom, multiple-browser, managed-notebook, and live-region review.
- Public owner, license, repository, package namespace, canonical URLs, release channels, publication, and deployment.

## Reassessment

This local loop had positive marginal utility because it found eight concrete contract/failure-boundary issues and repaired them with regression evidence. Further speculative local feature expansion now has lower value than the missing representative surfaces. Preserve this slice in final-assured maintenance unless a material defect, failed validation, stale authoritative fact, unsafe drift, explicit request, or newly available blocked surface appears.
