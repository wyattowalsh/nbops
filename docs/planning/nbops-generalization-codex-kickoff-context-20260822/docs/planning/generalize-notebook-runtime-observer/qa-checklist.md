---
status: active
type: qa-checklist
change: generalize-notebook-runtime-observer
tags:
  - qa
  - validation
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# QA checklist

## Identity and migration

- [ ] Current product, distribution, import, CLI, source target, docs, defaults, and new-artifact metadata use `nbops`.
- [ ] Google Colab appears as the flagship adapter, not a competing umbrella identity.
- [ ] Stable historical OpenSpec IDs and baseline paths remain resolvable.
- [ ] TASK-103 behavior fixtures pass before TASK-104 package migration.
- [ ] A prior import shim exists only from verified compatibility evidence.
- [ ] Prior supported databases, reports, and bundles remain readable.
- [ ] Competing candidate names are absent from active current surfaces.
- [ ] External package/repository/domain/trademark readiness is documented before any external action.

## OpenSpec and tasks

- [ ] Every requirement uses `### Requirement:` and MUST/SHALL behavior.
- [ ] Every requirement has at least one scenario.
- [ ] Implementation detail stays in design/tasks/plans.
- [ ] Task IDs are unique and dependencies form a DAG.
- [ ] `tasks.md` and `task-graph.json` contain the same tasks.
- [ ] Parallel tasks have non-overlapping writes and independent validation.

## Runtime truthfulness

- [ ] Kernel/process/container/server/host/quota scope is explicit.
- [ ] Unknown scope or limits are not promoted to host or unlimited.
- [ ] Platform tiers match representative evidence.
- [ ] Static text/HTML/table/CSV paths remain usable without interactive transport.

## Safety

- [ ] No default telemetry, hosted backend, public endpoint, runtime CDN, or remote code.
- [ ] No automatic remediation, keepalive, anti-idle, reconnect automation, timeout bypass, or quota circumvention.
- [ ] No install, network, Git, publication, deployment, account, permission, domain, or secret action without approval.

## Packaging and handoff

- [ ] Kickoff prompt, handoff, goals, PLANS, validation, traceability, risks, and manifests agree.
- [ ] JSON/YAML, OpenSpec schemas, links, manifests, and archive safety pass.
- [ ] Deterministic ZIP reproduces byte-for-byte and clean extraction matches source.
