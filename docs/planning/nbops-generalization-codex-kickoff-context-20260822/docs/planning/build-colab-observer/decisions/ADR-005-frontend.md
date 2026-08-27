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

# ADR-005: Preact plus Apache ECharts SVG

**Status:** Proposed, spike-gated  
**Date:** 2026-07-11

## Context
The dashboard needs modern interactions and dense time-series visualization with a small notebook payload.

## Decision
Spike a private TypeScript frontend using Preact and Apache ECharts SVG rendering, bundled locally. Keep semantic summaries/tables authoritative for accessibility.

## Alternatives
- React-heavy application: familiar but larger.
- Plotly: feature-rich but potentially larger and still needs table parity.
- Hand-built SVG: smallest control surface but high chart engineering cost.

## Consequences
Bundle-size, license, ARIA, and wheel-content validation are release gates.

## Review trigger
Spike misses size/render/accessibility budgets.
