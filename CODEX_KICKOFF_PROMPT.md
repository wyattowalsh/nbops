# Codex kickoff: adopt `nbops` and generalize notebook runtime observability

You are Codex working in the target repository on OpenSpec change:

`generalize-notebook-runtime-observer`

## Goal

Implement the largest safe, compatibility-first, dependency-ready slice of the `nbops` generalization change.

The exact canonical current identity is:

```text
Product:             nbops
Local repository:    nbops
Python distribution: nbops
Python import:       nbops
CLI:                 nbops
Source package:      src/nbops/
Default artifact dir:<platform-appropriate>/nbops/
Tagline:             Local-first runtime observability for Python notebooks.
Flagship adapter:    Google Colab
```

Begin in this order:

1. `TASK-103-freeze-colab-compatibility-fixtures`
2. `TASK-105-freeze-nbops-migration-fixtures`
3. `TASK-106-implement-nbops-identity-migration`
4. `TASK-110-implement-runtime-profile-models`
5. `TASK-111-implement-evidence-validation`
6. `TASK-112-implement-adapter-registry`

Do not begin adapter extraction, support-tier promotion, interactive-transport promotion, or release work until TASK-103, TASK-105, and TASK-106 are reviewed and green.

## Product boundary

`nbops` is one platform-neutral Python notebook runtime observability system. Google Colab is the flagship and best-supported adapter. Jupyter, IPython, Deepnote, JupyterHub, and future notebook environments are evidence-gated platform surfaces, not separate products.

The stable OpenSpec ID `build-colab-observer` and baseline paths under `openspec/changes/build-colab-observer/` and `docs/planning/build-colab-observer/` remain historical provenance. Do not bulk-rename or rewrite them. See `LEGACY_IDENTITY_NOTICE.md`.

A prior source/import namespace in the target repository is migration input. Retain a temporary compatibility shim only when verified external usage requires one. It must delegate to `nbops`, remain tested, and have a removal criterion.

## Current authoritative state

- Canonical identity decision: accepted as `nbops`.
- Historical implemented baseline: `openspec/changes/build-colab-observer/`.
- Active proposed change: `openspec/changes/generalize-notebook-runtime-observer/`.
- Completed planning tasks: TASK-100, TASK-101, TASK-102, TASK-104.
- Follow-on product implementation: not started.
- Next critical tasks: TASK-103, then TASK-105 and TASK-106. TASK-104 is complete in this planning revision.
- External repository, registry, domain, publication, deployment, and announcement actions: not authorized.

Treat this bundle as planning authority and evidence, not permission to overwrite newer target-repository facts. Reconcile it with the actual repository before editing.

## Read first

1. `IDENTITY_MAP.md`
2. `LEGACY_IDENTITY_NOTICE.md`
3. Root and nearest path-local `AGENTS.md`
4. `openspec/changes/build-colab-observer/proposal.md`
5. `openspec/changes/build-colab-observer/specs/**/spec.md`
6. `openspec/changes/build-colab-observer/design.md`
7. `openspec/changes/build-colab-observer/tasks.md`
8. `openspec/changes/generalize-notebook-runtime-observer/proposal.md`
9. `openspec/changes/generalize-notebook-runtime-observer/specs/**/spec.md`
10. `openspec/changes/generalize-notebook-runtime-observer/design.md`
11. `openspec/changes/generalize-notebook-runtime-observer/tasks.md`
12. `docs/planning/generalize-notebook-runtime-observer/README.md`
13. `docs/planning/generalize-notebook-runtime-observer/context-map.md`
14. `docs/planning/generalize-notebook-runtime-observer/source-registry.md`
15. `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-016-adopt-nbops-before-first-publication.md`
16. `docs/planning/generalize-notebook-runtime-observer/naming-packaging-strategy.md`
17. `docs/planning/generalize-notebook-runtime-observer/compatibility-migration.md`
18. `docs/planning/generalize-notebook-runtime-observer/architecture.md`
19. `docs/planning/generalize-notebook-runtime-observer/runtime-profile-model.md`
20. `docs/planning/generalize-notebook-runtime-observer/platform-adapter-contract.md`
21. `docs/planning/generalize-notebook-runtime-observer/measurement-scope.md`
22. `docs/planning/generalize-notebook-runtime-observer/storage-profiles.md`
23. `docs/planning/generalize-notebook-runtime-observer/display-transport.md`
24. `docs/planning/generalize-notebook-runtime-observer/platform-support-matrix.md`
25. `docs/planning/generalize-notebook-runtime-observer/validation.md`
26. `docs/planning/generalize-notebook-runtime-observer/traceability-matrix.md`
27. `docs/planning/generalize-notebook-runtime-observer/PLANS.md`
28. `docs/planning/generalize-notebook-runtime-observer/outer-loop.md`
29. `docs/planning/generalize-notebook-runtime-observer/task-graph.json`
30. `docs/planning/generalize-notebook-runtime-observer/codex-handoff.md`

## Session-start challenge

Begin with a read-only `/grill-me` pass when available. Otherwise apply the same protocol:

- Inspect repository and supplied evidence before asking.
- Ask one material question only when the answer changes architecture, behavior, compatibility, security, privacy, acceptance, packaging, or release state and cannot be inferred safely.
- Include the recommended/default answer, consequences, blocker status, and affected artifacts.
- Continue safe useful work when evidence or the default is sufficient.

Record assumptions, decisions, discoveries, blockers, changed paths, and validation evidence in PLANS, validation, traceability, and outer-loop state.

## TASK-103: freeze behavior before moving identity

