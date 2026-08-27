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

# ADR-013: Keep semantic static display as the universal baseline

**Path:** `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-013-keep-semantic-static-display-as-the-universal-baseline.md`  
**Purpose:** Record a consequential architecture or product decision, alternatives, consequences, validation, rollback, and review trigger.  
**Status:** Accepted  

**Decision status:** Accepted  
**Decision date:** 2026-08-21

## Context and constraints

Provider-specific widgets and comm transports vary, can require hosted assets, and may fail during notebook lifecycle changes. The current text/static HTML/SVG/table path already has local evidence and accessibility foundations.

## Decision

One semantic dashboard model feeds text and script-free static output everywhere. Enhanced transports are capability-gated and cannot be required for correctness.

## Alternatives considered

| Option | Pros | Cons | Outcome |
|---|---|---|---|
| Widget-first UI | Richer interaction | Dependency/runtime/CDN/lifecycle risk | Rejected |
| Static-only forever | Most portable | Limits interactive exploration | Not selected |
| Static baseline + optional transports | Correctness and progressive enhancement | Parity tests required | Selected |

## Consequences

### Positive

- Universal fallback.
- No remote assets/public service.
- Clear accessibility and export parity.

### Negative / tradeoffs

- Enhanced interactions may arrive later on some platforms.
- One semantic model must satisfy multiple transports.

## Validation

No-network browser tests plus chart/summary/table/CSV parity and transport-failure recovery.

## Rollback or supersession

Disable enhanced transports without changing observer/store/export behavior.

## Review trigger

Revisit a transport only after representative lifecycle and accessibility evidence exists.
