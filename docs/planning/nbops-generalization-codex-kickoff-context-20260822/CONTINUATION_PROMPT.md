# `nbops` implementation continuation controller

Use this only when the kickoff implementation is interrupted after material work begins.

## Goal

Continue OpenSpec change `generalize-notebook-runtime-observer` from the exact recorded task state. Preserve `nbops` as the canonical product/distribution/import/CLI/default-artifact identity and preserve historical identifiers only as explicit provenance or compatibility.

## Read first

1. `CODEX_KICKOFF_PROMPT.md`
2. `LEGACY_IDENTITY_NOTICE.md`
3. `openspec/changes/generalize-notebook-runtime-observer/tasks.md`
4. `docs/planning/generalize-notebook-runtime-observer/PLANS.md`
5. `docs/planning/generalize-notebook-runtime-observer/validation.md`
6. `docs/planning/generalize-notebook-runtime-observer/traceability-matrix.md`
7. `docs/planning/generalize-notebook-runtime-observer/outer-loop.md`
8. Current repository diff and test output

## Resume rule

- Resume the earliest incomplete dependency-ready task.
- `TASK-103` freezes behavior.
- `TASK-105` freezes identity migration.
- `TASK-106` implements the `nbops` migration.
- Runtime-profile and adapter tasks begin only after those gates pass.

## Constraints

No installs, network expansion, external runtime access, Git remote mutation, publication, deployment, secrets, permissions, remote repository rename, domains/handles, or OpenSpec apply/sync/archive without separate approval.

## Validation

Rerun focused tests for changed surfaces, then applicable repository gates. Scan current surfaces for exact `nbops` identity and fail mixed current naming. Preserve stable historical IDs and supported legacy artifacts.

## Stop

Stop for incompatible repository evidence, unapproved breaking behavior, missing representative evidence, overlapping writes, or validation failure without a bounded repair.
