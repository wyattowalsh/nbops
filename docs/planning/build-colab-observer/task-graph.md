---
status: active
type: task-graph
change: build-colab-observer
tags:
  - tasks
  - dependencies
  - codex
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Task graph

**Machine graph:** `docs/planning/build-colab-observer/task-graph.json`  
**Canonical checklist:** `openspec/changes/build-colab-observer/tasks.md`

## Wave summary

| Wave | Tasks |
|---|---:|
| Wave 0 — Preflight and contracts | 4 |
| Wave 1 — Core observer and persistence | 5 |
| Wave 2 — Collectors | 6 |
| Wave 3 — Diagnostics and exports | 5 |
| Wave 4 — Accessible notebook dashboard | 7 |
| Wave 5 — Notebook adoption and documentation | 6 |
| Wave 6 — Quality, CI/CD, release readiness | 6 |
| Wave 7 — Final verification and handoff | 6 |

## Dependency architecture

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#eef2ff", "primaryBorderColor": "#6366f1", "primaryTextColor": "#172554", "lineColor": "#64748b", "tertiaryColor": "#f8fafc", "fontFamily": "Inter, ui-sans-serif, system-ui"}, "flowchart": {"curve": "basis", "padding": 12}}}%%
flowchart TD
    T001[TASK-001 evidence] --> T002[TASK-002 contracts]
    T002 --> T003[TASK-003 workspaces]
    T003 --> T004[TASK-004 fixtures]
    T004 --> C[Core 010–014]
    C --> K[Collectors 020–025]
    K --> D[Diagnostics/exports 030–034]
    C --> U[UI contract 040]
    D --> U
    U --> UI[Dashboard 041–046]
    D --> N[Snippets/docs 050–055]
    UI --> N
    T003 --> Q[Quality foundation 060]
    N --> CI[CI/release plans 061–065]
    Q --> CI
    CI --> F[Final verification 070–075]
```

## Parallelism rules

- `[P]` tasks have distinct paths and dedicated validation.
- A task cannot run parallel merely because it is small.
- Generated artifacts have one source owner and one generation owner.
- Dependencies that define schemas, public API, UI messages, or root configuration serialize downstream work.
- Parallel work reports exact files and does not modify shared lockfiles or workflow permissions without coordination.

## Task execution record

Use [[docs/planning/build-colab-observer/PLANS]] for current task, evidence, changed files, commands/results, discoveries, blocked state, and reassessment. The JSON graph is planning metadata, not completion evidence.
