---
status: ready
type: decisions
change: build-colab-observer
tags:
  - adr
  - architecture
  - tradeoffs
updated: 2026-07-11
cssclasses:
  - planning-doc
---
# Architecture decision records

## ADR-001: Product-centered single distribution

**Status:** Proposed  
**Decision:** Begin with one Python distribution and optional extras, plus a separate docs application in the same repository.  
**Why:** One installation is the adoption path; internal modules remain separable without premature multi-package release complexity.  
**Alternatives:** multiple packages; docs-first monorepo; hosted service.  
**Review trigger:** independent teams/releases, dependency conflicts, or extension ecosystem requirements.

## ADR-002: SQLite core; DuckDB deferred

**Status:** Accepted for the unpublished development line  
**Decision:** Use SQLite as the canonical durable run store and range-aware CSV/JSONL/summary exports as the initial analytical surface. Defer a DuckDB adapter until approved dependency and representative Colab evidence demonstrate net value.  
**Why:** Zero extra database dependency, transactions, portable artifacts, and sufficient local single-writer evidence.  
**Tradeoff:** Large analytical queries may eventually benefit from DuckDB; exported schemas preserve that future option.  
**Validation:** local WAL/backup/corruption/low-disk/range-export tests pass; revisit after representative install, wheel-size, startup, and query measurements.

## ADR-003: Tiered accessible dashboard

**Status:** Accepted for the local static baseline; enhanced transport provisional  
**Decision:** Use semantic text/table output plus a polished script-free SVG dashboard as the correctness path. Keep any richer transport optional and local-only.  
**Why:** Colab compatibility and accessibility survive transport or browser failure.  
**Alternative rejected:** Gradio/public server as core due lifecycle, tunnel, privacy, and accessibility complexity.  
**Validation:** static chart/table parity and malicious-text tests pass; real Colab keyboard/AT checks remain required.

## ADR-004: Passive framework adapters

**Status:** Accepted for the local development line  
**Decision:** Observe frameworks only when already loaded; the observer does not import or install an absent framework solely for monitoring.  
**Why:** Monitoring must not initialize CUDA/XLA or distort the workload.  
**Validation:** unit tests assert absent modules remain absent; local selected-workload smoke passes for installed PyTorch and JAX with no observer-triggered import of the other frameworks. TensorFlow is absent and is reported as unavailable rather than installed.

## ADR-005: Local staging before Drive

**Status:** Proposed  
**Decision:** Keep active DB and write queue on local runtime storage; checkpoint/copy finalized artifacts to Drive.  
**Why:** Avoid slow/transient mounted storage in the sampling hot path.  
**Validation:** interrupted copy, retry, partial marker, and latency benchmark.

## ADR-006: Rules with windows, hysteresis, and evidence

**Status:** Proposed  
**Decision:** Diagnostics use deterministic rule envelopes and lifecycle states.  
**Why:** Transparent, testable, and less likely to overclaim than opaque scoring.  
**Review trigger:** a validated learned model produces material gains with equal explainability/privacy.

## ADR-007: Fumadocs with shadcn/Tailwind v4

**Status:** Directed by user, implementation pending  
**Decision:** Use Fumadocs and its shadcn preset with Tailwind CSS v4; isolate component primitives behind local wrappers.  
**Why:** Advanced product/API docs, built-in docs patterns, and current requested stack.  
**Validation:** current version check, production build, search, a11y, metadata, and Vercel preview.

## ADR-008: Vercel Git preview, protected promotion

**Status:** Proposed  
**Decision:** Prefer Vercel Git integration over a credential-heavy CLI workflow.  
**Why:** Native previews and simpler secret posture; GitHub CI remains independent validation.  
**Validation:** preview protection, deployment checks, production rollback rehearsal.  
**Approval:** project connection, deploy, domain, and environment changes require user approval.


## ADR-009: Direct Colab comm candidate; custom widget manager rejected as default

**Status:** Accepted for an experimental spike; production selection deferred  
**Decision:** Do not use Colab's current custom-widget-manager activation as the default because the inspected implementation loads a hosted manager asset. Test an explicit, self-contained direct kernel-comm bridge instead, while preserving the static dashboard.  
**Why:** This is the smallest candidate compatible with the no-runtime-CDN, no-public-endpoint, and no-hidden-reconnect invariants.  
**Alternatives considered:** current Colab custom widget manager; generic ipywidgets/anywidget embedding; localhost/Gradio server; static-only.  
**Consequences:** Python and TypeScript protocol candidates and a local comm spike can be tested now, but automatic activation and compatibility claims remain blocked on managed-Colab/browser evidence.  
**Validation:** JSON Schema, fake comm, malformed-control, privacy, Node syntax, no-network-pattern, and static fallback tests; real CPU/NVIDIA Colab and manual accessibility remain the promotion gate.  
**Review trigger:** Colab changes its comm or widget-manager implementation, a fully local supported transport appears, or managed-Colab tests fail.
