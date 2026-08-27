---
status: active
type: codex-handoff
change: build-colab-observer
tags:
  - codex
  - handoff
  - implementation
updated: 2026-07-25
cssclasses:
  - planning-doc
---
# Codex handoff: `build-colab-observer`

## Objective

Continue `colab-observer` only when a material runtime, compatibility, dependency, accessibility, ownership, defect, failed-validation, stale-fact, unsafe-drift, or explicit-request trigger exists. Preserve the verified local CPU-first slice and never substitute docs/deploy polish for product evidence.

## Done when

- The selected next task is complete or blocked with exact evidence and an unblocker.
- Public behavior, source, tests, OpenSpec, traceability, PLANS, validation, and continuation state agree.
- Validation runs or an unavailable-runtime/tool blocker is recorded precisely.
- No claim exceeds captured evidence.

## Read first

1. `AGENTS.md`
2. `openspec/changes/build-colab-observer/proposal.md`
3. `openspec/changes/build-colab-observer/specs/**/spec.md`
4. `openspec/changes/build-colab-observer/design.md`
5. `openspec/changes/build-colab-observer/tasks.md`
6. `docs/planning/build-colab-observer/runtime-evidence-hardening-20260725.md`
7. `docs/planning/build-colab-observer/runtime-boundary-hardening-20260717.md`
8. `docs/planning/build-colab-observer/validation.md`
9. `docs/planning/build-colab-observer/traceability-matrix.md`
10. `docs/planning/build-colab-observer/PLANS.md`
11. `docs/planning/build-colab-observer/outer-loop.md`
12. The nearest nested `AGENTS.md` for the write scope.

## Current evidence

- 249 tests pass with `ResourceWarning` promoted to failure and ambient pytest plugin auto-loading disabled.
- Combined line-and-branch coverage is 87.4176%, gate 85%.
- TypeScript/Node 9/9, Chromium 21/21, Jupyter 10/10.
- Local smoke, default/stress benchmarks, isolated 30-second soak, PyTorch, and JAX pass; final package reproduction and extracted-wheel evidence are regenerated after the reconciled source settles.
- Managed Colab, Python 3.11/3.12, reviewed locks/toolchain, manual accessibility, ownership/release, publication/deployment, and OpenSpec archive remain blocked or approval-gated.

## Allowed write scope

Only the paths named by the selected OpenSpec task and its nearest `AGENTS.md`. Use non-overlapping writes for parallel work and update durable evidence ledgers after material discoveries.

## Prohibited actions

Do not install dependencies, resolve packages over the network, mutate Git/remotes, commit, push, open a PR, publish, deploy, create public endpoints, configure secrets/accounts/DNS/payment/permissions, activate telemetry, add keepalive/reconnect/timeout-bypass behavior, or verify/sync/archive OpenSpec without explicit approval.

## Validation

```bash
PYTHONDONTWRITEBYTECODE=1 make check
PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python -W error::ResourceWarning -m pytest   -p no:cacheprovider --cov=colab_observer --cov-branch --cov-fail-under=85
python scripts/check_ui_protocol.py
python scripts/check_python_compat.py
tsc -p packages/dashboard-ui/tsconfig.json --noEmit
python /mnt/data/script_planpack.py validate-pack --root <workspace> --change build-colab-observer
```

Run representative scripts only when their runtime is actually available and approved.

## Stop conditions

Stop for missing authority files, conflicting specs/tasks, scope expansion, credentials, destructive or network/tool-expanding actions, unavailable representative runtime, validation failure without a bounded repair, or overlapping write scope.

## Progress log

Update `docs/planning/build-colab-observer/PLANS.md`, `grill-me.md`, `outer-loop.md`, `validation.md`, and `finalization-report.md` after each material slice.
