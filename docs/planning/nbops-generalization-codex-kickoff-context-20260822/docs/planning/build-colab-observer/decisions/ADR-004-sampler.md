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

# ADR-004: Daemon thread and bounded queue

**Status:** Proposed  
**Date:** 2026-07-11

## Context
The observer must return notebook control and avoid conflicts with notebook event loops.

## Decision
Use one daemon sampling thread, monotonic scheduling, collector-specific cadences, and a bounded queue with one store writer.

## Alternatives
- Asyncio: event-loop integration varies across notebooks.
- Child process: stronger isolation but complex lifecycle/IPC and provider handles.
- Blocking loop: violates notebook ergonomics.

## Consequences
Thread safety, bounded shutdown, and backpressure tests are mandatory.

## Review trigger
Measured collector blocking cannot be contained or a subprocess becomes necessary for unsafe providers.
