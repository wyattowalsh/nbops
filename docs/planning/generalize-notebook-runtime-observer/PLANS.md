---
status: active
type: plans
change: generalize-notebook-runtime-observer
tags:
  - plans
  - nbops
  - implementation
updated: 2026-08-26
cssclasses:
  - planning-doc
---

# PLANS: adopt `nbops` and generalize the notebook runtime observer

## Objective

Implement one platform-neutral `nbops` core while preserving supported Google Colab behavior, legacy artifact readability, semantic static fallback, local-first privacy, and evidence-gated platform support.

## Current state

- Historical baseline `build-colab-observer`: preserved as provenance in this repository.
- Follow-on change `generalize-notebook-runtime-observer`: implementation started in
  `wyattowalsh/nbops` (operations catalog already present on `main` is retained).
- Canonical identity decision: accepted as `nbops`.
- Completed planning tasks: TASK-100, TASK-101, TASK-102, TASK-104.
- Completed implementation slice: TASK-103, TASK-105, TASK-106, TASK-110, TASK-111,
  TASK-112, TASK-113.
- Target-repository reconciliation: FastAPI stays at `nbops.api:app`; observer
  library API lives in `nbops.observer` / `nbops.config`. No `colab_observer`
  shim (no verified external import obligation).
- Next task: TASK-114 persist profile and scope, then TASK-115 / TASK-120+.

## Milestones

| Milestone | Tasks | Outcome |
|---|---|---|
| M1 behavior freeze | TASK-103 | Supported behavior and artifacts are captured independently of the prior package path |
| M2 identity migration | TASK-104 | Current package/import/CLI/docs/default/new-artifact identity converges on `nbops` |
| M3 profile foundation | TASK-110 through TASK-115 | Faceted runtime profile, evidence, adapter registry, support tiers, persistence, inspection |
| M4 environment adapters | TASK-120 through TASK-128 | Generic Python, IPython, Colab, storage, Deepnote/Jupyter preview, diagnostics |
| M5 display and migration | TASK-130 through TASK-146 | Semantic parity, transport isolation, schema/artifact migration, examples, publication readiness |
| M6 representative validation | TASK-150 through TASK-158 | Runtime, security, performance, accessibility, and release decision evidence |

## Progress

- [x] TASK-100 audit current coupling
- [x] TASK-101 research platform boundaries
- [x] TASK-102 write follow-on contracts
- [x] TASK-103 freeze pre-`nbops` behavior fixtures
- [x] TASK-104 adopt `nbops` canonical identity
- [x] TASK-105 freeze nbops migration fixtures
- [x] TASK-106 implement nbops identity migration
- [x] TASK-110 implement runtime-profile models
- [x] TASK-111 implement evidence validation
- [x] TASK-112 implement adapter registry
- [x] TASK-113 implement support-tier evaluator
- [ ] TASK-114 persist profile and scope

## Decisions

| Date | Decision | Rationale | Review trigger |
|---|---|---|---|
| 2026-08-21 | Separate follow-on OpenSpec change | Preserve baseline evidence and stage truth | Material baseline defect |
| 2026-08-21 | One platform-neutral core with internal adapters | Avoid duplicated behavior and releases | Adapter isolation failure |
| 2026-08-21 | Static text/HTML is universal baseline | Accessibility and transport resilience | Representative evidence supports an additive transport |
| 2026-08-22 | Adopt exact canonical identity `nbops` now | Lowest pre-public migration cost and product truth | Explicit superseding decision before publication |
| 2026-08-22 | External publication is separately gated | Namespace signals are not ownership or legal clearance | Publication lifecycle begins |

## Validation log

Planning and kickoff bundle validation is recorded in `VALIDATION_REPORT.md` and `NBOPS_IDENTITY_AUDIT.json`. Product implementation validation begins with TASK-103.

## Recovery and rollback

- Planning changes can be reverted without product mutation.
- TASK-103 fixtures are the rollback surface for TASK-104.
- If identity migration fails, restore the last green source tree and artifact readers, not a partially moved package.
- Retain a prior import shim only when verified compatibility evidence requires it.

## Resumable next step

Read the kickoff prompt and complete TASK-103 within its exact write scope. Do not start adapter extraction until TASK-104 is green.
