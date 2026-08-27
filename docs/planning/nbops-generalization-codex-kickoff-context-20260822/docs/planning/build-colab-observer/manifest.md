---
status: active
type: manifest
change: build-colab-observer
tags:
  - manifest
  - navigation
updated: 2026-08-21
cssclasses:
  - planning-doc
---
# Planning artifact manifest

## Source of truth

| Layer | Paths | Role |
|---|---|---|
| Proposed behavior | `openspec/changes/build-colab-observer/specs/**/spec.md` | Observable requirements and scenarios |
| Intent/design/work | `proposal.md`, `design.md`, `tasks.md` | Scope, decisions, implementation graph |
| Machine contracts | `change-pack.json`, `task-graph.json`, `manifest.generated.json` | Agent/tool ingestion and integrity |
| Product deep dives | `docs/planning/build-colab-observer/` | Evidence, architecture, UX, safety, validation, handoff |
| Presentation | MOC, Canvas, Bases, dashboard, `.obsidian/` | Progressive navigation with static fallback |

## Key counts

- 11 OpenSpec domains
- 73 requirements and 93 scenarios
- 45 implementation tasks
- 9 ADRs
- 9 normalized skill lenses
- 25-task conditional next loop

## Read order

See [[START_HERE]], [[docs/maps/build-colab-observer-moc|MOC]], [[docs/planning/build-colab-observer/runtime-boundary-hardening-20260717|runtime-boundary hardening]], [[docs/planning/build-colab-observer/final-assurance-hardening-20260716|prior final-assurance hardening]], [[openspec/changes/build-colab-observer/tasks|task state]], [[docs/planning/build-colab-observer/validation|validation]], and `manifest.generated.json`.

## Follow-on change boundary

- Baseline decision: [[docs/planning/build-colab-observer/decisions/ADR-010-generalization-sequencing|ADR-010]]
- Follow-on OpenSpec: [[openspec/changes/generalize-notebook-runtime-observer/proposal|proposal]], [[openspec/changes/generalize-notebook-runtime-observer/tasks|tasks]]
- Follow-on planning: [[docs/planning/generalize-notebook-runtime-observer/manifest|manifest]], [[docs/maps/generalize-notebook-runtime-observer-moc|map of content]]

The follow-on is proposed planning only and does not alter this baseline's final-with-known-risks status.
