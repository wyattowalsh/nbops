---
status: proposed
type: openspec-proposal
change: build-colab-observer
tags:
  - openspec
  - proposal
  - product
updated: 2026-08-21
cssclasses:
  - planning-doc
---

# Proposal: Build `colab-observer`

**Path:** `openspec/changes/build-colab-observer/proposal.md`  
**Purpose:** Define the product intent, scope, impact, risks, and success criteria for the first production-grade release.  
**Status:** Proposed

## Intent

Build an open-source, local-first, notebook-native observability package for Google Colab. A notebook user installs one Python package, starts an observer without surrendering notebook control, sees live and accessible runtime health, receives evidence-based diagnostics, and exports a portable report bundle for later debugging.

The product is `colab-observer`. The documentation site, CI/CD, Vercel deployment, nested `AGENTS.md` files, and planning vault exist to support that product rather than replace it.

## Scope

### In scope

- A publishable Python package with stable configuration, lifecycle, display, and export entry points.
- Runtime, CPU, memory, disk, network, process, NVIDIA GPU, framework, and best-effort TPU observations.
- A notebook-inline dashboard with accessible live summaries, charts, tables, filters, drilldowns, diagnostics, and exports.
- Local persistence and portable CSV, JSONL, database, Markdown, HTML, and zip outputs.
- Evidence-bearing, non-automated diagnostics for common Colab bottlenecks and resource risks.
- A safe three-cell Colab snippet and example notebooks.
- A Fumadocs documentation site using a shadcn-aligned Tailwind theme, with accessible UX and AI-readable exports.
- Pre-commit, CI, package/release checks, nested agent instructions, and approval-gated Vercel/PyPI delivery plans.

### Out of scope

- Keepalive, anti-idle, reconnect automation, timeout bypass, activity simulation, quota circumvention, or any attempt to influence Colab allocation policy.
- A required hosted backend, account, API key, or public dashboard URL.
- Remote command execution, notebook-content capture, environment-secret capture, or default upload of telemetry.
- Automatic remediation of performance findings or automatic deletion/migration of user files.
- A full experiment-tracking platform, scheduler, distributed tracing system, or replacement for W&B, MLflow, Prometheus, Grafana, or vendor profilers.
- Reliable low-level TPU utilization telemetry where the active runtime does not expose it.
- Deployment, package publishing, cloud/account changes, secrets setup, commits, or pull requests during this planning change.

## Approach

1. Keep the core lightweight and local-first; isolate optional accelerator, UI, database, and integration capabilities behind extras.
2. Establish one versioned observation schema and collector contract before implementing individual collectors.
3. Run sampling independently of notebook cell execution, isolate collector failures, and expose sampling lag and capability quality.
4. Persist durable raw observations locally; send only bounded deltas to the live UI.
5. Treat the enhanced widget dashboard as progressive enhancement over a static notebook summary and semantic data tables.
6. Produce deterministic diagnostics with thresholds, windows, hysteresis, confidence, evidence, and safe remediation guidance.
7. Build docs, automation, and agent guidance around the same public contracts and acceptance tests.

## Capabilities

- `runtime-observability` — bounded lifecycle, status, sampling, and run context.
- `metrics-collectors` — capability-aware resource and framework observations.
- `notebook-snippet` — copyable, rerunnable, safe Colab adoption path.
- `dashboard-ux` — local notebook dashboard, drilldowns, controls, and fallbacks.
- `accessibility` — WCAG 2.2 AA target and equivalent non-chart access to data.
- `diagnostics` — evidence-bearing bottleneck and pressure findings.
- `export-reporting` — local, redacted, portable data and report outputs.
- `docs-site` — product documentation, discovery, API reference, and AI-readable surfaces.
- `quality-automation` — pre-commit and reproducible local quality gates.
- `ci-cd` — least-privilege continuous integration and approval-gated delivery.
- `security-policy` — privacy, supply-chain, subprocess, and Colab-policy boundaries.

## Impact

