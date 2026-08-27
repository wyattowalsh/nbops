---
status: proposed
type: openspec-proposal
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - proposal
  - notebook-observability
  - platform-adapters
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Proposal: Generalize the notebook runtime observer

**Path:** `openspec/changes/generalize-notebook-runtime-observer/proposal.md`  
**Purpose:** Define the follow-on change that separates the platform-neutral notebook observability engine from evidence-gated platform adapters while preserving Colab as the flagship product wedge.  
**Status:** Proposed  
**Depends on:** `openspec/changes/build-colab-observer/`

## Why now

The completed local historical `build-colab-observer` slice already contains a mostly platform-neutral engine: lifecycle, bounded sampling, typed observations, collectors, diagnostics, SQLite and memory stores, exports, text/static HTML display, and notebook-safe cleanup. The remaining Google Colab coupling is concentrated in runtime detection, `/content` and Drive behavior, TPU and Colab diagnostics, and the experimental direct-comm transport.

Leaving those assumptions embedded in otherwise generic contracts would make later support for JupyterLab, Notebook 7, JupyterHub, Deepnote, and similar Python notebook environments more expensive and less truthful. Generalizing the architecture now is comparatively reversible. Generalizing support claims without representative runtime evidence would not be. The package identity decision is now separately approved as `nbops` before first publication.

This proposal combines three ordered decisions:

1. **Adopt `nbops` as the canonical local product/package/import/CLI identity before first publication.**
2. **Generalize the engine and evidence model behind that identity.**
3. **Promote each platform only after direct representative validation.**

## Intent

Evolve the implemented Colab-first baseline into `nbops`, a platform-capable Python notebook runtime observability package whose core behavior is independent of any one hosted notebook provider.

The package SHALL describe what it can actually observe from inside the Python runtime, distinguish kernel/process/container/server/host scope, report platform and frontend evidence with confidence, choose storage and display behavior from explicit capabilities, and preserve safe static fallbacks everywhere.

The canonical product, distribution, import package, and CLI identity is now `nbops`. Existing pre-`nbops` imports, artifacts, defaults, and historical OpenSpec paths remain protected only as explicit migration or provenance surfaces.

## Goals

- Extract Colab-specific assumptions from generic lifecycle, storage, diagnostics, display, and metadata contracts.
- Introduce a versioned, faceted runtime profile rather than a single brittle platform enum.
- Make measurement scope and limit provenance explicit so kernel-visible evidence is never presented as server- or host-wide fact.
- Establish generic Python and IPython/static-display baselines.
- Preserve Google Colab as the flagship and strongest platform-specific product position under `nbops`.
- Add JupyterLab/Notebook 7 as the first non-Colab validation target.
- Add Deepnote as a preview target with storage-aware guidance and static display first.
- Define, but do not automatically install or enable, an optional authenticated Jupyter Server integration for server-level evidence.
- Gate support labels, documentation claims, examples, and release decisions on captured runtime evidence.
- Preserve one `nbops` distribution and one core public API; do not split per platform.

## Non-goals

- Replacing the current `build-colab-observer` change or rewriting its validated implementation history.
- Claiming all Jupyter frontends, JupyterHub deployments, hosted notebooks, or Python kernels behave identically.
- Supporting R, Julia, SQL, or other non-Python kernels through this Python package.
- Automatically installing or enabling a Jupyter Server extension.
- Accessing notebook source, server tokens, account APIs, project contents, or unrelated kernels by default.
- Building a hosted control plane, public dashboard, remote telemetry service, or multi-node observability platform.
- Competing primarily as a status-bar CPU/RAM gauge.
- Adding keepalive, anti-idle, hidden reconnect, timeout bypass, quota circumvention, or platform-policy avoidance.
- Renaming a remote repository, publishing to a package registry, acquiring domains/handles, or making external announcements without separate approval.
- Promoting the experimental Colab direct-comm transport without managed-Colab lifecycle evidence.

## Product positioning

The approved positioning is:

> **`nbops`: local-first runtime observability for Python notebooks, built first for Google Colab.**

The defensible cross-platform value is not merely a current CPU or RAM number. It is the combined behavior of:

- bounded time-series observation;
- explicit source, quality, freshness, and scope;
- GPU and framework evidence;
- deterministic diagnostics with alternatives and limitations;
- accessible chart, summary, table, and CSV parity;
- local persistence and portable support bundles;
- redaction, integrity, and partial-loss evidence;
- no account, backend, public port, or default telemetry;
- notebook-safe reruns, cleanup, and degraded modes.

## Scope

### In scope

