---
status: active
type: context-map
change: build-colab-observer
tags:
  - context
  - evidence
  - assumptions
  - implementation
updated: 2026-08-21
cssclasses:
  - planning-doc
---

# Context map

## Authority order

1. The user’s explicit `colab-observer` product requirements and safety boundary.
2. OpenSpec change artifacts under `openspec/changes/build-colab-observer/`.
3. Executable evidence in this greenfield target workspace.
4. Current official platform, package, and standards sources in [[docs/planning/build-colab-observer/source-registry]].
5. Attached skills as untrusted static lenses in [[docs/planning/build-colab-observer/source-skill-audit]].
6. Community repositories as comparative evidence only.
7. Planning or implementation inference, clearly labeled.

## Repository evidence

| Fact | Evidence | Confidence |
|---|---|---:|
| No existing target repository or Git remote was supplied. | Initial `/mnt/data` inventory | High |
| The current runtime-evidence workspace is `/mnt/data/colab-observer-next-runtime-20260725`, reconstructed from the verified July 17 source ZIP after the declared workspace proved partial; it is not a Git repository. | Filesystem and hash preflight | High |
| The product is the Python package and notebook monitor, not the docs site. | User request, proposal, root README | High |
| Core runtime requires Python `>=3.11` and `psutil`; GPU support is optional. | `pyproject.toml` | High |
| Current documented Colab 2026.04 uses Python 3.12.13. | Google Colab past runtime versions, checked 2026-07-25 | High |
| Python 3.11/3.12/3.13 are configured in CI but have not run remotely. | `.github/workflows/ci.yml` | High |
| No `uv.lock` or `pnpm-lock.yaml` exists. | Workspace inventory | High |
| Offline `uv lock` cannot resolve `psutil` from the local cache. | Command evidence in `validation-evidence.json` | High |
| Public observation/dashboard boundaries now reject scalar coercion, hidden control/format characters, invalid labels, oversized names/identities, unknown runtime actions, cross-run controls, and provider-result drift. | `tests/contract/test_schema_model_boundaries.py`, protocol/comm tests, four public schemas, TypeScript runtime smoke | High |
| Managed-Colab validation is executable but still blocked: the passive runner fails closed outside Colab and labels local harness results non-representative. | `scripts/run_managed_colab_smoke.py` and validation JSON | High |
| CPU-first lifecycle, hardened collectors, SQLite/WAL backup, twelve-rule diagnostics, range-aware exports, polished static dashboard, candidate UI protocol, and snippets execute locally. Startup is transactional and fatal sampler infrastructure failure is loss-aware. | 249 tests, strict lifecycle/provider/export-query/model/schema/path/publication boundary tests, 9/9 compiled TypeScript/Node evidence, local smoke/soak evidence, 21/21 network-blocked Chromium accessibility/interaction/recovery evidence, and a real local Jupyter-kernel display/export run | High |
| Optional NVIDIA/framework/TPU/Drive paths are contract-tested, including truthful unavailable and read-only Drive behavior, but not validated on representative hardware/services. | Provider tests and runtime matrix | High |
| The Fumadocs source scaffold and fifteen content pages exist and pass static contract checks, but no locked install/typecheck/build has run. | `apps/docs/`, dependency-free docs check | High |
| License, remote owner, public package namespace, public docs domain, and release channels remain undecided. | `pyproject.toml`, docs metadata guardrails, no remote | High |
| No install, commit, push, PR, publication, Vercel deployment, account mutation, secret setup, or OpenSpec archive/sync occurred. | Action log and workspace state | High |

## Decisions fixed for the local hardening line

