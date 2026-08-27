---
status: proposed
type: display-design
change: generalize-notebook-runtime-observer
tags:
  - display
  - accessibility
  - transports
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Display transport strategy

**Path:** `docs/planning/generalize-notebook-runtime-observer/display-transport.md`  
**Purpose:** Define the universal static baseline, capability negotiation, enhanced transport boundaries, and accessibility parity.  
**Status:** Proposed  

## Transport layers

```text
Semantic dashboard model
├── text snapshot                         universal
├── static HTML + SVG + semantic tables  supported baseline in rich frontends
├── download/export controls             capability-gated
├── Colab direct comm                    experimental/non-default
├── Jupyter widget/comm                  future evidence-gated option
└── provider-native integration          future, platform-specific
```

## Selection algorithm

1. Build the semantic snapshot independently of transport.
2. Determine available transport capabilities from profile evidence.
3. Apply explicit user preference if supported and approved.
4. Select the strongest validated transport.
5. On activation or runtime failure, return to static/text without changing observation state.
6. Record transport status, limitations, and fallback reason.

## Static baseline requirements

- No remote scripts, runtime CDN, public server, or hosted backend.
- Semantic regions, headings, status text, tables, and accessible names.
- Bounded local SVG charts.
- Visible focus where controls exist.
- Reduced motion and forced-colors/high-contrast support.
- Non-color-only severity and unavailable-state labels.
- Every chart has summary/table/CSV parity.

## Colab direct comm

Remain explicit, experimental, and absent from default/root API until managed Colab validates:

- comm target registration/open;
- iframe lifecycle;
- refresh, pause, history, filters, and CSV;
- disconnect and kernel restart;
- malformed/version/cross-run messages;
- no polling, hidden reconnect, remote assets, public endpoint, or keepalive;
- static fallback and accessibility behavior.

## Generic Jupyter

Static IPython display is the first support claim. A widget or comm transport is optional and must not require the Jupyter Server provider. The architecture must tolerate Notebook 7, JupyterLab, JupyterHub, VS Code, and unknown frontends without assuming equal capabilities.

## Deepnote

Start with static output. Deepnote-specific rich controls require direct evidence and should not duplicate built-in machine-monitoring behavior unless they add meaningful history, scope, diagnostics, or export value.

## Protocol evolution

- Include profile/scope/support/limitations in snapshots.
- Version Python, JSON Schema, and TypeScript together.
- Keep payload history, evidence, labels, errors, and tables bounded.
- Reject malformed raw input before sanitizing for presentation.
