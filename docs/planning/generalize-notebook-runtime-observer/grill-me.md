---
status: active
type: grill-me
change: generalize-notebook-runtime-observer
tags:
  - grill-me
  - decisions
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# `/grill-me` protocol

Inspect evidence before asking. Ask one material question only when the answer changes architecture, behavior, compatibility, security, privacy, acceptance, packaging, or release state and cannot be inferred safely. Include the recommended answer, consequences, blocker status, and affected artifacts.

## Settled decisions

| Question | Recommended/default answer | State | Artifact impact |
|---|---|---|---|
| Canonical current identity? | Exact lowercase `nbops` | Accepted | ADR-016, identity spec, package migration, kickoff |
| Google Colab role? | Flagship adapter, not umbrella identity | Accepted | product brief, support matrix, docs copy |
| Per-platform packages? | No, one `nbops` distribution | Accepted | architecture, packaging, tasks |
| Prior import shim? | Only when verified external usage requires it | Evidence-gated | migration spec, TASK-104 |
| External publication now? | No, run readiness checks and obtain explicit approval first | Blocked by separate lifecycle | TASK-145 |

## Session cadence

Run `/grill-me`:

- at session start;
- after TASK-103;
- after TASK-104;
- after each implementation wave;
- before support-tier promotion;
- before external publication readiness review;
- before finalization;
- whenever confidence, scope, or marginal utility changes.

## Marginal-utility gate

Continue for evidence, compatibility, correctness, security, accessibility, traceability, migration safety, and support-claim truthfulness. Defer cosmetic churn, speculative adapters, public plugin APIs, and external identity actions lacking evidence or approval.
