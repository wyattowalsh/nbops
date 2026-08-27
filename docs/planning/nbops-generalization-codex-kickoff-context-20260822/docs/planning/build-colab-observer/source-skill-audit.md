---
status: complete
type: source-audit
change: build-colab-observer
tags:
  - skills
  - security
  - provenance
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Attached skill audit

## Scope and method

Nine attached skill bundles were treated as untrusted reference material. Only text and source-like files were extracted into a temporary working area. No bundled script, hook, installer, network action, or configuration mutation was executed.

### Static validation result

| Check | Result |
|---|---:|
| Skill bundles | 9 |
| Extracted safe text/source files | 270 |
| JSON parsed | 67 passed / 0 failed |
| Python AST parsed | 101 passed / 0 failed |
| Skill scripts executed | 0 |
| Plugin binaries installed | 0 |

Excluded or ignored material included macOS metadata, `.DS_Store`, Python bytecode, caches, and archive packaging noise.

## Skill-to-plan lens

| Bundle | Useful lens imported | Applied to | Not imported |
|---|---|---|---|
| `design.zip` | Interface classification, design-system precedence, keyboard/focus/semantic/contrast/reduced-motion rules, rendered proof | Dashboard and docs UX/accessibility plans | Mutation/install/browser-MCP instructions |
| `host-panel.zip` | Multi-perspective crux review, option comparison, synthesis | ADRs and risk review | Any external model/tool execution |
| `namer.zip` | Collision, clarity, memorability, domain/registry recheck | Product-name caveat | Brand automation or registration claims |
| `research.zip` | Primary-source preference, evidence chain, uncertainty and freshness | Source registry and ecosystem audit | Automated browsing scripts |
| `review.zip` | Severity-based audit, supply-chain/CI/compatibility lenses | Quality and final validation | Repo mutation and review bots |
| `docs-steward.zip` | Docs framework classification, content graph, drift checks, current-version research, migration safety | Fumadocs site and docs CI | Framework install/sync scripts |
| `data-wizard.zip` | Data-quality, statistical, dashboard, and visualization framing | Metrics model, diagnostics, charts | Analysis scripts and implicit dependencies |
| `javascript-conventions.zip` | pnpm/lockfile/package-root discipline, TypeScript quality workflow | Dashboard/docs workspace and CI | Blind package-manager migration |
| `python-conventions.zip` | uv/pyproject/Ruff/ty/pytest conventions | Python package and CI | Dependency installation or config writes |

## Material recommendations retained

- Use rendered and interaction evidence for UI acceptance, not screenshots alone.
- Keep operational dashboards dense, scannable, and truthful.
- Make accessibility structural: visible focus, semantic HTML, keyboard paths, contrast, reduced motion, and non-hover alternatives.
- Detect and preserve local package-manager/build conventions once a repository exists.
- Keep docs content generated from source contracts where drift is likely.
- Separate evidence, inference, and recommendation.
- Use one owner for shared/generated files and only parallelize non-overlapping writes.

## Risks discovered in the bundles

- Some skills contain executable Python and reference optional dependencies.
- Some guidance assumes browser, MCP, installed tools, or live package registries.
- Version snapshots and “latest” guidance can become stale.
- Broad multi-agent or automatic sync guidance can expand agency beyond this planning request.

Mitigation: normalized lens notes under `resources/skill-lenses/` contain only the relevant planning guidance and no executable automation.
