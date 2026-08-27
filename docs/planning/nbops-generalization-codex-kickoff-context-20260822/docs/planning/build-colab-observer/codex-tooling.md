---
status: proposed
type: codex-tooling
change: build-colab-observer
tags:
  - codex
  - agents
  - tooling
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Codex tooling proposal

## Recommendation

Begin with repository docs, OpenSpec, nested `AGENTS.md`, PLANS, and normal sandboxed commands. Do not add MCP, hooks, custom Skills, plugins, or write-capable subagents until implementation demonstrates a recurring gap.

## Tooling decisions

| Surface | Recommendation | Trigger | Approval |
|---|---|---|---|
| Nested `AGENTS.md` | Include now | durable local rules | docs-only no; repo write per normal review |
| Codex `/goal` | Use after TASK-001/002 and verified commands | bounded long implementation | availability check; no config mutation without approval |
| PLANS | Include now | multi-wave work | no |
| pre-commit | Implement TASK-060 | deterministic quality/policy | install/config approval in target repo |
| Skill | Defer | repeated collector or release workflow across projects | draft no; install yes |
| MCP | None initially | live external context that docs/scripts cannot supply | yes |
| Plugin | None | reusable cross-project package with proven need | yes |
| Subagents | Read-only reviews or non-overlapping collector/UI/docs slices | enough independent work and merge owner | write agents yes |
| Worktrees | Optional for truly independent tasks | target repo supports clean separation | yes |

## Codex security posture

- Use default/tight sandbox and approval settings first.
- Network access only for explicit dependency/current-doc tasks.
- Scope writes to task paths.
- Do not grant release/deploy/account permissions to implementation agents.
- Keep current platform facts in source registry and recheck before dependency/workflow changes.

## Useful future Skill candidates

1. `add-colab-observer-collector`: only after at least three collector additions prove a stable workflow; references provider contract, fixture matrix, privacy, units, and docs.
2. `validate-colab-observer-release`: only after release steps stabilize; builds/tests/artifact audits but never publishes by default.
3. `refresh-diagnostic-catalog`: only if source/rule/docs generation repeats and remains deterministic.

Each needs trigger-rich description, references/scripts/tests, and explicit NOT-for boundaries. No vague prompt-only skill.

## Subagent plan

| Agent/lane | Read scope | Write scope | Output | Merge owner |
|---|---|---|---|---|
| Collector lanes | contracts + collector docs | distinct collector/test files | implementation + evidence | collector registry task |
| Accessibility reviewer | UI/docs fixtures | review findings, later bounded repairs | WCAG matrix | UI lead |
| Security reviewer | threat model/workflows/exports | findings, later bounded repairs | severity/evidence | main agent |
| Docs lane | public contracts and content graph | docs source only | buildable content | docs task |
| CI reviewer | scripts/manifests | workflow proposal/review | permission/fork analysis | main agent |

No two agents edit root locks, generated assets, registry/init files, or the same workflow concurrently.


## Evidence, source, and validation

Every tooling addition must identify the target-repository evidence that justifies it, the official source for non-obvious behavior, a least-privilege permission model, an approval owner, a deterministic validation command, and a disable/rollback path. Tooling remains a proposal until approved.
