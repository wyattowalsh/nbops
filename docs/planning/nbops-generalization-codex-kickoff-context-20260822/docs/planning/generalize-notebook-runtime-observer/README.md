---
status: active
type: project-brief
change: generalize-notebook-runtime-observer
tags:
  - planning
  - read-first
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Planning brief: adopt `nbops` and generalize notebook runtime observability

**Path:** `docs/planning/generalize-notebook-runtime-observer/README.md`  
**Purpose:** Human and agent entry point for the approved identity migration and follow-on architecture change.  
**Status:** Active

## Objective

Move the hardened Colab-first implementation into the canonical `nbops` package and then generalize its runtime-profile, adapter, storage, display, diagnostics, and support-evidence architecture without weakening existing behavior or overclaiming platform scope.

## Decisions

- Canonical product/distribution/import/CLI/default-artifact identity: `nbops`.
- Google Colab remains the flagship adapter.
- Historical `build-colab-observer` paths remain stable provenance.
- One distribution, one platform-neutral core, no per-platform forks.
- Static text/semantic HTML/table/CSV remains the universal correctness path.
- Support tiers require representative evidence.

## Critical implementation sequence

```text
TASK-103 freeze supported Colab behavior and legacy evidence
TASK-104 approve nbops canonical identity                    complete
TASK-105 freeze nbops migration fixtures
TASK-106 implement nbops package/import/CLI/artifact migration
TASK-110+ runtime-profile and adapter foundation
```

## Scope summary

| Included | Excluded without separate approval |
|---|---|
| `nbops` local package/import/CLI/artifact migration | Remote repository rename or registry publication |
| Generic Python/IPython core | Non-Python kernels |
| Colab adapter extraction | Hosted backend or telemetry |
| Jupyter and Deepnote evidence-gated targets | Blanket “all Jupyter” support |
| Storage and display capability profiles | Automatic server extension installation |
| Legacy import/artifact compatibility fixtures | Silent storage mounts or account APIs |
| Optional authenticated server-provider spike | Keepalive, timeout bypass, quota circumvention |

## Read order

1. `proposal.md` and `specs/package-identity/spec.md`
2. `ADR-016-adopt-nbops-before-first-publication.md`
3. `naming-packaging-strategy.md`
4. `compatibility-migration.md`
5. `design.md` and remaining specs
6. `tasks.md` and `task-graph.json`
7. `validation.md` and `traceability-matrix.md`
8. `PLANS.md`, `outer-loop.md`, and `codex-handoff.md`

## Planning state

| Surface | State |
|---|---|
| OpenSpec domains | 10 |
| Behavior requirements | 30 |
| Scenarios | Recounted by validation after final content settles |
| Tasks | 44 |
| Planning tasks complete | TASK-100, TASK-101, TASK-102, TASK-104 |
| Product implementation | Not started for this change |
| Identity implementation | Starts after TASK-103 and TASK-105 |
| Representative Jupyter/Deepnote/managed-Colab evidence | Blocked until runtime access |
| Remote publication/repository operations | Approval-gated |

## Definition of done for this planning revision

- [x] `nbops` is canonical in active proposal/spec/design/tasks/plans/handoff.
- [x] Package identity is behavior-specified and traceable.
- [x] Legacy identifiers are classified as history/compatibility rather than current branding.
- [x] Task dependencies put migration before adapter extraction.
- [x] Kickoff prompt permits bounded local identity migration but blocks external publication actions.
- [ ] Implementation and representative runtime evidence, intentionally future work.
