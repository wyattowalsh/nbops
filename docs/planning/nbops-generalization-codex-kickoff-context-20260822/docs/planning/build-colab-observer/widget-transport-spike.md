---
status: active
type: research-and-design
change: build-colab-observer
tags:
  - dashboard
  - colab
  - transport
  - accessibility
  - security
updated: 2026-07-12
cssclasses:
  - planning-doc
---

# Local Colab dashboard transport spike

**Checked:** 2026-07-12  
**Decision state:** Candidate implementation exists locally; managed-Colab validation is still required.

## Bottom line

The current official Colab custom-widget-manager path is **not** the default for
`colab-observer` because the inspected source loads its manager JavaScript from a
hosted `gstatic` URL. That conflicts with the product requirement that the
monitor have no runtime CDN dependency.

A narrower first-party pattern exists in Colab's file helpers: the Python side
registers a kernel comm target and inline output JavaScript opens that target
through `google.colab.kernel.comms.open(...)`. This supports a plausible local,
on-demand transport without a public server or custom-widget manager. It is an
implementation inference from current source, not a documented compatibility
guarantee.

## Source table

| Source | Evidence | Confidence | Consequence |
|---|---|---:|---|
| [Colab `_widgets.py`](https://github.com/googlecolab/colabtools/blob/main/google/colab/output/_widgets.py) | `enable_custom_widget_manager` describes third-party website code and references a hosted `ssl.gstatic.com` manager asset. | High for inspected source | Reject as the default under the no-runtime-CDN invariant. |
| [Colab `files.py`](https://github.com/googlecolab/colabtools/blob/main/google/colab/files.py) | A first-party helper registers a comm target and inline JavaScript opens it with `google.colab.kernel.comms.open(id)`. | High for inspected source | Direct comm is a viable candidate for a bounded transport spike. |
| [Jupyter Widgets embedding](https://ipywidgets.readthedocs.io/en/stable/embedding.html) | Standard static/custom embedding examples load widget managers and packages through browser-side scripts, commonly from hosted assets. | High | Do not rely on generic embedding as proof of a local-only Colab path. |

## Implemented candidate

`src/colab_observer/ui/colab_comm.py` now provides an **opt-in experimental**
bridge. It is intentionally absent from the package root and the default
`Observer.display()` path.

The candidate:

- registers one kernel comm target only after explicit invocation;
- sends a bounded versioned snapshot on browser open;
- accepts only fresh-snapshot, bounded-history, pause-presentation, and
  resume-presentation controls;
- keeps pause semantics presentation-only while observation collection continues;
- rejects unknown fields, mismatched run identifiers, arbitrary commands, and
  malformed ranges;
- exposes manual refresh and history query controls rather than background polling;
- renders data through DOM `textContent`, not untrusted HTML insertion;
- supports local CSV copy/download with formula neutralization and safe filenames;
- loads no external script, font, stylesheet, iframe, server, tunnel, or endpoint;
- performs no reconnect loop, keepalive action, anti-idle behavior, or workload
  mutation;
- fails back to the supported script-free static dashboard.

The cross-language candidate contract is recorded in:

- `schemas/dashboard-message.schema.json`;
- `src/colab_observer/schemas/dashboard-message.schema.json`;
- `src/colab_observer/ui/protocol.py`;
- `packages/dashboard-ui/src/protocol.ts`.

## Local validation completed

- JSON Schema and fixture validation.
- Python/TypeScript protocol consistency check.
- Fake comm-manager tests for registration, snapshot, bounded controls, history,
  mismatch rejection, generic errors, and cleanup.
- Malicious text/control and privacy-negative tests.
- Browser document checks for no remote URLs, no fetch/WebSocket/XHR, no polling,
  no dynamic HTML insertion, no executable evaluation, and no reconnect API.
- Node syntax validation of the generated inline JavaScript.
- Keyboard-reachable native controls, live status region, visible focus,
  reduced-motion and forced-color CSS, semantic table, and no color-only state.

These checks demonstrate local contract integrity. They do not establish Colab
browser compatibility or WCAG conformance.

## Required managed-Colab evidence

Before promotion from experimental to supported:

1. Run the reviewed wheel in a clean CPU Colab runtime.
2. Register/display/close the bridge repeatedly without leaked targets or threads.
3. Verify initial snapshot, manual refresh, filtered history, pause/resume, CSV
   copy/download, and static fallback.
4. Exercise notebook reruns, runtime reconnect/disconnect, cell deletion, long
   histories, narrow/wide outputs, 200% and 400% zoom, and theme changes.
5. Confirm no browser or kernel request is made to a product-controlled or
   third-party runtime asset endpoint.
6. Run keyboard, screen-reader, forced-colors, reduced-motion, and chart/table
   parity checks in the actual Colab output environment.
7. Repeat on representative NVIDIA Colab; TPU only requires truthful detection if
   available, never inferred utilization.
8. Capture exact Colab runtime, browser, package, and provider versions.

## Promotion gate

Do not make this transport automatic or public API until the managed-Colab matrix
passes and the no-runtime-CDN invariant is demonstrated through browser/network
evidence. If the direct comm surface proves unstable or unsupported, preserve the
static dashboard as the product path and keep the enhanced transport deferred.

## Local browser and Jupyter update: 2026-07-12

A newly available system Chromium and local Jupyter kernel provided two bounded evidence surfaces without installing dependencies or opening a public endpoint.

The Chromium run uses a mocked `google.colab.kernel.comms.open` surface and blocks every remote request. It passes responsive 320 px and wide layouts, dark/light/forced-colors/reduced-motion media states, keyboard focus order, semantic row headers, live-region updates, bounded controls, local CSV copy/download, formula neutralization, malformed/cross-run/version-mismatch isolation, and later-message recovery. It also exposed and drove repairs for a malformed-message consumer crash and dark-table color inheritance.

The Jupyter run executes the supported static `Observer.display()` path in a real local kernel. It emits one script-free semantic HTML `display_data` payload, persists observations without drops, stops cleanly, and exports HTML, Markdown, and a valid bundle.

These results strengthen local confidence but do not promote the direct comm candidate. They do not prove managed Colab iframe APIs, kernel comm lifecycle, rerun/disconnect behavior, accelerator behavior, or manual assistive-technology compatibility. The candidate remains explicit, experimental, non-default, and absent from the root package API.
