---
status: active
type: manifest
change: generalize-notebook-runtime-observer
tags:
  - manifest
  - planning
  - navigation
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Planning manifest

**Path:** `docs/planning/generalize-notebook-runtime-observer/manifest.md`  
**Purpose:** Inventory follow-on planning artifacts and recommended read order.  
**Status:** Active  

## Read order

1. Proposal and behavior delta specs.
2. Design and ADRs.
3. Product/context/research/architecture deep dives.
4. Tasks, task graph, traceability, risks, and validation.
5. Migration/support/naming strategy.
6. PLANS, outer loop, Goal, and Codex handoff.
7. Finalization report.

## Files

| Path | Purpose |
|---|---|
| `docs/planning/generalize-notebook-runtime-observer/PLANS.md` | Provide a self-contained living execution plan that can resume without chat history. |
| `docs/planning/generalize-notebook-runtime-observer/README.md` | Provide the human and agent entry point for the follow-on OpenSpec change. |
| `docs/planning/generalize-notebook-runtime-observer/architecture.md` | Give implementers a precise component, control-flow, data-flow, failure, migration, and ownership model for the neutral core and first-party platform adapters. |
| `docs/planning/generalize-notebook-runtime-observer/codex-handoff.md` | Provide the compact execution packet, read-first paths, write boundaries, task start, validation, output, and stop rules. |
| `docs/planning/generalize-notebook-runtime-observer/compatibility-migration.md` | Preserve current Colab API/defaults and legacy artifacts while adding profiles, scopes, adapters, and support evidence. |
| `docs/planning/generalize-notebook-runtime-observer/context-map.md` | Map authoritative source paths, current facts, assumptions, decisions, exclusions, and context-loading triggers. |
| `docs/planning/generalize-notebook-runtime-observer/decision-log.md` | Index accepted and deferred architecture/product decisions for the follow-on change. |
| `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-010-use-a-separate-follow-on-openspec-change.md` | Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger. |
| `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-011-use-a-faceted-runtime-profile-and-internal-adapter-registry.md` | Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger. |
| `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-012-make-measurement-scope-first-class-and-server-evidence-optional.md` | Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger. |
| `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-013-keep-semantic-static-display-as-the-universal-baseline.md` | Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger. |
| `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-014-separate-active-working-storage-from-finalized-artifacts.md` | Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger. |
| `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-015-gate-support-tiers-on-representative-evidence.md` | Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger. |
| `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-016-keep-one-colab-first-distribution-and-defer-neutral-naming.md` | Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger. |
| `docs/planning/generalize-notebook-runtime-observer/display-transport.md` | Define the universal static baseline, capability negotiation, enhanced transport boundaries, and accessibility parity. |
| `docs/planning/generalize-notebook-runtime-observer/finalization-report.md` | Record planning-pack completion, evidence status, implementation blockers, release decision, and maintenance/reopen policy. |
| `docs/planning/generalize-notebook-runtime-observer/goal-prompts.md` | Provide bounded Codex and generic-agent prompts grounded to the follow-on OpenSpec artifacts. |
| `docs/planning/generalize-notebook-runtime-observer/goal.md` | Define a bounded OpenSpec-grounded long-running implementation objective, lifecycle controls, validation loop, and stops. |
| `docs/planning/generalize-notebook-runtime-observer/grill-me.md` | Record material questions, recommended defaults, inferred decisions, blockers, and artifact impact for this change. |
| `docs/planning/generalize-notebook-runtime-observer/implementation-plan.md` | Turn the behavior and design decisions into dependency waves, milestones, validation gates, rollback, and adoption strategy. |
| `docs/planning/generalize-notebook-runtime-observer/jupyter-server-extension-boundary.md` | Bound the optional server-level evidence spike, security posture, interoperability question, and no-go criteria. |
| `docs/planning/generalize-notebook-runtime-observer/manifest.md` | Inventory follow-on planning artifacts and recommended read order. |
| `docs/planning/generalize-notebook-runtime-observer/measurement-scope.md` | Prevent notebook, kernel, process, container, server, host, capacity, and quota evidence from being conflated. |
| `docs/planning/generalize-notebook-runtime-observer/naming-packaging-strategy.md` | Define when to retain `nbops`, when a neutral identity may be justified, and how to avoid package fragmentation. |
| `docs/planning/generalize-notebook-runtime-observer/outer-loop.md` | Provide a 5-wave, 25-task execution and reassessment controller for implementation and representative evidence. |
| `docs/planning/generalize-notebook-runtime-observer/platform-support-matrix.md` | Separate product priority, detected capabilities, current evidence, intended tier, blockers, and promotion gates. |
| `docs/planning/generalize-notebook-runtime-observer/product-brief.md` | Define the target product, users, differentiated value, non-goals, and staged support strategy. |
| `docs/planning/generalize-notebook-runtime-observer/requirements-map.md` | Index every follow-on requirement, scenario set, task mapping, and acceptance posture. |
| `docs/planning/generalize-notebook-runtime-observer/research.md` | Synthesize current ecosystem and platform evidence into concrete OpenSpec and architecture implications. |
| `docs/planning/generalize-notebook-runtime-observer/risk-register.md` | Track product, architecture, migration, security, evidence, support, and naming risks with mitigations and triggers. |
| `docs/planning/generalize-notebook-runtime-observer/runtime-profile-model.md` | Define the canonical profile facets, evidence model, conflict handling, serialization, privacy, and compatibility expectations. |
| `docs/planning/generalize-notebook-runtime-observer/source-registry.md` | Record source-backed platform facts, confidence, implications, conflicts, and recheck triggers. |
| `docs/planning/generalize-notebook-runtime-observer/storage-profiles.md` | Define portable storage semantics, automatic-policy limits, platform mappings, write behavior, diagnostics, and validation. |
| `docs/planning/generalize-notebook-runtime-observer/task-graph.json` | Planning artifact |
| `docs/planning/generalize-notebook-runtime-observer/task-graph.md` | Provide the human-readable dependency waves, critical path, parallelization rules, approvals, and machine-graph link. |
| `docs/planning/generalize-notebook-runtime-observer/traceability-matrix.md` | Map every requirement to scenarios, implementation/validation tasks, evidence class, risk, and current status. |
| `docs/planning/generalize-notebook-runtime-observer/validation.md` | Define structural, semantic, deterministic, simulated, representative-runtime, accessibility, security, packaging, migration, and human-review gates. |
| `docs/planning/generalize-notebook-runtime-observer/validation-evidence.json` | Machine-readable executed evidence, blockers, and manifest-contract boundary. |

## Boundaries

- These artifacts are proposed planning state, not implementation evidence.
- The baseline change remains authoritative for current implemented Colab behavior.
- External platform facts are dated and require recheck at implementation/support promotion.
- No install, external runtime, naming, publishing, deployment, or archive action is authorized by this manifest.

- `platform-adapter-contract.md` - adapter contract deep dive.

- `platform-diagnostics.md` - platform diagnostic activation model.

| `openspec-grounding.md` | OpenSpec authority and downstream reconciliation map | Evidence |

| `diagram-index.md` | Diagram inventory, grounding, and text fallbacks | Navigation |

| `codex-tooling.md` | Bounded Codex/Goal/subagent/tooling proposal | Execution |

| `qa-checklist.md` | Planning, compatibility, security, runtime, accessibility, and release checks | Validation |
