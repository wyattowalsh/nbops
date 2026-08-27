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

# ADR-001: One product package with private UI and docs workspaces

**Status:** Proposed  
**Date:** 2026-07-11

## Context
The monitor needs Python runtime code, a compiled dashboard, and a modern docs site without turning into multiple published products.

## Decision
Use one repository with one publishable `colab-observer` Python package, a private `packages/dashboard-ui` pnpm workspace, and `apps/docs`. No Nx/Turborepo initially.

## Alternatives
- Separate repositories: clearer boundaries but harder coordinated schema/assets/releases.
- Python-only inline JavaScript: smaller repo but poor maintainability and accessibility testing.
- Full generic monorepo orchestrator: added complexity before scale justifies it.

## Consequences
Cross-language locks/builds are required; wheel asset generation must be deterministic. Product ownership remains unambiguous.

## Review trigger
Independent teams/releases or build performance make a monorepo orchestrator materially useful.
