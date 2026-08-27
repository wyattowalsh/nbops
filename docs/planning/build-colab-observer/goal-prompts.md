---
status: proposed
type: goal-prompts
change: build-colab-observer
tags:
  - codex
  - goal
  - handoff
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Copyable goal prompts

## Availability and setup checks

- Codex: confirm `/goal` is available. If not, recheck official docs; compatibility setup may mention `features.goals = true` or `codex features enable goals`, but config mutation or upgrade requires approval.
- Grok Build: confirm the current CLI/session exposes Goal controls. Do not install, upgrade, sign in, subscribe, or run network setup automatically. Use the Generic goal-capable agent prompt when unavailable.
- Read [[docs/planning/build-colab-observer/openspec-grounding|openspec-grounding.md]] before starting any goal.

## Goal lifecycle controls

| Surface | Start | Status | Pause | Resume | Clear |
|---|---|---|---|---|---|
| Codex | `/goal <objective>` | `/goal` | `/goal pause` | `/goal resume` | `/goal clear` |
| Grok Build | `/goal <objective>` | `/goal status` | `/goal pause` | `/goal resume` | `/goal clear` |
| Generic | Native goal/task command | Native status | Native pause/stop | Native resume/retry | Native clear/cancel |

## Codex `/goal`

```text
/goal Implement OpenSpec change `build-colab-observer` in the target repository as a production-grade, local-first, accessible Google Colab runtime observability package. Read AGENTS.md, proposal.md, all delta specs, design.md, tasks.md, context-map.md, source-registry.md, validation.md, traceability-matrix.md, and PLANS.md first. Begin with implementation Wave A and work only through satisfied dependencies and approved write scopes. After each slice, run the smallest relevant checks, update PLANS with changed files, evidence, discoveries, and validation, reconcile OpenSpec if behavior changes, then run a /grill-me reassessment. Preserve these invariants: no account or hosted backend required, no default telemetry, no secrets, no public share URL, no keepalive/anti-idle/reconnect/timeout-bypass/quota behavior, no automatic remediation, truthful unavailable/estimated/stale states, and an accessible text/table/CSV equivalent for every chart. Stop before installs, network expansion, commits, pushes, PRs, deploys, publishing, GitHub/Vercel/PyPI/account/config/permission changes, destructive actions, or secrets unless explicitly approved. Done only when approved tasks and validation evidence agree; release, deploy, verify/sync, and archive remain separate approvals.
```

## Grok Build `/goal`

```text
/goal Implement OpenSpec change `build-colab-observer` from the proposal, delta specs, design, tasks, validation, and outer-loop ledger. Begin with read-only Wave A evidence. Maintain a checklist and validation evidence, preserve all safety/accessibility/privacy invariants, and use `/goal status`, pause, resume, or clear only when verified for the current tool. Stop for missing evidence, unsafe permissions, approval boundaries, scope conflict, or validation without a safe repair path. Do not install, upgrade, sign in, subscribe, or run network setup automatically.
```

## Generic goal-capable agent

```text
Goal: Implement OpenSpec change `build-colab-observer` to release-candidate quality.
Read first: AGENTS.md; openspec/changes/build-colab-observer/{proposal,design,tasks}.md; all delta specs; docs/planning/build-colab-observer/{openspec-grounding,context-map,source-registry,traceability-matrix,validation,PLANS,outer-loop}.md.
Loop: inspect evidence -> select the smallest dependency-ready task -> implement within write scope -> validate -> update PLANS and traceability -> run /grill-me -> continue only while safe material value remains.
Constraints: no secrets, no default telemetry, no remote/public dashboard, no anti-idle/keepalive/reconnect/timeout-bypass/quota logic, no automatic remediation, and no install/commit/publish/deploy/config/account action without approval.
Done when: approved requirements, tasks, runtime evidence, accessibility, security, package artifacts, documentation, and release-candidate checks agree, or blockers are documented precisely.
```


Compatibility safety marker: do not install, upgrade, sign in, subscribe, or run network setup automatically; use the generic OpenSpec goal contract instead.
