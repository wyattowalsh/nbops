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

# ADR-012: Make measurement scope first-class and server evidence optional

**Path:** `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-012-make-measurement-scope-first-class-and-server-evidence-optional.md`  
**Purpose:** Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger.  
**Status:** Accepted  

**Decision status:** Accepted  
**Decision date:** 2026-08-21

## Context and constraints

Kernel-side code cannot inherently establish notebook-document, sibling-kernel, server, workspace, or host scope. Server integration introduces separate installation, authentication, authorization, and deployment risks.

## Decision

Every metric/report preserves scope and limit provenance. Kernel-local operation is the default. Jupyter Server evidence is an optional explicit read-only integration with a valid no-go outcome.

## Alternatives considered

| Option | Pros | Cons | Outcome |
|---|---|---|---|
| Infer host/server scope | Simple labels | Misleading and unsafe | Rejected |
| Kernel-local only forever | Low risk | Leaves useful authorized server evidence unavailable | Not selected |
| First-class scope + optional server provider | Truthful baseline and additive capability | More validation/security surface | Selected |

## Consequences

### Positive

- Prevents overclaiming.
- Supports JupyterHub variation.
- Keeps core install usable everywhere.

### Negative / tradeoffs

- More verbose reports/UI.
- Optional server provider requires long-term security maintenance if adopted.

## Validation

Runtime fixtures and representative deployments prove kernel-only, container-visible, server-visible, conflict, and unavailable behavior.

## Rollback or supersession

Disable or omit the server provider; core falls back to kernel/process/container scope.

## Review trigger

Revisit after the server-provider spike and interoperability review with `jupyter-resource-usage`.
