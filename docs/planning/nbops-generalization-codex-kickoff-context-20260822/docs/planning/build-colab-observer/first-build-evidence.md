---
status: ready
type: implementation-evidence
change: build-colab-observer
tags:
  - implementation
  - validation
  - cpu
  - security
updated: 2026-07-11
cssclasses:
  - planning-doc
---
# First-build implementation evidence

> [!note] Historical baseline
> This file preserves the first-build evidence snapshot. Current product-hardening results, task promotions, 89-test coverage, range-aware exports, and SQLite/collector/diagnostic hardening are recorded in [[docs/planning/build-colab-observer/hardening-evidence|hardening-evidence.md]].

**Authoritative workspace:** `/mnt/data/colab-observer-authoritative-20260711`, frozen from the isolated greenfield target because no owning repository was supplied.  
**Decision:** The CPU-only product slice is locally validated and **final-with-known-risks**. It is not a release candidate and does not establish real Colab, GPU, TPU, browser, or manual accessibility compatibility.

## `/grill-me` outcome

| Challenge | Evidence/default | Decision | Artifact impact |
|---|---|---|---|
| Existing or greenfield target? | The target directory contained the generated first-build source but no Git metadata or remote. | Audit and repair in place; do not create Git or remote state. | Preserved isolated workspace. |
| Could stale ledgers be trusted? | Planning files said implementation had not started while executable source existed. | Treat source/tests as evidence, then reconcile ledgers. | Tasks, PLANS, validation, finalization, manifest, and continuation refreshed. |
| What failed first? | Pytest could not import integration helpers because `tests` was not a package. | Repair the harness before assessing product correctness. | Added `tests/__init__.py`; collection now succeeds. |
| What core gaps had highest value? | Degraded runs could look clean; partial export and schema packaging needed proof. | Add loss-aware terminal status, stage-preserving exports, packaged schemas, and regression tests. | Runtime and artifact semantics strengthened. |
| Should support surfaces lead? | Runtime hardening and direct evidence still dominate risk. | Keep docs/CI/Vercel subordinate; add only static contracts that prevent drift. | Fumadocs scaffold and pre-commit validator remain support surfaces. |
| Can locks/tools be fabricated? | Offline resolution lacked `psutil`; Ruff, ty, pre-commit, OpenSpec, and pnpm executables are absent. | Keep frozen CI deliberately blocked until reviewed locks exist. | No dependency installation or online resolution occurred. |

## Material implementation and repair work

- Added importable test package and expanded the suite to queue overflow, transform failure, slow collectors, shutdown timeout, concurrent SQLite reads, storage-write failure, diagnostics cooldown/suppression/reactivation, deterministic bundles, size warnings, and partial export preservation.
- Added deterministic coverage for inactive diagnostic recovery and persisted structured-event decoding so scheduler timing no longer changes the reported coverage total.
- Added `RunStatus.STOPPED_WITH_LOSS` and persisted it when collection, queue, sampler, or storage loss prevents a truthful clean stop.
- Hardened bundle export so one failed stage does not erase valid artifacts; failures are named without copying sensitive exception text.
- Bundled all public JSON Schemas in the wheel and added source/package schema parity checks.
- Added a dependency-free pre-commit contract validator for 16 local hooks with 14 commit-stage and 2 pre-push gates.
- Pinned GitHub Actions to immutable full SHAs, set read-only default permissions, and made frozen dependency sync an explicit prerequisite rather than hidden resolution.
- Preserved a script-free accessible static display and no-public-service/no-telemetry boundary.

## OpenSpec task state

| State | Count | IDs |
|---|---:|---|
| Complete | 12 | TASK-004, TASK-011, TASK-012, TASK-014, TASK-020, TASK-021, TASK-022, TASK-023, TASK-025, TASK-030, TASK-033, TASK-045 |
| Partial | 24 | TASK-001, TASK-002, TASK-003, TASK-010, TASK-013, TASK-024, TASK-031, TASK-032, TASK-034, TASK-040, TASK-050, TASK-051, TASK-052, TASK-053, TASK-054, TASK-055, TASK-060, TASK-061, TASK-062, TASK-063, TASK-070, TASK-071, TASK-073, TASK-074 |
| Blocked/deferred | 9 | TASK-041, TASK-042, TASK-043, TASK-044, TASK-046, TASK-064, TASK-065, TASK-072, TASK-075 |

The original acceptance criteria remain authoritative. A partial task has executable evidence but still has a named gap in `tasks.md` and `outer-loop.md`.

## Exact validation results

