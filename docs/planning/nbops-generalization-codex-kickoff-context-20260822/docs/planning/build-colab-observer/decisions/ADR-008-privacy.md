---
status: proposed
type: decision-record
change: build-colab-observer
tags:
  - adr
  - decision
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# ADR-008: No telemetry and redacted collection by default

**Status:** Proposed  
**Date:** 2026-07-11

## Context
Runtime/process/environment observations can expose sensitive notebook context.

## Decision
Default operation is local and non-transmitting. Omit notebook content, environment values, full command lines, full paths, and full inventories. External integrations and expanded fields are explicit opt-ins.

## Alternatives
- Anonymous product analytics: still adds network/trust complexity.
- Rich default environment snapshot: easier support, unacceptable disclosure risk.

## Consequences
Some support questions require opt-in evidence; reports must show redaction state.

## Review trigger
A concrete support need and privacy review justify a narrowly scoped additional field.
