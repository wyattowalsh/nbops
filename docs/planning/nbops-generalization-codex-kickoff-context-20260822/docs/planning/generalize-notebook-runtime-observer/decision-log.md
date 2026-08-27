---
status: active
type: decision-log
change: generalize-notebook-runtime-observer
tags:
  - decisions
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Decision log

| ADR | Decision | Status |
|---|---|---|
| ADR-010 | Use a separate follow-on OpenSpec change | Accepted |
| ADR-011 | Use a faceted runtime profile and internal adapter registry | Accepted |
| ADR-012 | Make measurement scope first-class and server evidence optional | Accepted |
| ADR-013 | Keep semantic static display as the universal baseline | Accepted |
| ADR-014 | Separate active working storage from finalized artifacts | Accepted |
| ADR-015 | Gate support tiers on representative evidence | Accepted |
| ADR-016 | Adopt `nbops` before first publication | Accepted |

## Current identity decision

`nbops` is fixed as the canonical local product, distribution, import, CLI, and repository identity. Google Colab remains the flagship adapter. External publication and ownership actions remain separately evidence- and approval-gated.

## Reconciliation rule

Any change to ADR-011 through ADR-016 requires rechecking proposal, behavior specs, design, tasks, migration, support tiers, validation, traceability, package artifacts, kickoff prompt, and manifests before implementation resumes.
