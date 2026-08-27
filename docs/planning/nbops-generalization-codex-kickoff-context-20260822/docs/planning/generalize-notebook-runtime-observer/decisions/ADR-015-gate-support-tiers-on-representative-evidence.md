---
status: accepted
type: adr
change: generalize-notebook-runtime-observer
tags:
  - decision
  - architecture
  - notebook-observability
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# ADR-015: Gate support tiers on representative evidence

**Path:** `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-015-gate-support-tiers-on-representative-evidence.md`  
**Purpose:** Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger.  
**Status:** Accepted  

**Decision status:** Accepted  
**Decision date:** 2026-08-21

## Context and constraints

Detection and successful import do not establish full support. Platform runtimes, frontends, storage, accelerators, and policies change independently.

## Decision

Use validated, preview, experimental, unverified, and unsupported tiers tied to named evidence gates and recheck triggers. Product priority is a separate field.

## Alternatives considered

| Option | Pros | Cons | Outcome |
|---|---|---|---|
| Binary supported/unsupported | Easy to understand | Hides partial scope and evidence gaps | Rejected |
| Evidence-backed tier per scope | Truthful and maintainable | Requires evidence ledger and automation | Selected |
| Marketing-owned support labels | Flexible copy | Drifts from executable evidence | Rejected |

## Consequences

### Positive

- Support claims are auditable.
- Static, enhanced, kernel, and server scopes can differ.
- Stale evidence can downgrade cleanly.

### Negative / tradeoffs

- More complex documentation and release process.
- Requires disciplined evidence capture.

## Validation

Tier evaluator tests, stale-evidence mutations, claim-drift checks, and representative support matrices.

## Rollback or supersession

Downgrade the affected tier/scope while retaining stronger generic fallback.

## Review trigger

Revisit vocabulary after user testing, without weakening evidence requirements.
