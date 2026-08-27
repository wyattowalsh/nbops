---
status: active
type: codex-handoff
change: generalize-notebook-runtime-observer
tags:
  - codex
  - handoff
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Codex handoff: adopt `nbops` and generalize notebook runtime observability

## Goal

Complete the largest safe dependency-ready slice of `generalize-notebook-runtime-observer`, beginning with TASK-103, TASK-105, and TASK-106.

## Context

- Canonical identity: `nbops`.
- Historical baseline: `openspec/changes/build-colab-observer/`.
- Active change: `openspec/changes/generalize-notebook-runtime-observer/`.
- Full runbook: `CODEX_KICKOFF_PROMPT.md`.
- Progress ledger: `docs/planning/generalize-notebook-runtime-observer/PLANS.md`.

## Constraints

- Freeze observable behavior before package migration.
- Use `nbops` for every current canonical surface.
- Preserve baseline change IDs and prior artifact readability.
- Retain a prior import shim only from verified external compatibility evidence.
- Respect task dependencies and exclusive write scopes.
- Do not install, access network/external runtimes, mutate remote Git identity, publish, deploy, change domains/permissions, handle secrets, or apply/sync/archive without approval.
- Do not add telemetry, hosted/public services, runtime CDN, remote code, automatic remediation, keepalive, anti-idle, reconnect automation, timeout bypass, or quota circumvention.

## Done when

- TASK-103 behavior fixtures are green.
- TASK-105 migration fixtures are green.
- TASK-106 current identity migration is green.
- Any additional completed task satisfies its OpenSpec acceptance and validation.
- PLANS, tasks, validation, traceability, risks, and changed paths agree.
- Remaining work has an exact next task or blocker.

## Stop

Stop for contradictory evidence, unapproved behavior break, missing representative evidence required for a claim, overlapping writes, approval-gated action, or validation failure without a bounded repair.
