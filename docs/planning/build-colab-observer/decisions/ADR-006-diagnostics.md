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

# ADR-006: Deterministic diagnostic rules

**Status:** Proposed  
**Date:** 2026-07-11

## Context
Users need explanations, but local evidence is partial and privacy-sensitive.

## Decision
Use versioned deterministic rules with windows, hysteresis, confidence, evidence, alternatives, and manual suggestions. No LLM or opaque anomaly model in core.

## Alternatives
- LLM diagnosis: network/privacy/cost/non-determinism.
- Unsupervised anomaly model: opaque and difficult to validate across runtimes.
- Raw metrics only: insufficient product differentiation.

## Consequences
Rule tuning and false-positive tests are ongoing maintenance.

## Review trigger
A local explainable model materially improves validated outcomes without violating constraints.
