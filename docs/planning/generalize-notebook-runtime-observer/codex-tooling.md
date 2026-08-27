---
status: proposed
type: codex-tooling
change: generalize-notebook-runtime-observer
tags: [codex, tooling, approvals]
updated: 2026-08-22
cssclasses: [planning-doc]
---

# Codex tooling proposal

**Path:** `docs/planning/generalize-notebook-runtime-observer/codex-tooling.md`  
**Purpose:** Bound Codex Goal, subagent, Skill, MCP, hook, config, and validation usage for implementation.  
**Status:** Proposed  
**Load/use when:** Preparing implementation orchestration beyond the existing AGENTS, Goal, PLANS, and handoff artifacts.

## Recommendation

Use the existing repository commands and documents first. No new MCP, plugin, hook, Skill, or Codex config is required to begin TASK-103. Tooling additions are justified only when they remove a repeated evidence loop or strengthen a safety gate.

| Surface | Proposed use | Boundary/approval |
|---|---|---|
| `AGENTS.md` | Durable repo/subtree rules | Already present; no task dump |
| Codex Goal | Long-running compatibility-first implementation | Verify availability; enabling config requires approval |
| Subagents | Read-only platform research, test review, independent adapter audits | Non-overlapping writes; one merge owner |
| Skill | Only if runtime-profile/support-matrix workflow becomes recurring | Draft okay; install/enable approval required |
| MCP | Not needed for core implementation | External systems/network/config require approval |
| Hooks/config | Existing deterministic gates only | New config/hooks require trust review and approval |

## Safe parallel packets

- Profile/schema contract review: read-heavy, no shared implementation writes.
- Jupyter/Deepnote research refresh: docs/source registry only.
- Security threat review: tests/planning findings, no product writes.
- Representative-runtime execution: separate environments/evidence outputs.

Do not parallelize shared model/schema implementation, migration state, package manifest, or release evidence without exclusive write scopes and a merge owner.