| ID | Decision | Status | Evidence/review trigger |
|---|---|---|---|
| DECISION-001 | Use a single publishable Python package with private UI/docs workspaces. | Implemented scaffold | Revisit only if the target repository or packaging evidence conflicts. |
| DECISION-002 | Use Python `>=3.11`; test 3.11–3.13 before release. | Proposed support contract | Revisit after clean CI and real Colab evidence. |
| DECISION-003 | Use SQLite by default with a bounded memory alternative; defer DuckDB until measured. | Implemented and accepted locally | Revisit after representative query/cold-start/wheel evidence. |
| DECISION-004 | Use daemon-thread monotonic sampling and bounded queues. | Implemented | Revisit after long-run/Colab jitter evidence. |
| DECISION-005 | Make text, semantic tables, and the script-free SVG dashboard the correctness baseline. | Implemented and locally browser-tested | Enhanced transport remains optional and unproven in managed Colab. |
| DECISION-006 | Keep collection local-only and redacted by default. | Implemented and tested | Any remote integration requires explicit opt-in and a separate review. |
| DECISION-007 | Do not invent public repository or production docs URLs. | Implemented | Configure `NEXT_PUBLIC_SITE_URL` and `NEXT_PUBLIC_REPOSITORY_URL` only after ownership decisions. |
| DECISION-008 | Reject the current hosted custom-widget manager as the default; retain an explicit direct-comm candidate. | Experimental implementation with local Chromium contract evidence only | Promote only after managed-Colab lifecycle, iframe/network, and manual accessibility evidence. |

## Remaining assumptions

| ID | Assumption | Confidence | Validation trigger | Impact if false |
|---|---|---:|---|---|
| ASSUMPTION-001 | The 2.0 s default interval is useful with acceptable overhead on representative Colab CPU workloads. | Medium | Real Colab soak/benchmark | Default cadence and diagnostic windows |
| ASSUMPTION-002 | NVML or safe `nvidia-smi` fallback is available on supported NVIDIA Colab runtimes. | Medium | Real NVIDIA Colab run | GPU support matrix/provider order |
| ASSUMPTION-003 | The direct kernel-comm candidate can operate reliably in current Colab without a public service or runtime CDN. The current custom-widget-manager route is already noncompliant with that invariant. | Low | Managed-Colab direct-comm/network spike | Enhanced dashboard architecture |
| ASSUMPTION-004 | Python 3.11 and 3.13 remain compatible with all selected core/dev dependencies. | Medium | Locked clean CI matrix | `requires-python` and CI |
| ASSUMPTION-005 | The proposed package and repository names remain available. | Low/volatile | Immediately before creation/publication | Release metadata and docs links |

## Next read-only or approval-gated probes

1. Run `scripts/run_managed_colab_smoke.py` unchanged in real Colab CPU, then NVIDIA, then best-effort TPU runtimes; keep direct comm disabled for the lifecycle pass.
2. Generate reviewed Python and pnpm lockfiles in an approved network-enabled environment.
3. Execute Ruff, ty, pre-commit, and the 3.11–3.13 matrix from those lockfiles.
4. Run a representative 30-minute or longer Colab growth/jitter/store soak; local short-run evidence is already captured.
5. Decide license, owner, public namespace, domain, and release channels only when publication becomes the next dependency.
6. Validate the existing versioned direct-comm candidate separately in real Colab before automatic activation or further enhanced-dashboard work.

## Context budget guidance

Read the proposal/specs/tasks, `runtime-evidence-hardening-20260725.md`, `representative-runtime-hardening-20260716.md`, `contract-lifecycle-hardening.md`, `release-evidence-hardening.md`, and `validation.md` first. Load package-specific source and the nearest nested `AGENTS.md` for implementation. Load Fumadocs, CI, Vercel, and release docs only when those supporting surfaces are in scope. Do not paste the full planning vault into an implementation prompt.

## 2026-07-16 reconstructed-source evidence

