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

# ADR-002: Progressive widget transport with static fallback

**Status:** Proposed  
**Date:** 2026-07-11

## Context
Colab is notebook-native but custom-widget and iframe behavior can change. A live UI must not be a correctness dependency or public service.

## Decision
Use a locally bundled custom-widget adapter for enhanced live interaction and a core static summary/semantic-table fallback. No Gradio share URL, tunnel, or required port server.

## Alternatives
- Gradio/port iframe: rapid UI but adds server lifecycle/exposure and platform fragility.
- Terminal TUI: robust but not native to normal Colab cells.
- Static-only: most portable but loses interactive diagnosis.

## Consequences
Two presentation paths require parity tests. Transport is versioned and isolated.

## Review trigger
Current Colab no longer supports a safe custom-widget path or a first-party supported dashboard API supersedes it.
