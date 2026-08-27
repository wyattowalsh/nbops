---
status: active
type: diagram-index
change: build-colab-observer
tags:
  - diagrams
  - mermaid
  - navigation
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Diagram index

| Diagram | Location | Purpose | OpenSpec/validation anchor |
|---|---|---|---|
| Product system map | `START_HERE.md` | Orient product and support surfaces | proposal and design |
| Product boundaries | `product-brief.md` | Show local-first trust boundary | security-policy spec |
| Architecture/data flow | `architecture.md`, `design.md` | Explain lifecycle, collectors, store, diagnostics, UI, export | design decisions |
| Metric pipeline | `metrics-model.md` | Explain provenance and quality semantics | metrics-collectors spec |
| Collector state | `collector-design.md` | Explain discovery and degradation | collector requirements |
| Dashboard hierarchy | `dashboard-ux.md` | Explain primary interaction model | dashboard and accessibility specs |
| Transport decision | `widget-transport-spike.md` | Separate supported static output from the experimental direct-comm candidate | dashboard/security specs and managed-Colab gate |
| Diagnostic evaluation | `diagnostics-rules.md` | Explain deterministic rule lifecycle | diagnostics spec |
| Documentation graph | `docs-site-plan.md` | Explain docs routes and outputs | docs-site spec |
| CI/release gates | `ci-cd-plan.md`, `quality-automation.md` | Explain validation and approval flow | quality and CI specs |
| OpenSpec lifecycle | `openspec-grounding.md` | Prevent derived-artifact drift | all OpenSpec artifacts |
| Task dependency graph | `task-graph.md`, `tasks.md` | Sequence implementation | tasks |
| Goal lifecycle | `goal.md` | Bound long-running agent work | handoff and validation |
| Outer loop | `outer-loop.md` | Carry implementation queue and stops | PLANS/continuation |
| Finalization flow | `finalization-report.md` | Show final planning gate | validation and bundle |

All Mermaid blocks use the shared init/style inserted during final normalization. Canvas provides an alternate overview, and tables/text remain the precise fallback.