- Versioned runtime-profile and measurement-scope contracts.
- Platform-neutral core boundaries for lifecycle, sampling, observations, persistence, diagnostics, exports, and static display.
- Evidence-producing adapters for generic Python, IPython, Colab, Jupyter, and Deepnote.
- Storage profiles for ephemeral local, persistent local, mounted cloud, and object-backed workspaces.
- Display capability negotiation for text, static HTML/SVG/table, direct comm, widget, and download surfaces.
- Support tiers and evidence gates that are separate from product priority.
- Platform-aware diagnostics that activate only when required evidence is present.
- Additive migration of run metadata, exports, reports, schemas, examples, docs, and tests.
- Optional authenticated Jupyter Server integration design and spike.
- A bounded legacy import/artifact compatibility policy while `nbops` becomes canonical.

### Out of scope

- Implementing the full follow-on change during this planning pass.
- Public release, rename, repository creation, package publication, deployment, or external announcements.
- Automatic environment mutation, package installation, server configuration, Drive mounting, or notebook restart.
- Unsupported cross-language kernel claims.
- Hosted observability or cross-user aggregation.

## Users and jobs

| User | Job to be done | Required truth boundary |
|---|---|---|
| Colab ML practitioner | Diagnose stalls, pressure, accelerator underuse, and storage risks | Colab/container-visible evidence; no allocation-policy claims |
| Local Jupyter user | Understand the current Python kernel and visible process tree over time | Kernel/process/container scope; no server-wide claim without extension |
| JupyterHub user | Capture portable evidence without assuming hub/server permissions | Kernel-local baseline; optional authenticated server evidence only |
| Deepnote user | Diagnose workload and storage behavior in a managed project | Distinguish `/tmp` ephemeral throughput from `/work` persistence |
| Maintainer/support engineer | Receive a redacted, integrity-checked evidence bundle | Platform profile, scope, support tier, limitations, and provenance preserved |
| Agent or automation | Inspect deterministic local evidence safely | No hidden control, network, keepalive, or automatic remediation |

## Affected behavior domains

- `runtime-profiles`
- `measurement-scope`
- `platform-adapters`
- `storage-profiles`
- `notebook-display`
- `compatibility-support`
- `platform-diagnostics`
- `migration-compatibility`
- `security-policy`

## Approach summary

1. Add a versioned runtime profile composed of independent facets: provider, frontend, kernel, execution scope, resource scope, limit source, storage capabilities, display transports, evidence, confidence, and conflicts.
2. Define adapter contracts that contribute bounded evidence and capabilities but never own the core observer lifecycle.
3. Keep generic system and framework collectors platform-neutral; isolate platform detectors, storage advice, diagnostics, and transports behind registries.
4. Preserve text and script-free semantic HTML/SVG/table output as the universal display baseline.
5. Keep Colab-specific Drive, TPU, runtime warnings, and direct comm behind the Colab adapter.
6. Treat Jupyter Server evidence as an optional, separately installed and authenticated integration, not a kernel entitlement.
7. Promote Jupyter and Deepnote support only after representative smoke, persistence, export, performance, failure, and accessibility evidence.
8. Preserve existing API and export readers; evolve schemas additively with explicit versioning and unknown-field handling.
9. Adopt `nbops` across local package, import, CLI, artifact, default-path, example, and documentation contracts before adapter extraction; keep remote rename and publication approval-gated.

## Key decisions

| Decision | Status | Rationale |
|---|---|---|
| Separate follow-on OpenSpec change | Recommended | Avoids reopening the final-assured `build-colab-observer` scope and preserves audit history. |
| Generalize internals before public claims | Recommended | Lowers future coupling without fabricating compatibility. |
| `nbops` identity with Colab flagship positioning | Accepted | Aligns the umbrella name with the platform-neutral architecture while preserving the sharpest initial wedge. |
| Faceted runtime profile | Recommended | Real notebook environments combine provider, frontend, kernel, container, storage, and transport dimensions. |
| One `nbops` distribution | Accepted | Avoids duplicated release, docs, compatibility, and support burden. |
| Static display as universal baseline | Required | It is local, accessible, portable, and already validated in IPython/Jupyter contexts. |
| Deepnote preview/static first | Recommended | Deepnote already exposes machine performance; differentiated value is history, diagnostics, and portable evidence. |
| Optional Jupyter Server integration later | Recommended | Server-wide evidence is useful but requires installation, authentication, and permissions not guaranteed in managed platforms. |
| External publication only after readiness gates | Required | Registry, repository, domain, and announcement actions are externally consequential and require evidence plus approval. |

## Success criteria

