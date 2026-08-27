---
status: proposed
type: support-matrix
change: generalize-notebook-runtime-observer
tags:
  - support
  - evidence
  - platforms
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Platform support matrix

**Path:** `docs/planning/generalize-notebook-runtime-observer/platform-support-matrix.md`  
**Purpose:** Separate product priority, detected capabilities, current evidence, intended tier, blockers, and promotion gates.  
**Status:** Proposed  

## Tier definitions

| Tier | Meaning |
|---|---|
| Validated | Mandatory representative runtime, compatibility, failure, package, and accessibility gates pass for the stated scope |
| Preview | Core path works in representative evidence, but one or more non-critical platform-specific gates remain |
| Experimental | Explicit opt-in behavior with incomplete lifecycle/compatibility evidence |
| Unverified | Architecture or fixtures exist; no sufficient representative runtime evidence |
| Unsupported | Explicitly outside package capability or known incompatible |

## Current and target matrix

| Environment | Product priority | Current evidence | Current planning tier | Target scope | Mandatory promotion evidence |
|---|---:|---|---|---|---|
| Plain Python 3.13 local | Core | Existing source/wheel/local smokes | Legacy local evidence; revalidate after generalization | Process/process-tree/container-visible, text, store/export | Clean source/wheel, failure, package, performance |
| IPython local | Core | Current static/Jupyter evidence | Legacy local evidence; revalidate | Rich static display plus core | MIME/static semantics, no-network, accessibility automation |
| Managed Colab CPU | Flagship | Existing harness only; real run absent | Unverified for current release | Colab profile, `/content`, static UI, lifecycle/export | Real managed run, package, overhead, policy negative |
| Managed Colab NVIDIA | Flagship | Provider fixtures only | Unverified | NVML/`nvidia-smi`, framework, process attribution | Real hardware fields/fallback/failure/performance |
| Colab Drive/TPU | Flagship | Detection/read-only fixtures | Unverified | Mounted Drive profile, TPU/XLA presence limitations | Real mounted/unmounted and TPU runtime evidence |
| Colab direct comm | Optional | Local mocked Chromium | Experimental | Explicit enhanced transport | Real comm lifecycle, disconnect, iframe, accessibility, no-network proof |
| JupyterLab 4 | Next first-class | Local Jupyter kernel, frontend not fully profiled | Preview candidate | Kernel/process/container scope + static UI | Clean wheel in JupyterLab, browser semantics, failures, Python matrix |
| Notebook 7 | Next first-class | No distinct representative run | Unverified | Same as JupyterLab scope | Clean wheel Notebook 7 lifecycle/display/export |
| JupyterHub kernel-only | Important | No representative hub | Unverified | Kernel-local generic fallback | Real deployment profile, scope labels, permission failures |
| Optional Jupyter Server provider | Optional | Design only | Experimental candidate | Authenticated server-visible metrics | Explicit install, authn/authz, bounded endpoints, no-public-bind, disable |
| Deepnote | Preview target | Official docs only | Unverified | Static UI, profile, `/tmp` working, `/work` finalization | Real project lifecycle/storage/package/failure evidence |
| VS Code notebooks | Future | No evidence | Unverified | Generic Python/IPython where applicable | Representative frontend/package run |
| Kaggle/other hosted Python notebooks | Future | No evidence | Unverified | Generic fallback | Provider-specific evidence before any platform label |
| R/Julia/other kernels | Out of scope | Python package cannot run there | Unsupported | None | Separate architecture/change |

## Promotion rules

- Detection alone never promotes a tier.
- Evidence is tied to runtime versions and recheck triggers.
- A platform can be validated for static display while an enhanced transport remains experimental.
- A platform can be validated for kernel scope while server scope remains unavailable.
- Failed or stale mandatory evidence downgrades the affected scope, not unrelated generic behavior.
- Marketing/docs tables are derived from or checked against this evidence matrix.
