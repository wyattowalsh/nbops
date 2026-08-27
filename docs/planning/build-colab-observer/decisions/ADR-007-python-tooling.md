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

# ADR-007: uv-managed Python project with build-backend spike

**Status:** Proposed  
**Date:** 2026-07-11

## Context
The project needs fast locked development and reliable inclusion of compiled frontend assets.

## Decision
Use `uv` for environments, locking, scripts, builds, and CI orchestration. Select Hatchling or `uv_build` after a minimal wheel-data spike proves reproducible package data and no Node dependency for end-user installation.

## Alternatives
- Commit to `uv_build` immediately: simpler, but asset-layout flexibility must be proven.
- Hatchling immediately: mature package-data controls, one additional build dependency.

## Consequences
The backend decision remains intentionally open for TASK-003; wheel tests decide it.

## Review trigger
Completed bundled-asset spike.
