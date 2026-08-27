---
status: proposed
type: research
change: generalize-notebook-runtime-observer
tags:
  - research
  - ecosystem
  - notebook-observability
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Research brief: notebook runtime observability abstraction

**Path:** `docs/planning/generalize-notebook-runtime-observer/research.md`  
**Purpose:** Synthesize current ecosystem and platform evidence into concrete OpenSpec and architecture implications.  
**Status:** Proposed  

## Bottom line

Generalization is technically justified because the existing core is already largely provider-neutral. The product should **not** become a generic status-bar monitor. Its cross-platform identity should remain scoped historical runtime observability with diagnostics, accessible fallbacks, and portable evidence.

## Findings

### Jupyter is a layered system

A Jupyter deployment separates frontend, server, and kernel. A Python package running inside the kernel can reliably describe its process and visible operating-system environment; it cannot infer the entire notebook document, Jupyter server, sibling kernels, workspace quota, or host without a separate authorized evidence source.

**Plan consequence:** make measurement scope first-class and design optional server evidence as a separate trust/deployment boundary.

### IPython is the right static-display baseline

Rich MIME display can work across compatible notebook frontends while text remains a terminal/failure fallback.

**Plan consequence:** support text and script-free semantic HTML/SVG/tables before any provider-specific transport.

### Jupyter already has a resource-usage extension

`jupyter-resource-usage` monitors server/child resources and can expose kernel-specific usage for IPython kernels. A new product that only shows CPU/RAM duplicates established behavior.

**Plan consequence:** differentiate on bounded history, explicit scope/quality, accelerator/framework evidence, diagnostics, accessibility parity, and portable bundles. Evaluate interoperability rather than replacement.

### Deepnote is compatible but operationally different

Deepnote supports core Jupyter notebook workflows and already has machine performance UI. Its persistent `/work` location is object-backed and not optimized for many small files; `/tmp` is fast and ephemeral.

**Plan consequence:** Deepnote begins as preview/static support with a storage profile that stages active SQLite work locally and finalizes artifacts explicitly to persistent storage. Do not auto-copy or mount.

### Colab remains the strongest wedge

Colab resources and limits vary, and accelerator assignment does not prove utilization. The current policy boundary prohibits keepalive/anti-idle/circumvention. Its first-party widget manager uses hosted assets, while direct comm exists in source but lacks representative lifecycle evidence for this product.

**Plan consequence:** keep Colab flagship behavior, Drive/TPU diagnostics, and direct comm isolated; static output remains supported and direct comm remains experimental.

## Ecosystem comparison

| Surface | Existing strength | Gap this product can fill |
|---|---|---|
| Colab built-in monitor | Immediate machine view | Historical scoped evidence, diagnostics, exports, integrity, accessible parity |
| Deepnote hardware panel | Machine selection/performance | Portable history, framework/GPU evidence, storage diagnostics, support bundle |
| `jupyter-resource-usage` | Server/child and kernel usage UI | Local-first run history, diagnostics, portable reports, cross-provider scope model |
| Generic OS tools | Detailed host/process metrics | Notebook lifecycle, semantic display, framework context, notebook-safe exports |
| Experiment trackers | Training metrics and remote collaboration | No-account local runtime health and environment evidence |

## OpenSpec implications

- Add profile, scope, adapter, storage, display, support, diagnostics, migration, and security behavior domains.
- Protect current API/defaults as full migration requirements.
- Require evidence-gated support tiers.
- Prohibit automatic server/storage/account mutation.
- Preserve static output and chart/table/export parity.

## Uncertainties

- Kernel-visible signals may not establish frontend identity reliably.
- Deepnote environment markers and filesystem behavior need live verification.
- JupyterHub deployments vary by spawner, cgroups, permissions, and installed extensions.
- Optional server integration may not provide enough incremental value to justify maintenance.
- Neutral branding may reduce the clarity and SEO value of the Colab wedge.

## Recommended experiments

1. Implement profile serialization and generic fallback behind compatibility fixtures.
2. Extract Colab assumptions behind an internal adapter without changing public defaults.
3. Run local JupyterLab and Notebook 7 wheel smokes.
4. Run a Deepnote preview smoke with `/tmp` active storage and `/work` final artifacts.
5. Spike an authenticated server provider and compare against `jupyter-resource-usage` interoperability.
6. Revisit public naming only after representative Colab plus two non-Colab targets pass.
