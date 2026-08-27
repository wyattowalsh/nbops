---
status: proposed
type: agents-map
change: build-colab-observer
tags:
  - agents-md
  - codex
  - instructions
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Nested `AGENTS.md` instruction map

## Policy

Root guidance is concise and durable. Nested files contain only local deltas. Task-specific work stays in OpenSpec tasks, PLANS, or handoffs. Agents read from root toward the file they edit.

## Proposed tree

```text
AGENTS.md
├── src/colab_observer/AGENTS.md
│   ├── collectors/AGENTS.md
│   ├── ui/AGENTS.md
│   └── integrations/AGENTS.md
├── packages/dashboard-ui/AGENTS.md
├── notebooks/AGENTS.md
├── apps/docs/AGENTS.md
├── openspec/AGENTS.md
└── .github/AGENTS.md
```

## Instruction ownership

| Path | Durable local guidance |
|---|---|
| `/AGENTS.md` | source of truth, repo map, verified commands, change workflow, approval/security, global done criteria |
| `src/colab_observer/AGENTS.md` | typed Python conventions, public API/schema compatibility, core dependency discipline, no import side effects |
| `collectors/AGENTS.md` | provider isolation, deadlines, units/quality, privacy, fake-provider tests, no installs/mutation |
| `ui/AGENTS.md` | transport/fallback boundary, local assets, escaped data, bounded messages, accessibility parity |
| `integrations/AGENTS.md` | opt-in outbound behavior, data mapping, no core coupling, disabled-path tests |
| `packages/dashboard-ui/AGENTS.md` | pnpm/TypeScript, source/generated boundary, semantic components, charts/table parity, rendered proof |
| `notebooks/AGENTS.md` | canonical snippets, no secrets/outputs/keepalive, safe reruns, notebook smoke |
| `apps/docs/AGENTS.md` | Fumadocs content graph, generated source mapping, SEO/accessibility, Vercel approval boundary |
| `openspec/AGENTS.md` | behavior/design/task separation, validation, no premature sync/archive |
| `.github/AGENTS.md` | least privilege, SHA pins, fork safety, protected release/deploy, no secrets in PR jobs |

## Root `AGENTS.md` budget

Keep under roughly 150 lines unless the repository proves more is needed. It should include:

- read-first/source-of-truth paths;
- repository map;
- commands confirmed from manifests;
- OpenSpec task execution rules;
- global style and testing expectations;
- no keepalive/no telemetry/default privacy invariants;
- approval gates;
- completion report requirements.

It should not include the 45-task plan, current progress, package versions, or volatile provider instructions.

## Nested delta example

```markdown
# AGENTS.md — collectors

Inherits repository and Python-package guidance from parent files.

- Every collector implements probe/collect/close and returns typed results.
- Never write to storage/UI or install/import disabled frameworks.
- Preserve units, provider, quality, deadlines, and bounded errors.
- Add fake-provider tests for unavailable, partial, malformed, timeout, and recovery paths.
- Full command lines/environment values are off by default.
```

## Agent write boundaries

- Parallel collector tasks own distinct collector and test files; the registry has one merge owner.
- UI source and generated Python assets are not edited concurrently; frontend task owns source, integration task owns generation/packaging.
- Docs generated pages are not hand-edited; generators/source contracts own them.
- Workflow files are security-sensitive and require focused review.
- OpenSpec changes that alter behavior precede code changes and ripple to traceability/docs.

## Validation rule

Each nested `AGENTS.md` names only commands relevant to its subtree or links to root commands. All commands must exist in the repository before they are described as executable facts.
