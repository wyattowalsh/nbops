---
status: active
type: goal
change: generalize-notebook-runtime-observer
tags:
  - goal
  - nbops
  - openspec
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Goal contract: adopt `nbops` and generalize notebook runtime observability

## Outcome

Current local product, distribution, import, CLI, source target, documentation, defaults, and new-artifact metadata use `nbops`; supported Colab behavior and prior artifact readability remain intact; runtime-profile work proceeds without unsupported platform claims.

## Non-goals

- Remote repository mutation, registry reservation, domain/handle action, publication, announcement, deployment, or archive.
- Non-Python kernels.
- Automatic server extension installation.
- Hosted backend, telemetry, public endpoint, runtime CDN, remote code, automatic remediation, keepalive, anti-idle, reconnect automation, timeout bypass, or quota circumvention.

## Read first

1. `CODEX_KICKOFF_PROMPT.md`
2. `IDENTITY_MAP.md`
3. Active OpenSpec proposal/specs/design/tasks
4. Historical baseline proposal/specs/design/tasks
5. ADR-016 and compatibility migration
6. Validation, traceability, PLANS, and outer loop
7. Nearest nested `AGENTS.md`

## Done when

- TASK-103, TASK-105, and TASK-106 are green before adapter extraction.
- All completed tasks satisfy their OpenSpec acceptance and exact validation.
- Current canonical identity is consistently `nbops`.
- Supported behavior and prior artifacts remain covered.
- Any legacy shim is evidence-backed, delegating, tested, and removable.
- Platform and scope claims match representative evidence.
- Security, accessibility, package, migration, and runtime gates agree.

## Goal controls

| Surface | Start | Status | Pause | Resume | Clear |
|---|---|---|---|---|---|
| Codex | `/goal <objective>` | `/goal` | `/goal pause` | `/goal resume` | `/goal clear` |
| Grok Build | `/goal <objective>` | `/goal status` | `/goal pause` | `/goal resume` | `/goal clear` |
| Generic | native goal/task mode | native status | native pause/stop | native resume/retry | native clear/cancel |

Goal setup or agent configuration mutation requires approval.

## Iteration policy

Freeze behavior, adopt `nbops`, validate, implement one dependency-ready core slice, validate again, update ledgers, then reassess.

## Stop conditions

Stop before approval-gated operations or when compatibility, representative evidence, scope, or validation cannot be resolved safely.
