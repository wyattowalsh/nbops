---
status: active
type: risk-register
change: build-colab-observer
tags:
  - risk
  - security
  - delivery
updated: 2026-07-16
cssclasses:
  - planning-doc
---

# Risk register

| ID | Risk | Likelihood | Impact | Mitigation / validation | Owner |
|---|---|---:|---:|---|---|
| R-001 | Monitor overhead distorts workload | Medium | High | cadence budgets, self metrics, bounded queues, soak tests | Core |
| R-002 | Direct comm or widget surfaces change or fail in Colab | Medium | High | explicit experimental adapter, versioned protocol, disclosure, static fallback, managed CPU/GPU browser smoke | UI |
| R-003 | Metrics have provider/platform semantic differences | High | High | source/quality/unit metadata, fixtures, limitations docs | Collectors |
| R-004 | Missing values rendered as zero | Medium | High | schema invariant and UI/report contract tests | Cross-cutting |
| R-005 | Process/environment data leaks sensitive context | Medium | High | minimization, opt-ins, redaction, export preview | Security |
| R-006 | Diagnostic heuristic misleads user | Medium | High | evidence/confidence/alternatives, no auto remediation, negative tests | Diagnostics |
| R-007 | SQLite growth or low disk harms run | Medium | High | batching, size monitoring, warnings, partial/fallback behavior | Storage |
| R-008 | `nvidia-smi` hangs or output is malformed | Low/Medium | Medium/High | timeout, byte limit, strict parser, backoff | GPU collector |
| R-009 | Framework probe initializes or mutates runtime | Low/Medium | High | already-loaded-only detection, import-state tests, local PyTorch/JAX selected-workload smoke, docs | Framework collectors |
| R-010 | TPU status implies nonexistent utilization | Medium | High | separate detection from telemetry, unavailable state | TPU collector |
| R-011 | Enhanced frontend increases install/start cost or trust surface | Medium | Medium | native DOM/SVG candidate first, no runtime assets/CDN, wheel/render benchmarks before selecting a framework | UI/package |
| R-012 | Dashboard inaccessible despite automated pass | Medium | High | manual keyboard/screen-reader/zoom/high-contrast evidence | Accessibility |
| R-013 | Docs drift from snippets/API/rules | High | Medium | generated sources and CI drift checks | Docs |
| R-014 | CI action/dependency compromise | Low/Medium | High | SHA pins, locks, least privilege, update review | CI/security |
| R-015 | Release/deploy secrets exposed to forks | Low | Critical | separate protected jobs/environments, OIDC, no PR secrets | Release |
| R-016 | Name becomes unavailable before publish | Medium | Medium | recheck immediately before repo/PyPI setup; rename ADR if needed | Maintainer |
| R-017 | Scope expands into hosted observability | Medium | Medium/High | proposal non-goals, ADR review, milestone gating | Product |
| R-018 | Users mistake tool for timeout prevention | Medium | High | prominent policy language, scans, no ambiguous marketing | Product/docs |
| R-019 | Dashboard/report contains active remote assets or hidden network behavior | Low/Medium | High | script-free supported dashboard, source/pattern audit, generated-JS check, browser-network proof before transport promotion | Reports/UI |
| R-020 | Planning commands/tool versions become stale | Medium | Medium | source registry recheck and repo-native command discovery | Planning |
| R-021 | Dashboard payload diverges from its public schema or reports false bounds | Low/Medium | High | real-payload schema tests, cross-language version checks, typed truncation metadata, 128-filter bound | UI/protocol |
| R-022 | Opaque run identifier escapes the selected export root or leaves ambiguous partial artifacts | Low after repair | Critical | deterministic single-segment artifact naming, logical-ID preservation, traversal regressions, atomic publication cleanup, ZIP/path audit | Exports/security |
| R-023 | Pre-existing filesystem alias redirects persistence or export writes outside the selected path | Low after repair | Critical | reject database/sidecar and generated-directory aliases, use attempt-owned temporary files, preserve external targets, containment regressions | Storage/exports/security |

## Highest-risk pre-implementation spikes

1. Managed-Colab direct-comm activation, rerun, disconnect, resize, transport loss, browser-network proof, and fallback.
2. Sampler/SQLite/psutil/NVML overhead and failure containment.
3. Frontend bundled size, wheel inclusion, no-CDN behavior.
4. Process/report redaction, opaque-identifier path containment, atomic publication failure, and malicious text rendering.
5. Accessible chart/table/keyboard/live-region proof.

## Rollback map

| Failed surface | Safe rollback |
|---|---|
| Enhanced widget | Disable adapter; retain static fallback/store/export |
| GPU primary provider | Disable primary/use fallback or mark unavailable |
| Diagnostic rule | Disable/version rule; retain raw evidence |
| Optional DuckDB | Remove extra/export path; retain SQLite |
| Docs release | Roll back provider deployment; preserve package |
| Package release | Yank only with maintainer review; release repaired version; never mutate existing artifact |