| Area | Expected impact |
|---|---|
| Notebook users | Faster diagnosis of stalls, memory pressure, accelerator underuse, and storage risks without leaving Colab. |
| Package surface | New public API and versioned observation/export schemas that require compatibility discipline. |
| Runtime overhead | A bounded background sampler and UI update loop consume some CPU, memory, and I/O; overhead must be observable and configurable. |
| Privacy | Process and environment observations can expose sensitive metadata unless defaults are redacted and collection is minimized. |
| Documentation | Product docs must keep examples, public API, schema, diagnostics, and policy boundaries release-aligned. |
| Delivery | CI and deployments introduce supply-chain and secret-boundary risks that require least privilege and approvals. |

## Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Monitor meaningfully distorts the workload | High | Bounded cadence, asynchronous persistence, self-observation, lag reporting, performance budgets, soak tests. |
| Colab widget behavior changes | High | Static HTML/table fallback, adapter boundary, no server/port requirement, documented capability detection. |
| Metrics imply false precision | High | Unit/source/quality metadata, unavailable/estimated states, explicit limitations, confidence-bearing diagnostics. |
| Sensitive process or environment data leaks | High | Data minimization, redaction, opt-in command-line/package capture, local-only defaults, export preview. |
| Diagnostics create harmful certainty | Medium/High | Use “possible/likely” language, evidence windows, no automatic remediation, user-disable controls. |
| Frontend assets create supply-chain exposure | Medium | Locally bundled assets, lockfiles, pinned CI actions, wheel-content tests, no runtime CDN. |
| Scope turns into a general observability platform | Medium | Preserve Colab/notebook-first non-goals and defer hosted/multi-node features. |

## Open Questions

- QUESTION-001: Recheck the `colab-observer` name on PyPI and GitHub immediately before publication; exact paths returned not-found during the 2026-07-11 research pass but availability is not reserved.
- QUESTION-002: Validate the enhanced widget transport against representative current Colab runtimes before freezing the first stable UI compatibility promise.
- QUESTION-003: Validate the proposed Python 3.11–3.13 support matrix. The current documented Colab 2026.04 runtime uses Python 3.12.13, but only direct matrix and real-Colab evidence can freeze the release claim.
- QUESTION-004: Decide whether DuckDB is an optional extra in the first release or follows after the SQLite-backed MVP.

## Success Criteria

- A user can start monitoring from a clean Colab runtime through one documented install/start cell and can continue running notebook cells.
- The observer records core CPU, memory, disk, network, runtime, and process signals on CPU-only runtimes; unavailable accelerators do not fail the session.
- NVIDIA runtime users receive GPU/VRAM observations through a primary provider or a safe fallback with provenance and quality labels.
- The dashboard works without a public endpoint and every chart has an equivalent accessible table or textual summary.
- Stopping and exporting are idempotent; the resulting bundle is locally inspectable, redacted by default, and manifest/checksum verified.
- Diagnostic findings name evidence, severity, confidence, duration, and a non-destructive remediation suggestion.
- No product path contains keepalive, anti-idle, reconnect, timeout-bypass, or quota-circumvention behavior.
- Unit, integration, notebook smoke, dashboard accessibility, docs, package-build, security, and OpenSpec checks are designed and represented in CI.
- The implementation handoff is bounded by task IDs, write scopes, validations, and approval stops.

## Follow-on generalization boundary

This change remains the Colab-first implementation baseline. Broader Python notebook runtime architecture is proposed separately in [`generalize-notebook-runtime-observer`](../generalize-notebook-runtime-observer/proposal.md).

The follow-on change MUST preserve the public API, canonical three-cell Colab workflow, current defaults, local-only security posture, and legacy artifact readability defined here. It may extract platform-neutral internals and add evidence-gated adapters, but it does not retroactively broaden this change's support claims or implementation status.

No requirement in `build-colab-observer` is modified merely by the existence of the follow-on plan. Any behavior change discovered during generalization must be reconciled explicitly through the appropriate OpenSpec artifact before implementation.
