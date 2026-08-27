---
status: active
type: diagram-index
change: generalize-notebook-runtime-observer
tags: [diagrams, mermaid, navigation]
updated: 2026-08-22
cssclasses: [planning-doc]
---

# Diagram index

**Path:** `docs/planning/generalize-notebook-runtime-observer/diagram-index.md`  
**Purpose:** Inventory diagrams by question, audience, source-of-truth anchor, and text fallback.  
**Status:** Active  
**Load/use when:** Reviewing architecture, task dependencies, validation, or preparing a walkthrough.

| Location | Question answered | Grounding | Text fallback |
|---|---|---|---|
| proposal | How does evidence become a support/naming decision? | intent/scope | approach summary |
| architecture | How do profile, adapters, core, display, and exports interact? | design | component tables |
| runtime-profile-model | How are evidence/conflicts/facets represented? | runtime-profiles spec | field tables |
| platform-adapter-contract | How is evidence validated and merged? | platform-adapters spec | contract rules |
| measurement-scope | What does each metric cover? | measurement-scope spec | scope matrix |
| storage-profiles | How do active and final destinations differ? | storage-profiles spec | profile table |
| display-transport | How does static fallback remain universal? | notebook-display spec | transport table |
| platform-diagnostics | When may platform rules activate? | platform-diagnostics spec | eligibility contract |
| compatibility-migration | How is Colab preserved while internals change? | migration spec | staged table |
| task-graph | What is the critical path and parallel-safe work? | tasks | dependency table/JSON |
| validation | Which evidence gates permit support promotion? | validation/support specs | validation matrix |
| outer-loop | How does implementation progress and reassess? | tasks/PLANS | 25-todo table |

Every Mermaid block uses the shared init style, has adjacent explanatory text, and is additive to tables or prose.
