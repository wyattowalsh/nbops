# Repository agent guidance for `nbops`

## Source of truth

- Canonical identity: `nbops`
- Active change: `openspec/changes/generalize-notebook-runtime-observer/`
- Implemented historical baseline: `openspec/changes/build-colab-observer/`
- Active planning: `docs/planning/generalize-notebook-runtime-observer/`
- Baseline evidence: `docs/planning/build-colab-observer/`
- Durable execution state: `docs/planning/generalize-notebook-runtime-observer/PLANS.md`

## Read first

1. `CODEX_KICKOFF_PROMPT.md`
2. `IDENTITY_MAP.md`
3. Active proposal/specs/design/tasks
4. ADR-016 and compatibility migration
5. Context map, validation, traceability, PLANS, and handoff
6. The nearest nested `AGENTS.md` for every assigned path

## Working rules

- Implement by task ID and dependency order.
- Freeze observable behavior before moving package identity.
- Use `nbops` for every current canonical product, distribution, import, CLI, source target, and new-artifact identity.
- Preserve `build-colab-observer` only as a stable historical change ID and evidence path.
- Add a legacy import shim only from verified compatibility evidence.
- Keep OpenSpec specs behavior-level; put packages, files, commands, and sequencing in design/tasks/plans.
- Update PLANS, validation, traceability, and task evidence when implementation discoveries change the plan.
- Do not invent commands, APIs, support tiers, platform scope, or migration obligations.

## Safety and approvals

Stop before installs, network access, external runtimes/accounts, server enablement, Git remote changes, commits, pushes, PRs, publication, deployment, domains, permissions, secrets, or OpenSpec apply/sync/archive without explicit approval.

Never add telemetry, a hosted backend, public endpoint, runtime CDN, remote code, automatic remediation, keepalive, anti-idle, hidden reconnect, timeout bypass, or quota circumvention.

## Done criteria

- Completed tasks satisfy their requirements and validation.
- Current canonical surfaces agree on `nbops`.
- Supported Colab behavior and portable artifacts remain covered.
- Legacy compatibility is bounded and evidence-backed.
- Support claims match representative evidence.
- PLANS, tasks, validation, traceability, risks, and handoff agree.