Freeze executable behavior for at least:

- Current observer configuration and lifecycle.
- `ObserverConfig`, `Observer`, `observe()`, `start_observer()`, `stop()`, `display()`, report export, and bundle export.
- Current Google Colab defaults and platform-specific behavior.
- Idempotent stop, context-manager behavior, terminal/failure/loss states, and same-cell rerun behavior.
- Current SQLite/run/report/bundle schemas and representative prior fixtures.
- Text and semantic static dashboard fallback.
- Canonical three-cell notebook flow.
- Absence of keepalive, anti-idle, hidden reconnect, timeout bypass, quota circumvention, default telemetry, public services, hosted backends, runtime CDNs, and remote code.

Initial write scope:

```text
tests/contract/
tests/fixtures/
docs/planning/generalize-notebook-runtime-observer/PLANS.md
docs/planning/generalize-notebook-runtime-observer/validation.md
docs/planning/generalize-notebook-runtime-observer/traceability-matrix.md
```

Do not change product behavior merely to make a fixture pass. A fixture that exposes undocumented behavior is an implementation discovery. Record it and reconcile OpenSpec before encoding a compatibility assumption.

## TASK-105 and TASK-106: freeze and implement the `nbops` migration

After TASK-103 is green and the TASK-104 identity decision is confirmed, complete TASK-105, then TASK-106:

- Update local package metadata to distribution `nbops`.
- Move the canonical source package to `src/nbops/`.
- Use `nbops` for current imports and CLI.
- Update current snippets, examples, schemas, reports, output defaults, docs, and new artifact metadata.
- Keep Google Colab behavior under an adapter/profile.
- Preserve supported prior databases, reports, and bundles.
- Add a previous-import shim only when verified external usage requires it.
- Do not create duplicate independently evolving packages.

Allowed write scope is bounded by repository evidence and the machine task graph. It may include `pyproject.toml`, the verified current source-package path under `src/`, `src/nbops/`, tests, notebooks, examples, schemas, and active migration docs. It does not authorize remote repository changes or publication.

## Subsequent architecture invariants

- One platform-neutral core and one canonical `nbops` distribution.
- No per-platform package split.
- Runtime identity is faceted, not one mutually exclusive platform enum.
- Kernel-local evidence is not server, host, quota, or sibling-kernel evidence.
- Unknown scope is not host scope; unavailable limits are not unlimited.
- Missing metrics are unavailable, stale, estimated, or degraded, never silently zero.
- Adapters are passive, bounded, deterministic, and failure-isolated.
- Text and semantic static HTML remain the universal correctness path.
- Interactive transports are additive and evidence-gated.
- Support tiers require representative runtime evidence.
- Active working storage and finalized artifact destinations are separate.

## Security and approval boundaries

Do not:

- install or resolve dependencies;
- enable network access or external runtime/account access;
- enable or configure a Jupyter Server extension;
- mount user storage or call platform account APIs;
- add telemetry, hosted backend, public endpoint, remote code, or runtime CDN dependencies;
- add keepalive, anti-idle, hidden reconnect, timeout bypass, quota circumvention, or automatic remediation;
- read, request, print, or embed secrets;
- commit, push, open a PR, create or rename a remote repository, reserve a package, change a domain, publish, deploy, change permissions, announce, or apply/sync/archive OpenSpec.

These require separate explicit approval.

## Validation

1. Discover and preserve the target repository's real commands and package-manager conventions.
2. Run the smallest focused tests for each task first.
3. Run the repository gate after each dependency-complete slice.
4. Run branch-aware coverage when the existing environment supports it.
5. Validate OpenSpec through the repository's confirmed command surface.
6. Do not install missing tools merely to satisfy proposed commands.
7. Classify evidence honestly: local deterministic, fixture/simulated, installed wheel, representative managed runtime, browser/manual accessibility, or blocked.
8. Do not promote support from local mocks.
9. Run a current-identity scan proving all active canonical surfaces use `nbops` and only allowlisted historical/migration contexts retain prior identifiers.

Known baseline commands to verify before use include:

```bash
make check
make coverage
make smoke
python scripts/check_precommit.py
python scripts/check_distribution.py dist
```

## Done when

- TASK-103 and the completed TASK-104 decision are prerequisites for TASK-105.
- TASK-106 migrates current canonical surfaces to `nbops` without unsupported behavior changes.
- Every completed task satisfies its requirement, write scope, validation, and evidence contract.
- Supported Google Colab behavior and prior artifacts remain covered.
- No unsupported platform, scope, storage, transport, support-tier, accessibility, performance, or publication claim is introduced.
- PLANS, validation, traceability, task state, risks, and handoff agree.
- Remaining work is dependency-ready, explicitly blocked with an unblocker, or deferred with rationale.

## Stop conditions

Stop when:

- target-repository evidence contradicts the plan in a way that changes behavior or architecture;
- compatibility cannot be captured without an unapproved breaking change;
- installation, network access, external runtime/account access, server enablement, secrets, destructive migration, remote identity action, publication, deployment, or OpenSpec lifecycle action is required;
- representative evidence is required for a claim but unavailable;
- write scopes overlap another active writer;
- validation fails without a bounded evidence-backed repair;
- work drifts toward docs, CI, deployment, external branding, or polish while higher-value compatibility and core work remains.

## Final response

Report completed, partial, blocked, and deferred task IDs; changed paths; observable behavior; exact validation commands/results; evidence classes; compatibility and migration impact; residual risks; and the next dependency-ready task. Do not claim implementation, support, accessibility, publication, or release readiness without executed evidence.
