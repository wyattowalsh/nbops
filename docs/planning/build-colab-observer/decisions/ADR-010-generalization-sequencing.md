---
status: accepted-for-planning
type: adr
change: build-colab-observer
tags:
  - adr
  - architecture
  - migration
  - notebook-observability
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# ADR-010: Generalize through a separate follow-on change

**Path:** `docs/planning/build-colab-observer/decisions/ADR-010-generalization-sequencing.md`  
**Purpose:** Preserve the validated Colab-first baseline while planning a platform-neutral notebook runtime architecture.  
**Status:** Accepted for planning  
**Review trigger:** Representative non-Colab runtime evidence or an explicit public identity decision materially changes the boundary.

## Context

Most of the implemented package is platform-neutral, while Colab coupling is concentrated in runtime detection, `/content` and Drive behavior, TPU/Colab diagnostics, and the experimental direct-comm path. Folding broader notebook support into `build-colab-observer` would rewrite a final-assured baseline, blur current support evidence, and make migration/naming decisions difficult to review.

## Decision

Keep `build-colab-observer` as the Colab-first implementation and evidence baseline. Plan cross-platform generalization in a separate full-rigor OpenSpec change: `generalize-notebook-runtime-observer`.

The follow-on may refactor internals, add runtime-profile/scope/storage/display contracts, and introduce evidence-gated adapters. It must preserve the current public API, Colab defaults, local-first boundaries, and legacy artifact readers unless an explicit behavior change is separately approved.

## Alternatives considered

| Option | Advantages | Disadvantages | Outcome |
|---|---|---|---|
| Expand the existing change | One change directory | Rewrites baseline scope and obscures evidence history | Rejected |
| Separate follow-on change | Clear lifecycle, migration, validation, and rollback | Additional planning artifacts and coordination | Selected |
| Rename and rewrite immediately | Neutral public identity from day one | Irreversible, unsupported by runtime/adoption evidence | Rejected |
| Keep architecture permanently Colab-specific | Lowest near-term effort | Increases coupling and future migration cost | Rejected |

## Consequences

### Positive

- Baseline evidence and release blockers remain truthful.
- Generalization has its own requirements, task graph, migration plan, support matrix, and validation gates.
- Colab remains the flagship acquisition and compatibility target.
- Jupyter/Deepnote support can be promoted independently after representative evidence.

### Negative

- Maintainers must reconcile two active change directories.
- Shared compatibility surfaces require explicit traceability.
- Public naming remains unresolved until the evidence gate is satisfied.

## Validation

- Baseline proposal/finalization docs explicitly point to the follow-on without changing status.
- Follow-on proposal declares dependency on `build-colab-observer`.
- Follow-on migration tasks start with frozen Colab compatibility fixtures.
- Root navigation and manifests distinguish implemented baseline from proposed generalization.

## Rollback or supersession

Remove or supersede the follow-on change without changing baseline behavior. Revisit this ADR only after direct runtime evidence shows that a different change boundary is necessary.
