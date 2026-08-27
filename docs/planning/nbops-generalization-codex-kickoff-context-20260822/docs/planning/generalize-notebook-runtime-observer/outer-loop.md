---
status: active
type: outer-loop
change: generalize-notebook-runtime-observer
tags:
  - outer-loop
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Outer loop

## Iteration objective

Freeze supported behavior, migrate current identity to `nbops`, then begin the platform-neutral runtime-profile foundation without unsupported support claims.

## Current queue

| Order | Task | Status | Evidence/unblocker |
|---:|---|---|---|
| 1 | TASK-103 freeze Colab behavior and legacy compatibility | Next | Target repository and focused fixtures |
| 2 | TASK-105 freeze `nbops` migration fixtures | Planned | TASK-103 plus accepted identity spec |
| 3 | TASK-106 implement `nbops` migration | Planned | TASK-105 green |
| 4 | TASK-110 runtime-profile models | Blocked by dependency | TASK-106 green |
| 5 | TASK-111 evidence validation | Blocked by dependency | TASK-110 |
| 6 | TASK-112 adapter registry | Blocked by dependency | TASK-111 |
| 7 | Continue dependency-ready tasks | Planned | `tasks.md` and `task-graph.json` |

## Completed this planning loop

- Canonical `nbops` identity approved and behavior-specified.
- ADR-016 superseded and replaced.
- Package identity domain added.
- Migration tasks inserted before runtime-profile extraction.
- Kickoff, Goal, handoff, validation, traceability, manifests, and bundle naming reconciled.

## Blocked or deferred

- Representative managed Colab, Jupyter, Deepnote, JupyterHub/server, and assistive-technology evidence.
- Python 3.11/3.12 execution.
- Reviewed dependency locks and unavailable quality/docs tools.
- Remote repository rename, registry publication, domains/handles, external announcements, deployment, secrets, permissions, and OpenSpec apply/sync/archive.

## Reassessment

After each task or wave:

1. Compare observed behavior with OpenSpec.
2. Recheck identity convergence and legacy boundaries.
3. Recheck platform/scope/support claims.
4. Run focused then full applicable validation.
5. Update PLANS, traceability, risks, and exact blockers.
6. Continue only while the next task has positive material value and a safe write scope.

## Stop conditions

Stop for unapproved breaking behavior, missing required evidence, overlapping writes, install/network/remote/account actions, publication, or validation failure without a bounded repair.
