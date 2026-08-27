---
status: active
type: implementation-evidence
change: build-colab-observer
tags:
  - implementation
  - dashboard
  - protocol
  - compatibility
  - validation
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Evidence-gated hardening — dashboard contract and transport candidate

**Path:** `docs/planning/build-colab-observer/evidence-gated-hardening.md`  
**Purpose:** Record the product work completed after the CPU/storage hardening pass and distinguish local evidence from managed-Colab claims.  
**Decision state:** Local implementation is final-with-known-risks; managed-Colab promotion remains blocked.

## `/grill-me` outcome

The authoritative source ZIP was valid, while the declared workspace was incomplete. The source was reconstructed into a new working directory and the prior bundle remained immutable. No user question was required because the source bundle, OpenSpec, and local runtime evidence were sufficient to choose the recommended default: continue only with locally demonstrable product hardening and stop before dependency resolution, managed-Colab claims, or release operations.

The highest-value safe gaps were:

1. a publicly versioned dashboard constant without a corresponding protocol/schema;
2. no polished product dashboard beyond the correctness fallback;
3. no bounded local transport candidate to evaluate in Colab;
4. no Python 3.11 syntax gate or cross-language protocol check;
5. no reusable framework or extracted-wheel smoke runner.

## Product changes

### Versioned dashboard protocol

A transport-neutral `1.0.0` message contract now covers:

- kernel-to-UI snapshots, deltas, acknowledgements, and errors;
- UI-to-kernel controls limited to snapshot request, bounded history query, presentation pause, and presentation resume;
- sequence ranges, recovery indicators, run identity, and bounded history metadata;
- capability, observation, diagnostic, status, and presentation payloads;
- strict rejection of arbitrary commands, unknown fields, invalid ranges, oversized filters, and mismatched run identifiers.

The contract is represented in Python, TypeScript, root JSON Schema, wheel-bundled JSON Schema, and fixtures. A real-snapshot validation found and repaired a material serializer defect: generic list truncation inserted a string sentinel into a typed `Observation[]`, violating the schema and making the reported row count disagree with the payload. Typed arrays now preserve element types, top-level protocol arrays remain bounded at their schema limits, nested evidence remains separately bounded, and metric filters are capped at 128 unique names.

### Modern static dashboard

The supported notebook fallback is now a polished, script-free, local dashboard with:

- responsive CPU, RAM, GPU, VRAM, disk, and network cards;
- bounded SVG sparklines with semantic table parity;
- latest-metric and capability tables;
- diagnostic evidence, limitations, and non-destructive suggestions;
- explicit exact, estimated, stale, and unavailable states;
- visible focus, semantic regions, native controls, reduced-motion CSS, forced-colors support, and non-color status labels;
- no runtime CDN, public service, remote asset, script tag, or telemetry.

The text renderer and HTML report/export path remain usable when notebook HTML is unavailable.

### Opt-in direct Colab comm candidate

The current official custom-widget-manager route was not selected as the default because the inspected manager source references a hosted runtime asset. A narrower direct comm pattern used by first-party Colab helpers was therefore implemented as an explicitly experimental candidate.

The candidate:

- registers one comm target only after explicit invocation;
- sends an initial bounded snapshot and responds to bounded controls;
- exposes manual refresh, metric-filtered history, row limits, presentation pause/resume, and local CSV copy/download;
- neutralizes CSV formulas and sanitizes local filenames;
- writes browser content through `textContent` and `replaceChildren`;
- contains no polling, reconnect loop, keepalive, public endpoint, runtime CDN, fetch, XHR, WebSocket, eval, or workload mutation;
- falls back to the supported static dashboard when prerequisites are unavailable.

It is intentionally absent from the package root and default `Observer.display()` path. It remains a candidate until managed-Colab browser, network, lifecycle, and accessibility evidence passes.

### Compatibility and release evidence

New dependency-free checks cover:

- Python 3.11 grammar parsing across source, tests, scripts, examples, and notebook source;
- Python metadata alignment for 3.11 through 3.13;
- Python/JSON-Schema/TypeScript protocol version and enum alignment;
- TypeScript no-emit compilation using the already available global compiler;
- generated inline JavaScript syntax using the already available Node runtime;
- extracted-wheel smoke without installation;
- deterministic local CycloneDX SBOM generation for declared direct dependencies and artifact hashes, with no license, vulnerability, or transitive-resolution claims.

A reusable framework smoke runner imports only the selected workload framework before starting the observer. Local evidence passes for installed PyTorch and JAX, shows no observer-triggered import of other frameworks, and records TensorFlow as unavailable rather than installing it.

## Local evidence

| Surface | Result | Boundary |
|---|---|---|
| Repository gate | Final result recorded in `validation.md` | Local Python 3.13 only |
| Dashboard schema | Real snapshot and bounded history validate | No Colab browser execution |
| Static dashboard | Script-free, no remote URLs, semantic tables and SVG trends | Automated/local checks only |
| Direct comm JavaScript | Node syntax check passes | No managed-Colab execution |
| TypeScript protocol | Global `tsc --noEmit` passes | No frozen pnpm environment |
| Python compatibility | All discovered Python files parse with 3.11 grammar | Not a 3.11/3.12 runtime test |
| Framework smoke | PyTorch and JAX pass locally; TensorFlow absent/skipped | Not representative of Colab |
| CPU smoke/benchmarks | Zero dropped batches in final local runs | Regression signals, not budgets |
| 30-second soak | Bounded history, clean SQLite/backup, no drops/read failures/threads | Not a 30-minute Colab soak |

## Promotion gates

The enhanced transport and release candidate cannot be promoted until all applicable evidence exists:

1. clean Python 3.11, 3.12, and 3.13 runs with reviewed lockfiles;
2. managed Colab CPU lifecycle, display, stop, export, and long-soak evidence;
3. representative NVIDIA NVML and fixed-query fallback evidence;
4. mounted Drive and best-effort TPU/XLA evidence;
5. real Colab direct-comm lifecycle, rerun, disconnect, no-network, and static-fallback checks;
6. keyboard, screen-reader, zoom, contrast, forced-colors, reduced-motion, and chart/table parity review in the actual notebook surface;
7. reviewed dependency licenses/advisories and public owner/license/repository decisions;
8. explicit separate approval before publication, deployment, secrets, accounts, permissions, commit, push, PR, or OpenSpec sync/archive.

## Reassessment

Further local dashboard polish without a managed-Colab transport/browser surface has low marginal value. The next material loop should begin only when at least one of these becomes available: an approved dependency-resolution environment, Python 3.11/3.12, managed Colab CPU/NVIDIA/TPU/Drive, a browser/assistive-technology test surface, or public ownership/release decisions.
