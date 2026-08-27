---
status: active
type: decision-log
change: build-colab-observer
tags:
  - decisions
  - adr
updated: 2026-08-21
cssclasses:
  - planning-doc
---

# Decision log

| ADR | Decision | Status | Primary tradeoff |
|---|---|---|---|
| [[docs/planning/build-colab-observer/decisions/ADR-001-repository-shape|ADR-001]] | One product package + private UI/docs workspaces | Proposed | Cross-language build versus product coherence |
| [[docs/planning/build-colab-observer/decisions/ADR-002-ui-transport|ADR-002]] | Enhanced widget + static fallback | Proposed | Two paths versus Colab resilience/accessibility |
| [[docs/planning/build-colab-observer/decisions/ADR-003-storage|ADR-003]] | SQLite default, DuckDB optional | Proposed | Zero-extra durability versus analytical convenience |
| [[docs/planning/build-colab-observer/decisions/ADR-004-sampler|ADR-004]] | Daemon thread + bounded queue | Proposed | Thread-safety versus notebook event-loop conflicts |
| [[docs/planning/build-colab-observer/decisions/ADR-005-frontend|ADR-005]] | Preact + ECharts SVG spike | Spike-gated | Bundle size versus chart capability |
| [[docs/planning/build-colab-observer/decisions/ADR-006-diagnostics|ADR-006]] | Deterministic evidence rules | Proposed | Explainability versus adaptive models |
| [[docs/planning/build-colab-observer/decisions/ADR-007-python-tooling|ADR-007]] | uv workflow; build backend decided by wheel spike | Proposed | Avoid premature backend commitment |
| [[docs/planning/build-colab-observer/decisions/ADR-008-privacy|ADR-008]] | Local/no-telemetry/redacted defaults | Proposed | Support richness versus user trust |
| [[docs/planning/build-colab-observer/decisions/ADR-009-artifact-naming|ADR-009]] | Separate logical run identity from filesystem artifact naming | Accepted | Readable safe names versus deterministic containment for unsafe IDs |
| [[docs/planning/build-colab-observer/decisions/ADR-010-generalization-sequencing|ADR-010]] | Generalize through a separate follow-on OpenSpec change | Accepted for planning | Extra coordination versus preserving baseline evidence and reversible migration |

A decision becomes accepted during implementation preflight only after target-repository evidence and validation are recorded.
