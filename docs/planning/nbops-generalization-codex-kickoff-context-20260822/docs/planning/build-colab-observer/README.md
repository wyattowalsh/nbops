---
status: active
type: planning-overview
change: build-colab-observer
tags:
  - overview
  - planning
  - implementation
updated: 2026-07-25
cssclasses:
  - planning-doc
---
# Planning overview: `build-colab-observer`

## Product hierarchy

1. Python runtime, collectors, stores, diagnostics, notebook UX, and portable evidence.
2. Representative Colab, privacy, performance, accelerator, and accessibility validation.
3. Promoted local-only interactive dashboard and complete examples.
4. Docs build, Vercel, release automation, and planning presentation.

## Current state

| Surface | State |
|---|---|
| OpenSpec | 11 domains, 73 requirements, 93 scenarios, 45 tasks, 9 ADRs |
| CPU-first package | Locally hardened and validated with 249 tests |
| Local security boundaries | Generated directories and export roots, publication temps, SQLite aliases, provider output, mounted-output normalization, and collector/discovery failures hardened |
| Static dashboard | Responsive script-free SVG and semantic-table fallback |
| Direct comm | Experimental, explicit, non-default, not promoted |
| Managed Colab | Not run |
| Release/deploy/archive | Not performed |

## Read order

1. [[docs/planning/build-colab-observer/runtime-boundary-hardening-20260717|Runtime-boundary evidence]]
2. [[docs/planning/build-colab-observer/final-assurance-hardening-20260716|Prior final-assurance evidence]]
3. [[openspec/changes/build-colab-observer/proposal|Proposal]]
4. [[openspec/changes/build-colab-observer/specs/runtime-observability/spec|Behavior specs]]
5. [[openspec/changes/build-colab-observer/design|Design]]
6. [[openspec/changes/build-colab-observer/tasks|Task state]]
7. [[docs/planning/build-colab-observer/traceability-matrix|Traceability]]
8. [[docs/planning/build-colab-observer/validation|Validation]]
9. [[docs/planning/build-colab-observer/PLANS|PLANS]]
10. [[docs/planning/build-colab-observer/outer-loop|Outer loop]]
11. [[docs/planning/build-colab-observer/codex-handoff|Handoff]]
12. [[CONTINUATION_PROMPT|Continuation]]

## Follow-on generalization

The current Colab-first product definition remains the implemented baseline. A separate additive change, [[openspec/changes/generalize-notebook-runtime-observer/proposal|`generalize-notebook-runtime-observer`]], plans a platform-neutral core, evidence-gated Jupyter/Deepnote adapters, explicit measurement scope, storage profiles, and a deferred naming decision. It does not reopen or rewrite this change.