- The original `build-colab-observer` change remains behaviorally unchanged and final-with-known-risks.
- A separate, valid OpenSpec follow-on change contains proposal, full behavior deltas, design, tasks, risks, validation, traceability, and bounded handoff.
- Runtime metadata identifies provider/frontend/kernel/scope/storage/transport facets without claiming more than captured evidence.
- Generic Python/IPython behavior works when no recognized notebook provider is detected.
- Colab-specific behavior remains available through a Colab adapter and existing API defaults remain compatible.
- Jupyter and Deepnote labels cannot advance beyond their evidence tier without representative runtime artifacts.
- Static text/HTML/SVG/table/CSV paths remain usable without JavaScript, a server extension, a public endpoint, or network access.
- Optional server integration requires explicit install/enable action and authenticated authorization.
- Legacy runs and bundles remain readable, with missing new fields represented as unknown rather than inferred.
- The naming decision remains deferred until its explicit validation gate is satisfied.

## Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| “Jupyter support” overstates scope | High | Define execution/resource scope and support tiers; require platform-specific evidence. |
| Adapter system becomes an extension framework too early | High | Keep adapters internal and allowlisted; no third-party plugin API in this change. |
| Platform detection becomes fingerprinting | High | Minimize evidence, redact raw values, avoid network/account APIs, expose confidence and conflicts. |
| Genericization weakens the Colab wedge | Medium/High | Keep Colab first in positioning, examples, and validation priority. |
| Deepnote persistence causes excessive small-file I/O | High | Storage profile distinguishes `/tmp` staging and `/work` persistence; batch and finalize copies. |
| Jupyter Server extension expands attack surface | High | Optional extra, explicit enablement, authenticated/authorized endpoints, local-only defaults, least privilege. |
| Static and enhanced UI behavior drifts | Medium | One semantic model and chart/summary/table/CSV parity tests across transports. |
| Identity migration breaks supported behavior or artifacts | High | Freeze behavior first, use additive schemas, run compatibility tests, and retain only evidence-backed shims. |
| External identity use creates ecosystem confusion | Medium | Keep canonical local identity fixed as `nbops`; require publication-readiness review and explicit approval before external actions. |
| Existing monitor ecosystem makes generic CPU/RAM view undifferentiated | Medium | Position around historical, scoped, diagnostic, accessible, portable evidence rather than status-bar gauges. |

## Open questions

- `QUESTION-GEN-001`: Which two non-Colab environments should be required before considering a neutral public name? Recommended default: local JupyterLab/Notebook 7 and Deepnote.
- `QUESTION-GEN-002`: Should an optional Jupyter Server provider interoperate with `jupyter-resource-usage`, consume its API when available, or remain independent? Recommended default: interoperate and avoid duplicating server gauges.
- `QUESTION-GEN-003`: Should the public API expose `RuntimeProfile` immediately or keep it behind `observer.runtime_profile` until the shape survives representative validation? Recommended default: expose read-only preview metadata first.
- `QUESTION-GEN-004`: What support-tier names should appear publicly? Recommended default: validated, preview, experimental, unverified, unsupported.
- `QUESTION-GEN-005`: Should Kaggle, SageMaker Studio Lab, VS Code notebooks, and Databricks be planned now? Recommended default: record as future candidates, not current implementation scope.

## Sources checked

Checked on **2026-08-21**:

- Jupyter architecture: https://docs.jupyter.org/en/stable/projects/architecture/content-architecture.html
- Jupyter kernels: https://docs.jupyter.org/en/stable/projects/kernels.html
- IPython display: https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html
- Jupyter Server extensions: https://jupyter-server.readthedocs.io/en/latest/developers/extensions.html
- Jupyter Server security: https://jupyter-server.readthedocs.io/en/latest/operators/security.html
- `jupyter-resource-usage`: https://github.com/jupyter-server/jupyter-resource-usage
- Deepnote Jupyter interoperability: https://deepnote.com/docs/importing-and-exporting-jupyter-notebooks
- Deepnote storage: https://deepnote.com/docs/importing-data-to-deepnote
- Deepnote hardware monitor: https://deepnote.com/docs/selecting-hardware
- Deepnote lifecycle: https://deepnote.com/docs/long-running-jobs
- Colab runtime versions: https://research.google.com/colaboratory/runtime-version-faq.html
- Colab policy and limits: https://research.google.com/colaboratory/faq.html
- Colab comm implementation reference: https://github.com/googlecolab/colabtools/blob/main/google/colab/files.py
- Colab custom widget manager: https://github.com/googlecolab/colabtools/blob/main/google/colab/output/_widgets.py
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