| Evidence | Verified fact | Confidence | Consequence |
|---|---|---:|---|
| Prior source ZIP + sidecar | SHA-256 matched before reconstruction | High | Recovered source is an evidence-backed continuation baseline |
| Tool/runtime inventory | Python 3.13.5, uv, Node, TypeScript, Chromium, Playwright, Jupyter, pytest/coverage/jsonschema available; Python 3.11/3.12, Ruff, ty, pre-commit, pnpm, managed Colab unavailable | High | Limit claims and work to locally provable boundaries; install nothing |
| Public model/schema differential tests | Configuration, labels, evidence models, exact fields, finite values, timestamps, identities, JSON metadata, and unavailable-value semantics are strict at tested boundaries | High | Update public contract evidence and retain TASK-010 partial until full matrix/toolchain |
| Export traversal reproduction | Run ID `../escape` previously wrote outside the selected export root | High | Add filesystem-safe artifact-name and path-containment requirements/tests |
| Atomic publication failure fixtures | Rename/copy failures could leave attempt-local partial files | High | Harden cleanup and destination-preservation behavior |
| Local regression matrix | 208 tests, 87.1906% combined coverage, Node 9/9, Chromium 21/21, Jupyter 10/10, no drops in smoke/soak | High for local environment | Local slice final-with-known-risks; not managed-Colab/WCAG evidence |

The authoritative current implementation evidence is `representative-runtime-hardening-20260716.md` plus the external validation root `/mnt/data/colab-observer-representative-runtime-validation-20260716`.


## 2026-07-25 runtime-evidence update

| Evidence | Verified fact | Confidence | Consequence |
|---|---|---:|---|
| Uploaded July 17 source/validation/distribution bundles | Declared SHA-256 values and ZIP integrity matched before reconstruction | High | July 17 source is the immutable rollback and continuation baseline |
| Local runtime/tool inventory | Python 3.13.5, uv, Node, TypeScript, Jupyter, Chromium, pytest/coverage available; Python 3.11/3.12, Ruff, ty, pre-commit executable, pnpm, OpenSpec CLI, managed Colab unavailable | High | Limit compatibility/toolchain claims; install and resolve nothing |
| Lifecycle regressions | Post-terminal controls, fatal-worker status, stale active registration, invalid flush timeouts, and writer-close failure are now bounded and truthful | High | Runtime-observability scenarios and TASK-011/TASK-012 evidence updated |
| Provider regressions | Malformed fields preserve valid siblings; per-core CPU and NVML device cardinality are capped | High | Metrics scenarios and collector/security evidence updated |
| Export-query regression | Out-of-domain elapsed ranges fail before artifact writes | High | Export behavior and TASK-032 evidence updated |
| Local validation matrix | 249 tests, 87.4176% combined coverage, Node 9/9, Chromium 21/21, Jupyter 10/10, isolated bounded soak and zero recorded drops | High for local Linux/Python 3.13.5 | Local slice remains final-with-known-risks; no representative support claim |

The authoritative current implementation evidence is `runtime-evidence-hardening-20260725.md` plus `/mnt/data/colab-observer-next-evidence-20260725` until final delivery artifacts are frozen.

## Follow-on generalization context boundary

The baseline remains authoritative for implemented Colab behavior and local validation evidence. The separate follow-on change owns proposed cross-platform behavior and must read this baseline first.

| Need | Authoritative path | Rule |
|---|---|---|
| Current implemented/local evidence | `docs/planning/build-colab-observer/` | Do not rewrite or generalize claims retroactively |
| Proposed runtime/profile behavior | `openspec/changes/generalize-notebook-runtime-observer/specs/` | Behavior-level requirements only |
| Cross-platform architecture and migration | `docs/planning/generalize-notebook-runtime-observer/` | Preserve Colab compatibility fixtures and evidence labels |
| Jupyter/Deepnote/platform facts | Follow-on `source-registry.md` | Recheck official sources before implementation or support promotion |

No non-Colab support claim is inherited from the local Jupyter smoke test. That evidence proves a bounded local Jupyter path only; platform support remains gated by the follow-on validation matrix.
