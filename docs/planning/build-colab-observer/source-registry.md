---
status: active
type: source-registry
change: build-colab-observer
tags:
  - research
  - sources
  - freshness
updated: 2026-08-21
cssclasses:
  - planning-doc
---

# Source registry

**Checked:** 2026-07-25  
**Rule:** Official and primary sources define current behavior. Community repositories are comparative examples, not platform contracts.

## Current authoritative sources

| Topic | Source | Supports | Confidence | Recheck trigger |
|---|---|---|---:|---|
| Current Colab runtime archive | [Google Colab past runtime versions](https://research.google.com/colaboratory/runtime-version-faq.html) | 2026.04 runtime lists Ubuntu 22.04.5, Python 3.12.13, PyTorch 2.10.0, JAX 0.7.2, and TensorFlow 2.19.0. | High | Before compatibility/release claims |
| Current uv release | [astral-sh/uv releases](https://github.com/astral-sh/uv/releases) | Current CI pin review; 0.11.28 checked 2026-07-11. | High | Before changing lock/CI tooling |
| setup-uv action | [astral-sh/setup-uv releases](https://github.com/astral-sh/setup-uv/releases) | Current v8.3.2 action release and immutable commit pin used by CI. | High | Before workflow updates |
| Local representative evidence | `runtime-boundary-hardening-20260717.md`, `final-assurance-hardening-20260716.md`, `representative-runtime-hardening-20260716.md`, `validation-evidence.json`, alias/provider audit, browser, Jupyter, benchmark, soak, framework, and package evidence | Actual package, network-blocked Chromium, local Jupyter-kernel, runtime, build, and blocker evidence. | High | After implementation or validation changes |
| Colab limits/policy | [Google Colab FAQ](https://research.google.com/colaboratory/faq.html) | Resources and limits vary; idle/runtime limits exist; accelerators should be used when needed. | High | Before public policy wording or runtime compatibility release |
| Colab runtime image | [Google Colab past runtime versions](https://research.google.com/colaboratory/runtime-version-faq.html) | The documented 2026.04 image uses Ubuntu 22.04.5 and Python 3.12.13; this is source evidence, not a substitute for a live smoke run. | High | Before freezing Python or compatibility claims |
| Colab custom widget manager | [googlecolab/colabtools `_widgets.py`](https://github.com/googlecolab/colabtools/blob/main/google/colab/output/_widgets.py) | Current activation source describes third-party code and references a hosted `gstatic` manager asset. | High for inspected source | Before any automatic/custom-widget activation decision |
| Colab direct kernel comm | [googlecolab/colabtools `files.py`](https://github.com/googlecolab/colabtools/blob/main/google/colab/files.py) | A first-party helper registers a kernel comm target and opens it from inline output JavaScript. | High for inspected source | Before promoting the experimental direct-comm candidate |
| Jupyter widget embedding | [Jupyter Widgets embedding](https://ipywidgets.readthedocs.io/en/stable/embedding.html) | Generic embedding commonly relies on browser-side widget manager/package scripts and does not itself prove a local-only Colab path. | High | Before selecting a generic widget adapter |
| Anywidget compatibility | [anywidget documentation](https://anywidget.dev/) and [repository](https://github.com/manzt/anywidget) | Portable custom widget model and compatibility claims; still requires local-asset/runtime evidence for this product. | Medium | Before choosing/pinning a non-Colab UI adapter |
| System metrics | [psutil documentation](https://psutil.readthedocs.io/en/latest/) | CPU, memory, disk, network, process semantics and warm-up caveats. | High | Before collector implementation/version pin |
| NVIDIA metrics | [NVIDIA NVML API reference](https://docs.nvidia.com/deploy/nvml-api/) | GPU utilization, memory, temperature, power, and process telemetry. | High | Before provider compatibility claims |
| NVIDIA Python binding | [nvidia-ml-py on PyPI](https://pypi.org/project/nvidia-ml-py/) | Official Python binding package and release metadata. | High | Before dependency pin/release |
| SQLite | [Python `sqlite3` documentation](https://docs.python.org/3/library/sqlite3.html) | Standard-library database availability and transaction behavior. | High | When minimum Python changes |
| OpenSpec workflow | [OpenSpec concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md), [OPSX workflow](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md) | Change-folder artifacts and current core/expanded workflow profiles. | High | Before naming commands in executable handoff |
| Fumadocs theming | [Fumadocs UI theme](https://fumadocs.dev/docs/ui/theme) | Tailwind v4 requirement and shadcn preset. | High | Before docs scaffold/pin |
| Fumadocs AI/LLM output | [Fumadocs AI search/LLM docs](https://fumadocs.dev/docs/ui/ai) | Framework-supported AI-readable documentation patterns. | High | Before AI-index implementation |
| shadcn/ui | [shadcn/ui introduction](https://ui.shadcn.com/docs) | Open-code, accessible component approach. | High | Before component choice/pin |
| Tailwind CSS | [Tailwind Next.js guide](https://tailwindcss.com/docs/installation/framework-guides/nextjs) | Current v4 integration pattern. | High | Before docs implementation |
| Next metadata | [Next.js metadata and OG images](https://nextjs.org/docs/app/getting-started/metadata-and-og-images) | Metadata, sitemap/robots, social image APIs. | High | Before docs implementation |
| Next JSON-LD | [Next.js JSON-LD guide](https://nextjs.org/docs/app/guides/json-ld) | Structured data and safe serialization guidance. | High | Before structured-data implementation |
| AI search | [Google AI features optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Google treats AI-search optimization as SEO and does not require `llms.txt`. | High | Before public AEO/GEO claims |
| `llms.txt` | [llms.txt proposal](https://llmstxt.org/) | Emerging optional convention for LLM-oriented site maps. | Medium | Before generated format/schema changes |
| Vercel Git delivery | [Vercel for GitHub](https://vercel.com/docs/git/vercel-for-github) | Preview and production deployment integration. | High | Before deployment setup |
| Vercel deployment checks | [Vercel deployment checks](https://vercel.com/docs/deployments/checks) | Current preview/production check behavior. | High | Before protected deployment design |
| GitHub Actions security | [GitHub secure use reference](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) | Least privilege and immutable action pinning. | High | Before workflow implementation/update |
| GitHub action releases | Official `actions/checkout`, `actions/setup-python`, and `astral-sh/setup-uv` release pages | The authored CI pins reviewed full commit SHAs for checkout v7.0.0, setup-python v6.3.0, and setup-uv v8.3.2; recheck before merge. | High | Before workflow merge or dependency refresh |
| pre-commit | [pre-commit documentation](https://pre-commit.com/) | Cross-language local hook management and stages. | High | Before hook config/pin |
| WCAG | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Normative accessibility target. | High | When standard target changes |
| Widget patterns | [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/) | Keyboard and semantic interaction patterns. | High | Before widget implementation |
| Reduced motion | [MDN `prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) | Motion preference behavior. | High | Before UI implementation |
| Accessible data visualizations | [USWDS data visualizations](https://designsystem.digital.gov/components/data-visualizations/) | Equivalent accessible tables and non-color guidance. | High | Before chart design review |
| ECharts accessibility/license | [Apache ECharts accessibility](https://echarts.apache.org/handbook/en/best-practices/aria/) and [repository](https://github.com/apache/echarts) | ARIA options, SVG renderer, Apache-2.0 licensing. | High | Before frontend pin/build |
| Python environment | [uv projects](https://docs.astral.sh/uv/guides/projects/) and [ty configuration](https://docs.astral.sh/ty/reference/configuration/) | Environment, lock and type-check configuration. Local lock generation remains blocked without approved dependency resolution. | High | Before lock/type-check execution |
| Codex Goal mode | [Codex Goal guide](https://developers.openai.com/codex/app/features/goals) and [Codex changelog](https://developers.openai.com/codex/changelog) | Current Goal availability, lifecycle, and compatibility notes. | High | Before using exact Goal controls |
| Codex AGENTS/security | [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) and [approvals/security](https://developers.openai.com/codex/agent-approvals-security) | Durable instruction hierarchy and approval boundaries. | High | Before implementation handoff |
| PyPI publication | [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) and [artifact attestations](https://docs.pypi.org/attestations/) | Proposed tokenless release and provenance path. | High | Before release workflow setup |

## Name availability probe

| Surface | Result on 2026-07-11 | Interpretation |
|---|---|---|
| `https://pypi.org/pypi/colab-observer/json` | 404 | No project was returned at that exact path; this does not reserve the name. |
| `https://github.com/wyattowalsh/colab-observer` | 404 | No repository was returned at that exact path; this point-in-time result neither creates nor reserves a remote. |
| npm exact package path | Registry page blocked the research fetch | Do not claim npm availability; the private dashboard package does not need publication. |

## Source-use rules

- Date-check volatile claims in release/docs changes.
- Do not cite community stars as a product requirement.
- Do not infer TPU utilization from detection sources.
- Do not convert a Colab helper API into a guarantee that it works forever.
- Keep `llms.txt` optional and never describe it as Google Search access control or a ranking requirement.
- Recheck exact package and workflow versions at implementation time and record them in lockfiles, not evergreen planning prose.


## Evidence and validation use

Each current claim must be translated into a requirement, design constraint, task, or validation check. A source link alone is not completion evidence. Runtime claims require captured provider output or a documented unavailable state; release claims require artifact and workflow evidence.

## First-build local evidence hierarchy

1. Source code and tests in this workspace define what is implemented.
2. `validation-evidence.json` records command results, artifacts and blockers.
3. `runtime-evidence/*.json` records short local CPU-only smoke measurements and explicitly marks them non-representative of Colab.
4. Official external sources constrain current platform/tool claims but do not substitute for runtime evidence.
5. Community examples remain illustrative only.

No release claim may be based solely on package metadata, CI configuration, a fake provider, or an external documentation statement.

## Hardening-loop source checks: 2026-07-11

| Source | Claim supported | Confidence | Plan impact |
|---|---|---:|---|
| Google Colab runtime-version FAQ | Current pinnable runtime evidence includes a 2026.04 image with Python 3.12.13; this does not prove package compatibility | High | Keep Python 3.12 in the required matrix and avoid claiming it before execution |
| Google Colab FAQ | Resource availability, limits, idle behavior, rich-output iframes, and Drive I/O characteristics are service-controlled and variable | High | Preserve no-keepalive boundary; require real Colab and mounted-Drive evidence |
| `googlecolab/colabtools` widget manager and file-helper sources | The custom-widget manager references a hosted asset, while a first-party file helper demonstrates direct inline JavaScript/kernel comms | High for inspected source | Reject custom-widget activation as the default; keep the direct-comm implementation experimental until managed-Colab/network evidence passes |
| DuckDB stable Python client docs | DuckDB remains a viable optional analytical adapter, but its product value and runtime cost are separate from SQLite durability | High | Keep DuckDB deferred until approved dependency, cold-start, wheel-size, query, and Colab evidence exist |

Recheck these sources before changing Python support, widget transport, Drive guidance, or optional analytical dependencies.


## Representative-runtime hardening checks: 2026-07-12

| Source | Claim supported | Confidence | Plan impact |
|---|---|---:|---|
| Google Colab runtime-version FAQ | The documented 2026.04 image uses Python 3.12.13 and current framework versions; docs do not prove this package works there | High | Keep Python 3.12 and managed-runtime execution as release gates |
| Google Colab FAQ | Resource limits, accelerator availability, idle/runtime behavior, browser support, iframe behavior, and Drive I/O remain service-controlled | High | Preserve no-keepalive boundary and require real CPU/GPU/TPU/Drive evidence |
| `googlecolab/colabtools` file helper source | First-party code registers kernel comm targets and opens browser comms | High for inspected source | Direct comm remains a technically grounded experiment, not a support guarantee |
| `googlecolab/colabtools` custom widget manager source | The manager loads a hosted `gstatic` asset and warns about third-party code loading | High for inspected source | Do not make that path the default under the no-runtime-CDN invariant |
| Local Chromium accessibility tree and geometry | Current static/experimental fixtures expose named semantics and tested target sizes in system Chromium | High for local fixture | Strengthens automated regression, not WCAG or managed-Colab conformance |
| Local TypeScript/Node execution | Runtime helper rejects invalid controls and emits schema-valid messages | High for Node 22/TS 5.8.3 | Keep runtime parity tests; still run locked web toolchain later |

The passive managed-Colab runner is the preferred next evidence entry point. It never installs packages, mounts Drive, activates direct comm, starts a public service, or substitutes local output for managed-Colab evidence.

## Representative-runtime contract/export checks: 2026-07-16

| Source | Claim supported | Confidence | Plan impact |
|---|---|---:|---|
| Reconstructed source + focused regressions | Public configuration/models reject tested coercive and malformed inputs at construction/decoding boundaries | High | Treat current source/tests as implemented evidence; keep Python matrix/toolchain release gates open |
| Traversal reproduction and fixed regressions | Opaque run IDs can no longer escape the selected export root and remain unchanged in metadata | High | Add path-containment behavior requirements and security validation |
| Atomic publication failure injection | Attempt-local partial files are removed and existing valid destinations are preserved in tested failure paths | High | Strengthen export integrity requirement and package audit |
| Root and wheel schema copies | Four public schema IDs use stable non-network URNs and match tested Python behavior | High | Offline readers use bundled schema/version; no external-domain ownership claim |
| Local validation matrix | 208 tests, 87.1906% combined coverage, Node 9/9, Chromium 21/21, Jupyter 10/10, bounded smoke/soak with zero drops | High for local Linux/Python 3.13.5 | Preserve local final-with-known-risks; do not infer managed-Colab, Python 3.11/3.12, or WCAG support |

Recheck Google Colab runtime and helper-source facts before any compatibility or direct-comm promotion claim. Current external documentation constrains the plan but does not substitute for running `run_managed_colab_smoke.py` inside managed Colab.


## Runtime-evidence checks: 2026-07-25

| Source | Claim supported | Confidence | Plan impact |
|---|---|---:|---|
| Google Colab past runtime versions | The current pinnable `2026.04` image documents Python 3.12.13 and current framework versions; documentation does not prove this package works there | High | Keep Python 3.12 and managed runtime execution as release gates |
| Google Colab FAQ | Resource availability, idle/runtime limits, and accelerator allocations remain variable and service-controlled | High | Preserve observe-only behavior and all no-keepalive/no-bypass requirements |
| `googlecolab/colabtools` widget manager source | The custom widget manager still references hosted `gstatic` code and permits third-party widget loading | High for inspected source | Do not promote this route under the no-runtime-CDN invariant |
| `googlecolab/colabtools` file helper source | First-party code demonstrates kernel comm registration and browser-side comm opening | High for inspected source | Direct comm remains technically grounded but experimental pending managed lifecycle evidence |
| Reconstructed source and focused regressions | Terminal controls, fatal-worker state, field-level provider isolation, provider cardinality, and export-range overflow are now bounded at tested boundaries | High | Update OpenSpec scenarios, tests, traceability, and final assurance evidence |
| Local validation matrix | 249 tests and 87.4176% combined coverage plus Node, Chromium, Jupyter, smoke, benchmark, isolated soak, and framework checks pass | High only for local Linux/Python 3.13.5 | Preserve final-with-known-risks and avoid representative claims |

Recheck these official sources before changing Python support, Colab compatibility, widget transport, or service-policy guidance. They constrain the product boundary but cannot replace managed execution evidence.

## Follow-on source routing

Jupyter architecture, IPython display, Deepnote storage/lifecycle, optional Jupyter Server integration, and cross-platform support-tier sources are maintained in [`docs/planning/generalize-notebook-runtime-observer/source-registry.md`](../generalize-notebook-runtime-observer/source-registry.md).

The baseline registry remains authoritative for Colab-specific runtime, policy, direct-comm, provider, accessibility, package, and local validation claims. Follow-on research may constrain future design, but it does not alter this baseline's executed evidence.
