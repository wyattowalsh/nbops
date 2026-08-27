---
status: ready
type: decision-record
change: build-colab-observer
tags:
  - adr
  - decision
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# ADR-003: SQLite default, DuckDB optional

**Status:** Accepted for the unpublished development line  
**Date:** 2026-07-11

## Context
The product needs durable local evidence in ephemeral runtimes without a large mandatory dependency.

## Decision
Use SQLite as the only default write store. Keep the range-aware CSV/JSONL, summary, report, and SQLite bundle formats as the initial analytical surface. Defer a DuckDB adapter until an approved dependency environment and representative Colab measurements show material query value after accounting for installation, wheel size, startup time, and maintenance cost.

## Alternatives
- DuckDB default: excellent analytics, additional wheel/install/start cost.
- CSV/JSONL only: simple but weaker transactional recovery and query.
- In-memory only: loses the report-first value.

## Consequences
One writer and batched transactions are architectural constraints. The package stays smaller and the default notebook mutation remains bounded. DuckDB is not advertised or partially stubbed before it can be built and tested against the optional-extra contract.

## Review trigger
A representative workload demonstrates that SQLite plus range-aware exports cannot satisfy a documented query need, and an approved DuckDB build shows acceptable cold-start, wheel, dependency, and maintenance cost.
