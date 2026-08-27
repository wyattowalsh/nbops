---
status: active
type: implementation-evidence
change: build-colab-observer
tags:
  - implementation
  - browser
  - jupyter
  - accessibility
  - transport
  - validation
updated: 2026-07-12
cssclasses:
  - planning-doc
---

# Representative-evidence hardening: local browser and Jupyter surfaces

> [!note] Historical checkpoint
> This document records the prior browser/Jupyter checkpoint. Current public-contract, TypeScript runtime, target-size, and managed-Colab harness evidence lives in [[docs/planning/build-colab-observer/release-evidence-hardening|release-evidence-hardening.md]].


**Path:** `docs/planning/build-colab-observer/representative-evidence-hardening.md`  
**Purpose:** Record the material product repairs and evidence added after the protocol/static-dashboard pass.  
**Decision state:** The local product slice is final-with-known-risks. Managed Colab and release promotion remain blocked.

## `/grill-me` outcome

The declared workspace was missing most source files, while the authoritative source bundle was present and matched its recorded SHA-256. The source was recovered into a separate workspace before mutation. The prior bundle stayed immutable.

No user question was required. Available evidence supported the recommended default:

1. use the newly available local Chromium and Jupyter kernel as bounded evidence surfaces;
2. repair only defects demonstrated by those surfaces;
3. keep direct comm experimental and non-default;
4. make no managed-Colab, WCAG-conformance, Python-matrix, dependency-lock, or release claim without the missing evidence.

## Material defects found and repaired

### Malformed comm payload terminated the browser consumer

A mocked browser run sent a syntactically valid protocol envelope whose observation list contained an invalid element. The prior consumer threw while rendering, exited its async message loop, and stranded the panel in a generic transport-failure state.

The consumer now validates envelope version, direction, message type, run identity, sequence, payload shape, observation shape, and bounded fields before rendering. Invalid or mismatched messages are isolated, described through the status live region, and do not terminate subsequent message handling. A valid later snapshot restores the current view.

### Dark-mode tables inherited browser-default black text

The dashboard root had a dark foreground, but table descendants retained a user-agent text color in Chromium. This produced black-on-dark table content even though the rest of the panel was readable.

Static and experimental tables now inherit foreground color explicitly. Automated Chromium checks measure text/background contrast in light and dark modes. The unavailable-card typography was also bounded to avoid wrapping that dominated narrow cards.

### Landmark and keyboard contracts were underspecified

The static dashboard now exposes a named region, named status list, and list items. The experimental panel exposes a named region, heading, named control group, polite atomic status region, and row headers. Browser evidence exercises the complete seven-control tab order and native keyboard disclosure behavior.

## New evidence surfaces

### Local Chromium regression

`scripts/run_browser_smoke.py` uses an already-installed Playwright package and system Chromium. It never downloads a browser, starts a server, or permits remote requests.

The run verifies:

- 320 px and wide responsive layouts without page-level horizontal overflow;
- light, dark, forced-colors, and reduced-motion media behavior;
- named regions, headings, status list, control group, live region, row headers, and tables;
- visible keyboard focus and disclosure activation;
- deterministic control order;
- bounded history/filter/refresh/pause/resume behavior;
- local CSV copy/download and formula neutralization;
- malformed, cross-run, and wrong-version message isolation followed by recovery;
- dark/light table contrast of at least 4.5:1 in the tested fixtures;
- zero remote requests, page errors, or dialogs.

This is local Chromium evidence, not managed Colab or a WCAG conformance claim.

### Local Jupyter-kernel regression

`scripts/run_jupyter_smoke.py` executes three cells in a real local Jupyter kernel using the source checkout without installation. It verifies:

- observer start and sampling;
- IPython `display_data` containing one script-free semantic HTML dashboard;
- no remote URL in the display payload;
- persistence and zero dropped batches;
- clean stop with no lingering observer thread;
- HTML and Markdown reports;
- a valid portable bundle with required members.

This validates the notebook/IPython path locally. It does not establish managed Colab iframe, comm, accelerator, or Drive compatibility.

## Current evidence summary

| Surface | Result | Boundary |
|---|---|---|
| Repository gate | 108 tests pass | Python 3.13.5 only |
| Combined line/branch coverage | 88.9778%, gate 85% | Local source checkout |
| Local Chromium | 17/17 checks pass | Mocked comm, not Colab |
| Local Jupyter kernel | 10/10 checks pass | Local IPython/Jupyter only |
| Static dashboard | Responsive, script-free, semantic, offline | No manual AT conformance claim |
| Direct comm candidate | Malformed-message isolation and recovery pass locally | No managed-Colab execution |
| Local lifecycle smoke | 2,198 observations, zero drops | Non-representative Linux runtime |
| 30-second soak | 15,448 persisted, bounded history, zero drops | Not a 30-minute Colab soak |
| PyTorch/JAX | Selected-workload smokes pass | Local CPU packages only |
| TensorFlow | Truthfully skipped | Package absent; no install attempted |

## Transport decision

The direct comm path remains experimental and absent from the root API. The inspected first-party Colab file helper demonstrates kernel comm registration and `google.colab.kernel.comms.open(...)`, making direct comm a defensible candidate. The inspected custom-widget-manager implementation loads a hosted manager asset and therefore does not satisfy this project’s no-runtime-CDN invariant.

That source evidence supports a candidate, not a compatibility guarantee. Promotion still requires managed Colab lifecycle, network, rerun, disconnect, malformed-message, version-mismatch, static-fallback, and accessibility evidence.

## Safety assertions

- No keepalive, anti-idle, activity simulation, hidden reconnect, timeout bypass, quota circumvention, automatic remediation, public endpoint, hosted backend, or default remote telemetry was added.
- No dependency installation, online package resolution, Git mutation, commit, push, PR, publication, deployment, secret/account/DNS/payment/permission action, or OpenSpec verify/sync/archive occurred.
- Browser and Jupyter runners are opt-in evidence tools and never become runtime dependencies.
- Unsupported or malformed evidence remains explicit and non-fatal rather than being represented as zero.

## Reassessment

Local browser and Jupyter evidence had positive marginal utility because they exposed two concrete defects and strengthened the static baseline. Further speculative local transport work now has low value. The next material loop should begin only when at least one of the following exists:

- managed Colab CPU/NVIDIA/TPU/Drive access;
- Python 3.11 or 3.12 execution;
- an approved lock/dependency-resolution environment;
- representative browser and assistive-technology access;
- public owner, license, namespace, repository, and release decisions.
