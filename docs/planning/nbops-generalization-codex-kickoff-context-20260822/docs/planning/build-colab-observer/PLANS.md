---
status: active
type: plans
change: build-colab-observer
tags:
  - plans
  - execution
  - validation
  - final-assurance
updated: 2026-08-21
cssclasses:
  - planning-doc
---
# PLANS: runtime-evidence and release-assurance hardening

## Objective

Preserve the working CPU-first `colab-observer` package while repairing only reproduced lifecycle, boundedness, provider-isolation, and export-query defects. Produce the strongest unpublished source, validation, and distribution artifacts that can be proved without dependency installation, online resolution, managed Colab, release operations, or unsupported compatibility/accessibility claims.

## Source of truth and read order

1. `AGENTS.md`
2. `openspec/changes/build-colab-observer/proposal.md`
3. `openspec/changes/build-colab-observer/specs/**/spec.md`
4. `openspec/changes/build-colab-observer/design.md`
5. `openspec/changes/build-colab-observer/tasks.md`
6. `docs/planning/build-colab-observer/runtime-evidence-hardening-20260725.md`
7. `docs/planning/build-colab-observer/validation.md`
8. `docs/planning/build-colab-observer/traceability-matrix.md`
9. `docs/planning/build-colab-observer/outer-loop.md`

## Constraints and non-goals

- No dependency installation or online package resolution.
- No Git mutation, commit, push, PR, publication, deployment, secrets, account/DNS/payment/permission action, or OpenSpec verify/sync/archive.
- No keepalive, anti-idle, hidden reconnect, timeout bypass, quota circumvention, public service, hosted backend, default telemetry, runtime CDN, or automatic remediation.
- No managed-Colab, accelerator, Python 3.11/3.12, dependency-lock, or WCAG conformance claim without direct evidence.
- Direct comm remains explicit, experimental, non-default, and absent from the package-root API.
- Supporting docs, CI, Vercel, and planning artifacts remain subordinate to product correctness.

## Progress

- [x] Verify supplied source, validation, and distribution hashes and ZIP integrity.
- [x] Recover the complete authoritative source from the verified July 17 source ZIP into an isolated workspace.
- [x] Inventory available runtimes and tooling; confirm no managed Colab, Python 3.11/3.12, lockfile, full toolchain, accessibility, ownership, or release surface appeared.
- [x] Reproduce and repair post-terminal phase/user-event acceptance.
- [x] Reproduce and repair fatal sampler state that could remain superficially running.
- [x] Reproduce and repair stale global active-observer registration after terminal/fatal state.
- [x] Reject invalid, negative, boolean, and non-finite public flush deadlines.
- [x] Contain writer close failure as bounded loss-aware evidence.
- [x] Add strict shared provider-value validation and preserve valid sibling fields.
- [x] Cap per-core CPU output and NVML device enumeration.
- [x] Reject export range arithmetic outside supported datetime/SQLite domains before writes.
- [x] Add regression tests and behavior-level scenarios; reconcile change pack, task graph, and traceability.
- [x] Pass the 249-test hermetic repository gate and 85% branch-aware coverage gate.
- [x] Pass TypeScript/Node, Chromium, Jupyter, lifecycle, benchmark, isolated soak, framework, and fail-closed managed-Colab harness evidence.
- [x] Build reproducible wheel/sdist, SBOM/provenance, and extracted-wheel evidence from the fully reconciled source.
- [x] Regenerate manifest, source/validation/distribution bundles, hashes, changed-path inventory, delivery manifest, and clean-extraction evidence.

## Surprises and discoveries

| Discovery | Impact | Resolution |
|---|---|---|
| A stopped observer still accepted phase/user markers | Events could enter a queue with no draining writer | Reject controls unless lifecycle is active and sampler healthy |
| Fatal sampler state did not immediately change `is_running`/status | Notebook code could believe observation continued | Report failed/non-running immediately, then finalize loss-aware on stop |
| Global active-observer state could return a fatally failed run | Same-cell rerun helpers could target stale state | Clean and clear stale registration on access |
| Flush accepted boolean, negative, NaN, or infinity | Wait behavior could be ambiguous or non-terminating | Validate finite non-negative real deadlines before queue interaction |
| One malformed provider field could erase useful sibling evidence | Degraded providers became all-or-nothing | Introduce strict field-level numeric validation and sibling isolation |
| NVML device count and per-core CPU cardinality were provider-controlled | Malformed providers could drive excessive iteration/output | Cap cardinality and expose bounded unavailable/truncation evidence |
| Extreme export elapsed ranges overflowed representable time | Query resolution could fail late | Validate arithmetic and persistence-domain bounds before writes |
| A combined evidence wrapper exceeded its outer budget during soak | Could be mistaken for product durability failure | Rerun the soak independently; preserve wrapper timeout and clean isolated result |

