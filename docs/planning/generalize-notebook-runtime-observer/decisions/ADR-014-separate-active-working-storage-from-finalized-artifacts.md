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

# ADR-014: Separate active working storage from finalized artifacts

**Path:** `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-014-separate-active-working-storage-from-finalized-artifacts.md`  
**Purpose:** Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger.  
**Status:** Accepted  

**Decision status:** Accepted  
**Decision date:** 2026-08-21

## Context and constraints

Colab, Deepnote, and Jupyter deployments expose storage with different persistence and small-file performance. A single output directory cannot express safe active SQLite writes versus durable final reports.

## Decision

Add optional working/artifact location semantics while preserving legacy `output_dir`. Storage profiles classify locations and advise behavior; no mount, authentication, or silent transfer occurs.

## Alternatives considered

| Option | Pros | Cons | Outcome |
|---|---|---|---|
| Single output path only | Simple compatibility | Poor fit for object-backed/persistent versus ephemeral storage | Insufficient |
| Working + artifact destinations | Matches runtime/storage behavior | Configuration and migration complexity | Selected |
| Always upload to cloud/provider API | Durable artifacts | Credentials/network/account authority | Rejected |

## Consequences

### Positive

- Supports Deepnote `/tmp` and `/work` safely.
- Reduces high-frequency writes to unsuitable storage.
- Preserves explicit finalization.

### Negative / tradeoffs

- Adds configuration and partial-publication states.
- Platform defaults require representative evidence.

## Validation

Path containment, alias, mount, persistence, active-write, explicit finalization, and partial-failure tests across representative platforms.

## Rollback or supersession

Use legacy output behavior; disable auto storage policy; preserve working evidence on publication failure.

## Review trigger

Revisit after real Deepnote and JupyterHub storage evidence.
