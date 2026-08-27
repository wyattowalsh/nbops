---
status: proposed
type: source-registry
change: generalize-notebook-runtime-observer
tags:
  - sources
  - research
  - notebook-observability
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Source registry

**Path:** `docs/planning/generalize-notebook-runtime-observer/source-registry.md`  
**Purpose:** Record source-backed platform facts, confidence, implications, conflicts, and recheck triggers.  
**Status:** Proposed  

## Source table

| Source | Checked | Supports | Confidence | Plan impact | Recheck trigger |
|---|---|---|---|---|---|
| Current repository and `build-colab-observer` OpenSpec | 2026-08-21 | Generic-core versus Colab-coupling map; current API/evidence state | High | Follow-on change, compatibility baseline | Any current-source patch |
| Jupyter architecture | 2026-08-21 | Kernel is a separate process; frontend/server/kernel are distinct | High | Explicit scope and optional server boundary | Major Jupyter architecture change |
| “What is Jupyter?” | 2026-08-21 | Jupyter Server orchestrates kernels and frontend communication | High | Do not infer server ownership from kernel package | Server lifecycle change |
| Jupyter Server extensions/security/auth | 2026-08-21 | Server extensions add handlers; authenticated/authorized access is required | High | Optional integration must be explicit and least-privilege | Jupyter Server auth API change |
| `jupyter-resource-usage` README/release | 2026-08-21 | Existing server/child and IPython-kernel usage UI | High | Differentiate on history/scope/diagnostics/bundles; consider interoperability | Major project API/release change |
| IPython display documentation | 2026-08-21 | Rich HTML/SVG display is a compatible frontend capability | High | Static MIME output is cross-notebook baseline | IPython display contract change |
| Deepnote Jupyter interoperability | 2026-08-21 | Core `.ipynb` compatibility with caveats for specialized blocks | High | Treat as preview target, not exact frontend parity | Deepnote notebook model change |
| Deepnote integrated file system | 2026-08-21 | `/work` object-backed; `/tmp` fast and ephemeral | High | Separate active working and final artifact destinations | Storage docs/environment change |
| Deepnote hardware | 2026-08-21 | Built-in machine monitoring exists | Medium/High | Do not compete as a basic gauge; focus differentiated evidence | Hardware UI/model change |
| Colab runtime/FAQ | 2026-08-21 | Dynamic resources/limits; policy boundary | High | No guarantees, keepalive, timeout bypass, or quota circumvention | Runtime/policy update |
| Colab widget and file-helper source | 2026-08-21 | Hosted widget manager assets; direct comm precedent | Medium/High | Keep direct comm experimental pending managed evidence | `colabtools` source change |
| WCAG 2.2 | 2026-08-21 | Accessibility target and testable success criteria | High | Automated plus manual validation; no unsupported conformance claim | WCAG revision |

## Canonical URLs

- https://docs.jupyter.org/en/stable/projects/architecture/content-architecture.html
- https://docs.jupyter.org/en/latest/what_is_jupyter.html
- https://jupyter-server.readthedocs.io/en/latest/developers/extensions.html
- https://jupyter-server.readthedocs.io/en/latest/operators/security.html
- https://jupyter-server.readthedocs.io/en/stable/api/jupyter_server.auth.html
- https://github.com/jupyter-server/jupyter-resource-usage
- https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html
- https://deepnote.com/docs/importing-and-exporting-jupyter-notebooks
- https://deepnote.com/docs/importing-data-to-deepnote
- https://deepnote.com/docs/selecting-hardware
- https://research.google.com/colaboratory/runtime-version-faq.html
- https://research.google.com/colaboratory/faq.html
- https://github.com/googlecolab/colabtools/blob/main/google/colab/output/_widgets.py
- https://github.com/googlecolab/colabtools/blob/main/google/colab/files.py
- https://www.w3.org/TR/WCAG22/

## Evidence rules

- Official docs/source define platform behavior; local runtime evidence defines support.
- Community examples may inform design but cannot promote a support tier.
- Frontend identity remains uncertain when only kernel evidence exists.
- Dates and recheck triggers travel with support evidence.
- Conflicting sources are recorded rather than silently reconciled.
