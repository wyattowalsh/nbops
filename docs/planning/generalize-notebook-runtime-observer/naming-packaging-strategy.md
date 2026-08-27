---
status: accepted
type: planning
change: generalize-notebook-runtime-observer
tags:
  - naming
  - packaging
  - migration
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# `nbops` naming and packaging strategy

**Path:** `docs/planning/generalize-notebook-runtime-observer/naming-packaging-strategy.md`  
**Purpose:** Define the exact canonical identity, migration boundary, publication gates, and anti-fragmentation rules.  
**Status:** Accepted for planning and implementation

## Decision

The exact lowercase canonical identity is `nbops`.

| Surface | Canonical value | Migration rule |
|---|---|---|
| Product/brand | `nbops` | Use in all current user-facing copy |
| Distribution | `nbops` | New installation and build metadata |
| Import package | `nbops` | New examples and public API |
| CLI | `nbops` | New command documentation and entry point |
| Source package | `src/nbops/` | Owns implementation after migration |
| Default product directory | `nbops` | For new output roots and artifacts |
| Docs title | `nbops` | Platform pages use `nbops for <platform>` |
| Tagline | Local-first runtime observability for Python notebooks | Describes scope without claiming host/server visibility |

Google Colab remains the flagship adapter and acquisition wedge:

> **`nbops` for Google Colab**

## Historical and legacy identifiers

The stable historical OpenSpec ID `build-colab-observer` remains unchanged. Its path is provenance, not the current product name.

A pre-`nbops` Python import or artifact identifier may remain temporarily only when executable compatibility fixtures justify it. Such a surface is:

- labeled legacy;
- non-canonical;
- thin and deterministic;
- covered by migration tests;
- excluded from new examples and primary docs;
- removable only through a later approved compatibility decision.

## One-distribution rule

Do not create Colab, Jupyter, Deepnote, or JupyterHub distributions. Platform behavior belongs in adapters under one core release.

Potential extras are allowed only for unique optional dependencies, such as an explicitly installed Jupyter Server provider. Extras do not change the canonical identity.

## Pre-public migration plan

1. Freeze existing behavior, signatures, defaults, artifacts, and local notebooks in fixtures.
2. Add `nbops` package/import/CLI identity tests.
3. Move implementation ownership to `src/nbops/`.
4. Add a bounded legacy shim only if fixtures or detected users require it.
5. Migrate current install/import examples, notebook snippets, generated docs, output defaults, report titles, bundle metadata, and schema IDs.
6. Keep legacy artifact readers and provenance labels.
7. Run a whole-repository identity scan and exact clean-wheel tests.
8. Build unpublished distributions named `nbops`.
9. Stop before remote repository rename, registry upload, domain/handle changes, announcements, or redirects without explicit approval.

## Preliminary namespace signal

Checked on 2026-08-22:

- The exact PyPI project URL for `nbops` returned 404.
- The exact GitHub owner URL for `nbops` returned 404.

These are only preliminary namespace signals. They are not registry reservation, legal clearance, trademark analysis, or publication approval.

## Identity drift gate

The gate fails when any active current surface uses a different canonical name:

- proposal, specs, design, tasks, ADRs;
- package metadata and source package;
- install/import/CLI examples;
- notebook snippets and default output paths;
- schema IDs, reports, bundles, and support metadata;
- docs titles, SEO metadata, and handoffs;
- manifests and generated artifacts.

Historical IDs and artifact filenames pass only when clearly classified as historical/legacy.

## Rollback

Before publication, roll back the package, import, CLI, output, schema, and docs changes as one unit. Do not leave a mixed identity. After publication, any identity change requires a separate migration proposal with package registry, redirects, deprecation, ownership, and rollback evidence.
