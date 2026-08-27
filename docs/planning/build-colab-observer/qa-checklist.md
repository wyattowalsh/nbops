---
status: active
type: qa-checklist
change: build-colab-observer
tags:
  - qa
  - checklist
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# QA checklist

## OpenSpec and planning

- [ ] Proposal, 11 delta specs, design, and tasks agree.
- [ ] Every requirement has scenarios and traceability.
- [ ] Specs contain observable behavior, not internal implementation steps.
- [ ] ADRs identify validation/review triggers.
- [ ] Task `[P]` markers have non-overlapping writes and independent checks.

## Product

- [ ] Start returns notebook control; stop/export are idempotent.
- [ ] Core works with no accelerator or optional framework.
- [ ] Missing/estimated/stale values are never silently zero/current.
- [ ] Provider changes and sampler lag are visible.
- [ ] Diagnostics include evidence/confidence/limitations and never mutate workload.
- [ ] Default operation performs no upload.
- [ ] Reports are local, escaped, redacted, and integrity-checked.
- [ ] No keepalive, anti-idle, reconnect, timeout-bypass, or quota behavior exists.

## Accessibility and UI

- [ ] Complete keyboard path and visible stable focus.
- [ ] Every chart has summary, semantic table, and CSV parity.
- [ ] No information relies on color, hover, motion, or canvas alone.
- [ ] Reduced motion, live pause, high contrast, narrow output, and zoom pass.
- [ ] Live announcements are meaningful and deduplicated.
- [ ] Enhanced and static paths expose the same truthful capability state.

## Docs, automation, delivery

- [ ] Snippets/API/metrics/diagnostics generated sources do not drift.
- [ ] Fumadocs build, search, links, metadata, JSON-LD, AI indexes, and accessibility pass.
- [ ] Pre-commit fast/heavy split and negative fixtures work.
- [ ] CI permissions/pins/fork behavior are reviewed.
- [ ] Wheel/sdist include local UI assets and exclude secrets/caches/unintended files.
- [ ] PyPI/Vercel setup, deploy, and publish remain protected and approval-gated.

## Handoff

- [ ] AGENTS files are durable deltas, not task dumps.
- [ ] PLANS records progress/discoveries/validation/recovery.
- [ ] Codex handoff names read-first paths, first task, write scope, checks, and stops.
- [ ] Continuation, outer loop, manifest, and finalization report agree.
