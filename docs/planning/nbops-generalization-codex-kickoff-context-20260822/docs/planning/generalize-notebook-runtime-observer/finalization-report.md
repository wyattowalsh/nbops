---
status: final-with-known-risks
type: finalization-report
change: generalize-notebook-runtime-observer
tags:
  - finalization
  - validation
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Finalization report: `nbops` naming revision

## Decision

The planning and Codex kickoff identity revision is complete. Product implementation has not started.

The exact canonical current identity is `nbops`. The stable historical change ID `build-colab-observer` and its evidence paths remain intact. Implementation now freezes behavior in TASK-103, adopts `nbops` in TASK-104, and only then begins runtime-profile and adapter work.

## Material repairs

- Accepted ADR-016 for the pre-public `nbops` identity.
- Added the `package-identity` behavior domain.
- Rewrote migration compatibility around canonical `nbops` behavior and stable historical provenance.
- Reconciled TASK-103, TASK-104, TASK-142, TASK-145, and downstream dependency/write-scope guidance.
- Updated kickoff, Goal, handoff, PLANS, validation, traceability, risks, manifests, and ZIP identity.
- Removed previously considered candidate-name literals and deferred-renaming contradictions from active surfaces.

## Current counts

- Domains: 10
- Requirements: 30
- Scenarios: 60
- Tasks: 44
- Accepted follow-on ADRs: 7

## Evidence status

| Surface | Status |
|---|---|
| Active identity convergence | PASS |
| OpenSpec and task machine schemas | PASS |
| Links, JSON/YAML, manifests, and ZIP integrity | PASS |
| Product implementation | BLOCKED: not part of this artifact-only request |
| Managed runtimes, Python matrix, manual accessibility | BLOCKED: unavailable evidence surfaces |
| External repository, registry, domain, publication, deployment | BLOCKED: separate approval and ownership lifecycle |

## Residual risks

- Preliminary namespace checks are not ownership, legal, or trademark clearance.
- Target-repository evidence determines whether a temporary prior-import shim is necessary.
- Representative runtimes may change support tiers and platform copy, but not the accepted `nbops` identity unless a new explicit decision supersedes ADR-016.

## Reopen triggers

Reopen planning for a material implementation discovery, failed validation, authoritative identity conflict, unsafe drift, representative runtime finding that changes behavior, or explicit user request.