## Decision log

| Decision | Rationale | Revisit trigger |
|---|---|---|
| Preserve task rollup at 17 complete / 24 partial / 4 blocked | Local repairs strengthen existing acceptance subsets but do not establish representative runtime/release completion | Original managed-runtime/toolchain/accessibility acceptance becomes available |
| Keep direct comm experimental | No managed-Colab comm/iframe lifecycle evidence exists | Representative managed-Colab execution |
| Add scenarios rather than new requirements | Reproduced defects refine existing lifecycle, collector, and export behavior | A materially new public capability appears |
| Keep core dependencies unchanged | Strict validation can be implemented in the package without dependency expansion | Evidence proves a dependency materially improves correctness/value |
| Enter final-assured maintenance after clean packaging | Remaining useful work requires unavailable surfaces or approval | Material defect, failed validation/package drift, stale behavioral fact, unsafe drift, installed-runtime defect, missing release evidence, or explicit request |

## Validation log

| Check | Result | Evidence |
|---|---|---|
| Targeted lifecycle/provider/export regressions | Pass | `runtime-evidence-hardening-20260725.md`; targeted pytest logs |
| Hermetic `make check` | 249 tests pass | `/mnt/data/colab-observer-next-evidence-20260725/full/make-check.log` |
| Branch-aware coverage | 87.4176%, gate 85% | `/mnt/data/colab-observer-next-evidence-20260725/full/coverage.json` |
| TypeScript compiler and runtime | No-emit pass; 9/9 runtime checks | `full/tsc-noemit.log`, `runtime/ui-protocol-runtime/` |
| Chromium | 21/21, zero remote requests/errors/dialogs | `runtime/browser-smoke/` |
| Local Jupyter | 10/10, 491 observations, zero drops | `runtime/jupyter-smoke/` |
| Local lifecycle/export smoke | 1,127 observations, zero drops | `runtime/local-smoke/` |
| Local default/stress benchmarks | Pass, zero drops | `runtime/benchmark-default.json`, `runtime/benchmark-stress.json` |
| Isolated 30-second soak | 7,747 persisted, zero drops, bounded history, clean SQLite checks | `runtime/local-soak-30s/local-soak.json` |
| Frameworks | PyTorch/JAX pass; TensorFlow truthfully skipped | `runtime/framework-smoke/` |
| Managed-Colab harness | Default blocked outside Colab; explicit local mode non-representative | `runtime/managed-colab-default/`, `runtime/managed-colab-local/` |
| Reproducible packages and final archive | Pass at release freeze | External distribution audit, delivery manifest, and clean-extraction log |

Local count differences from prior runs reflect host/runtime timing and do not define a regression budget. The invariant gates are clean termination, bounded history/queues, zero drops in the recorded runs, integrity checks, and truthful non-representative labeling.

## Recovery / rollback

The verified July 17 source ZIP remains immutable rollback evidence. This loop runs only in an isolated recovered copy. If final package or archive validation fails, retain the prior bundle and the exact failing evidence rather than replacing a known-good artifact.

## Outcomes and retrospective

The explicit rerun request exposed a coherent cluster of lifecycle and provider-boundary defects with direct reproductions and narrow repairs. The package is locally stronger without expanding dependencies or product scope. Remaining release value is concentrated in managed Colab, Python 3.11/3.12, reviewed locks/toolchain, manual accessibility, public ownership, and release approval.

## Follow-on planning state

- [x] Preserve this change as the implemented/local-evidence baseline.
- [x] Create `generalize-notebook-runtime-observer` as a separate proposed change.
- [x] Record the sequencing decision in ADR-010.
- [x] Link runtime profile, measurement scope, storage, display, support, migration, validation, and handoff plans.
- [ ] Begin follow-on implementation only through its compatibility-first TASK-103 gate and only after an explicit implementation request.

No current baseline task is reopened by the planning-only follow-on.
