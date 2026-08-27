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

# ADR-011: Use a faceted runtime profile and internal adapter registry

**Path:** `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-011-use-a-faceted-runtime-profile-and-internal-adapter-registry.md`  
**Purpose:** Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger.  
**Status:** Accepted  

**Decision status:** Accepted  
**Decision date:** 2026-08-21

## Context and constraints

Notebook environments combine independent provider, frontend, kernel, container, storage, transport, and support dimensions. A single platform enum creates false exclusivity and cross-cutting branches.

## Decision

Use a versioned faceted profile resolved from bounded adapter evidence. Keep the initial adapter registry internal, deterministic, allowlisted, and failure-isolated.

## Alternatives considered

| Option | Pros | Cons | Outcome |
|---|---|---|---|
| Single `platform` enum | Simple API | Cannot represent mixed frontends/runtimes or uncertainty | Rejected |
| Faceted evidence profile | Truthful and extensible; conflicts explicit | More schema and merge complexity | Selected |
| Public third-party plugin API | Ecosystem extensibility | Premature security/support burden | Deferred |

## Consequences

### Positive

- Models real deployments accurately.
- Supports generic fallback and mixed environments.
- Centralizes privacy, conflicts, and support evidence.

### Negative / tradeoffs

- Requires versioned schema, merge rules, fixtures, and bounded evidence.
- Must avoid becoming a generic plugin framework.

## Validation

Property/mutation tests cover deterministic merge, conflicts, unknowns, privacy reduction, timeout, and cardinality.

## Rollback or supersession

Fall back to a minimal generic profile and disable failing adapters independently.

## Review trigger

Revisit public adapter extensibility only after multiple first-party adapters stabilize and external demand is demonstrated.
