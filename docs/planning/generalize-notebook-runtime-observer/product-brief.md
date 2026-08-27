---
status: accepted
type: planning
change: generalize-notebook-runtime-observer
tags:
  - product
  - nbops
  - notebook-observability
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Product brief: `nbops`

## Product definition

`nbops` is local-first runtime observability for Python notebooks. It observes the Python runtime, visible process tree, container-visible system evidence, accelerators, frameworks, storage characteristics, diagnostics, and explicitly authorized optional server evidence.

It does not assume the kernel owns the notebook document, Jupyter server, sibling kernels, workspace quota, scheduler, or physical host.

## Positioning

> **`nbops`: local-first runtime observability for Python notebooks.**

> **`nbops` for Google Colab** is the flagship platform experience.

## Primary users

| User | Job | Truth boundary |
|---|---|---|
| Colab ML practitioner | Diagnose stalls, pressure, GPU underuse, and storage risk | Provider/container-visible evidence, no allocation guarantees |
| Local Jupyter user | Inspect the current kernel/process tree over time | No server/host claim without evidence |
| JupyterHub user | Capture evidence without admin rights | Kernel-local baseline; optional authenticated server evidence |
| Deepnote user | Diagnose workload and storage behavior | Distinguish active working storage from durable artifact destination |
| Maintainer/support engineer | Receive a portable redacted bundle | Preserve profile, scope, identity, limitations, and integrity |
| Agent/automation | Read deterministic local evidence | No hidden control, network, or remediation authority |

## Differentiated value

- Bounded historical time series.
- Source, quality, freshness, and measurement scope.
- GPU and framework evidence.
- Deterministic diagnostics with alternatives and limitations.
- Semantic chart/summary/table/CSV parity.
- Local persistence and integrity-checked support bundles.
- Explicit redaction and partial-loss evidence.
- No account, backend, public endpoint, or default telemetry.
- Rerun-safe notebook lifecycle and truthful degraded behavior.

## Product principles

1. Scope precedes number.
2. Unknown is not zero; absent limits are not unlimited.
3. Detection is not support.
4. Capabilities compose across provider, frontend, kernel, storage, and transport facets.
5. Static semantic output is the universal correctness path.
6. Adapters are passive, bounded, and failure-isolated.
7. Support labels are evidence-backed.
8. `nbops` is the canonical identity; historical names are provenance only.
9. Google Colab remains the flagship adapter.
10. One distribution avoids fragmentation.
