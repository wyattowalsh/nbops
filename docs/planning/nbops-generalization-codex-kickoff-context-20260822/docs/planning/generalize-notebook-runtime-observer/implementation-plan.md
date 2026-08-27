---
status: proposed
type: implementation-plan
change: generalize-notebook-runtime-observer
tags:
  - implementation
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Implementation plan

## Strategy

Migrate identity before extracting platform adapters. Freeze existing behavior, prove target and legacy contracts, apply one atomic local `nbops` migration, then generalize behind the canonical package.

## Waves

| Wave | Tasks | Outcome | Exit gate |
|---|---|---|---|
| A0 behavior and identity | 103–106 | `nbops` current identity plus supported legacy compatibility | Clean source/wheel/import/CLI/default/artifact identity tests |
| B runtime-profile foundation | 110–115 | Faceted profile, evidence, support tiers, persistence, read-only API | Schema/property/API tests |
| C adapters/scope/storage | 120–128 | Generic/IPython/Colab/Jupyter/Deepnote/server boundaries | Failure isolation and runtime fixtures |
| D display/accessibility | 130–135 | Static universal model plus evidence-gated transports | Semantic chart/table/CSV parity |
| E migration/adoption | 140–146 | Additive schemas, legacy readers, examples/docs, public-identity readiness | Legacy/current wheel and identity matrix |
| F representative validation | 150–158 | Executed platform/security/performance evidence and release decision | Every task complete, blocked, or deferred |

## Sequencing rationale

1. A platform-neutral architecture under the wrong package identity creates needless migration work.
2. Moving identity without frozen behavior risks accidental breaking changes.
3. Therefore behavior fixtures precede identity fixtures, which precede identity migration, which precedes adapter extraction.
4. Platform promotion remains evidence-gated even though identity is already decided.

## Validation summary

- Focused task tests before broad gates.
- Clean source and wheel validation for `nbops`.
- Legacy import/artifact fixtures where required.
- Whole-repository identity scan.
- OpenSpec and machine graph validation.
- Representative runtime and manual accessibility evidence before support/conformance claims.

## Rollback and repair

Before publication, revert the identity migration as one unit. Disable adapters independently. Preserve generic/static fallback and legacy readers. Do not delete or silently move user data.

## Approval boundary

Local package/import/CLI/artifact migration to `nbops` is in scope. Dependency installation/resolution, external runtimes/accounts, server enablement, Git remote changes, package publication, deployment, domains/handles, secrets, permissions, and OpenSpec apply/sync/archive require separate approval.
