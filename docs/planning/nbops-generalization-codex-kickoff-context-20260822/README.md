---
status: active
type: bundle-readme
change: generalize-notebook-runtime-observer
tags:
  - nbops
  - openspec
  - codex
  - planning
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# `nbops` planning, build, specification, and Codex kickoff bundle

## Purpose

This focused bundle gives Codex the smallest complete context needed to:

1. freeze the implemented Google Colab behavior;
2. migrate the canonical local identity to `nbops`;
3. preserve supported behavior and legacy artifact readability;
4. introduce the platform-neutral runtime-profile foundation;
5. promote Jupyter, Deepnote, Colab, and other environments only from representative evidence.

## Canonical identity

`nbops` is the exact current product, distribution, import-package, CLI, and repository identity. Google Colab remains the flagship adapter.

The change ID `build-colab-observer` and its baseline docs remain historical identifiers. They are not current competing branding.

## Primary read order

1. `CODEX_KICKOFF_PROMPT.md`
2. `IDENTITY_MAP.md`
3. `LEGACY_IDENTITY_NOTICE.md`
4. `AGENTS.md`
5. `openspec/changes/generalize-notebook-runtime-observer/proposal.md`
6. `openspec/changes/generalize-notebook-runtime-observer/specs/**/spec.md`
7. `openspec/changes/generalize-notebook-runtime-observer/design.md`
8. `openspec/changes/generalize-notebook-runtime-observer/tasks.md`
9. `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-016-adopt-nbops-before-first-publication.md`
10. `docs/planning/generalize-notebook-runtime-observer/naming-packaging-strategy.md`
11. `docs/planning/generalize-notebook-runtime-observer/compatibility-migration.md`
12. `docs/planning/generalize-notebook-runtime-observer/validation.md`
13. `docs/planning/generalize-notebook-runtime-observer/traceability-matrix.md`
14. `docs/planning/generalize-notebook-runtime-observer/PLANS.md`
15. `docs/planning/generalize-notebook-runtime-observer/codex-handoff.md`

## Stable baseline evidence

The preserved baseline lives under:

- `openspec/changes/build-colab-observer/`
- `docs/planning/build-colab-observer/`

Those files document the original Colab-first implementation and executed evidence. Do not bulk-rebrand them or interpret their historical titles as the current product identity.

## Current counts

- 10 follow-on behavior domains
- 30 follow-on requirements
- 60 follow-on scenarios
- 44 dependency-aware implementation tasks
- 7 accepted follow-on ADRs

## Validation boundary

The bundle is validated for identity consistency, OpenSpec shape, task-graph integrity, JSON/YAML parsing, internal links, manifests, deterministic ZIP construction, path safety, clean extraction, and byte comparison. Product runtime implementation and managed-platform support remain separate future evidence stages.
