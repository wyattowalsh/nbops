---
status: active
type: kickoff-overview
change: generalize-notebook-runtime-observer
tags:
  - nbops
  - openspec
  - codex
  - kickoff
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Start here: `nbops`

This bundle is the reviewed Codex kickoff context for adopting **`nbops`** and implementing OpenSpec change:

`generalize-notebook-runtime-observer`

## Canonical identity

```text
Product:             nbops
Repository:          nbops
Distribution:        nbops
Python import:       nbops
CLI:                 nbops
Source package:      src/nbops/
Tagline:             Local-first runtime observability for Python notebooks.
Flagship adapter:    Google Colab
```

The stable historical OpenSpec ID `build-colab-observer` remains intact as provenance. See [LEGACY_IDENTITY_NOTICE.md](LEGACY_IDENTITY_NOTICE.md).

## Use this bundle

1. Read [CODEX_KICKOFF_PROMPT.md](CODEX_KICKOFF_PROMPT.md).
2. Read [IDENTITY_MAP.md](IDENTITY_MAP.md).
3. Inspect the active proposal, behavior specs, design, and tasks under `openspec/changes/generalize-notebook-runtime-observer/`.
4. Inspect the implemented baseline under `openspec/changes/build-colab-observer/` without rewriting its history.
5. Read ADR-016, compatibility migration, validation, traceability, PLANS, and the Codex handoff.
6. Begin implementation with `TASK-103-freeze-colab-compatibility-fixtures`, then `TASK-105-freeze-nbops-migration-fixtures` and `TASK-106-implement-nbops-identity-migration`.

## Current stage

| Surface | State |
|---|---|
| Canonical name decision | Accepted: `nbops` |
| Planning update | Complete and validated |
| Product implementation | Not started in this artifact-only revision |
| Managed runtime evidence | Still evidence-gated |
| Publication, remote repository, domains, deployment | Separate approval-gated lifecycle |

## Core safety boundaries

- No dependency installation or network resolution without approval.
- No Git remote mutation, publication, deployment, account, domain, permission, or secret actions.
- No hosted backend, telemetry, public endpoint, runtime CDN, remote code, keepalive, anti-idle, reconnect automation, timeout bypass, or quota circumvention.
- No support-tier promotion without representative runtime evidence.