| Check | Result |
|---|---|
| Repository hygiene | Pass |
| Secret scan | Pass, no credential files or high-confidence token patterns |
| Prohibited behavior policy | Pass |
| JSON Schemas and fixtures | Pass, 3 schemas and 3 fixtures |
| Notebook structure/sync | Pass, exactly 3 clean canonical cells |
| OpenSpec structure | Pass, 11 domain delta specs |
| Nested AGENTS | Pass, 11 durable instruction files |
| Workflow security | Pass, 1 workflow, immutable action SHAs, read-only defaults |
| Pre-commit contract | Pass, 16 local hooks: 14 fast and 2 pre-push |
| Docs-site source contract | Pass, Fumadocs scaffold, 14 pages, SEO and AI-reader surfaces |
| Import every package module | Pass, 39 modules |
| Byte compilation | Pass |
| Tests | Pass, 60 |
| Branch-aware coverage | Pass, 90.74% against 85% gate |
| Offline, no-install wheel/sdist build | Pass twice with fixed `SOURCE_DATE_EPOCH`; no-index wheel and normalized build-meta sdist are byte-identical across runs |
| Distribution inspection | Pass, one wheel and one sdist, safe paths and bundled schemas |
| Direct wheel smoke | Pass, 502 observations, 0 dropped, clean stop, semantic static display, reports/bundle and 3 schemas |
| `uv lock --offline` | Blocked, `psutil` absent from local cache and network resolution not authorized |
| Ruff, ty, pre-commit executable, OpenSpec CLI, pnpm | Not run, tools unavailable and installation not authorized |
| Real Colab matrix | Not run |

## Local runtime evidence

| Profile | Interval | Wall | CPU signal | RSS signal | Observations | Dropped | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| Aggressive lifecycle/export smoke | 0.1 s | 2.066 s | 43.560% of one core | +3,252,224 bytes | 1,736 | 0 | Clean stop; 13 checksums verified |
| Bounded default-interval benchmark | 2.0 s | 6.223 s | 3.3507% incremental one-core signal | +3,100,672 peak bytes | 338 | 0 | Clean stop; no queue loss |
| Direct wheel smoke | 0.1 s | 0.5 s sampling sleep | Not benchmarked | Not benchmarked | 502 | 0 | Clean stop, accessible static markup, and exports |

These are short, noisy measurements on the available Python 3.13.5 Linux environment. They prove the local evidence path and interval sensitivity, but they are not Colab performance budgets.

## Distribution artifacts

Two independent fixed-epoch builds produced byte-identical artifacts. The source distribution was normalized to deterministic tar/gzip metadata after the standard backend build.
A third rebuild from the final reconciled source snapshot produced the same wheel and normalized sdist byte-for-byte.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `colab_observer-0.1.0.dev0-py3-none-any.whl` | 62,577 | `59745d2a0dc5c68ac6f2f81c01ea7fc5d9555c732ae4b6911713bf7735489ac3` |
| `colab_observer-0.1.0.dev0.tar.gz` | 44,050 | `73b94bc1dae356376e2cf50e74d055e60dcfd8b90a920c64fa34caf64a589636` |

## Runtime matrix

| Environment | Python | CPU/store/export | GPU/framework/TPU | Representative Colab? |
|---|---|---|---|---|
| Available Linux container | 3.13.5 | Pass | fake/passive/detection tests only | No |
| Direct wheel-archive import | 3.13.5 | Pass | disabled for smoke | No |
| Google Colab CPU | Not run | Not run | N/A | Pending |
| Google Colab NVIDIA | Not run | Not run | Not run | Pending |
| Google Colab TPU | Not run | Not run | best-effort only | Pending |

## Known gaps

- No reviewed `uv.lock` or `pnpm-lock.yaml`, no frozen dependency environment, and no multi-Python execution.
- No real Colab CPU/NVIDIA/TPU run or 30-minute soak.
- No full Drive I/O evidence, full diagnostics catalog, time-range export, optional DuckDB decision, or low-disk/corruption matrix.
- No enhanced widget/dashboard, browser e2e, chart/table parity audit, or manual assistive-technology review.
- Fumadocs source exists, but its locked install, typecheck, build, route, axe, and link checks have not run.
- No owner/license/remote/package publication/Vercel/OpenSpec archive decision or action.

## Safety assertions

No dependency install, online resolution, commit, push, PR, publication, deploy, account/DNS/payment/permission change, secret setup, public service, hosted backend, runtime CDN, default remote telemetry, automatic remediation, keepalive, anti-idle, hidden reconnect, timeout bypass, quota circumvention, or OpenSpec sync/archive occurred.
