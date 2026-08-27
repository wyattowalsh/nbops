---
status: proposed
type: planning
change: generalize-notebook-runtime-observer
tags:
  - compatibility
  - migration
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Compatibility and migration to `nbops`

**Path:** `docs/planning/generalize-notebook-runtime-observer/compatibility-migration.md`  
**Purpose:** Preserve supported Colab behavior and legacy evidence while moving every current public surface to `nbops`.  
**Status:** Proposed

## Migration invariants

- `nbops` is canonical for new install, import, CLI, docs, examples, defaults, reports, bundles, and schema identity.
- The historical `build-colab-observer` OpenSpec change ID remains stable.
- A legacy import shim is compatibility-only and never appears in new quickstarts.
- Existing supported run databases and bundles remain readable.
- Runtime-profile additions are additive and versioned.
- No mixed current identity may pass release validation.
- Colab behavior remains protected while Colab becomes an adapter under `nbops`.

## Current-to-target map

| Surface | Historical/current implementation evidence | Target |
|---|---|---|
| Distribution | Pre-`nbops` development distribution | `nbops` |
| Import | Legacy package path | `nbops` |
| Source ownership | Legacy source package | `src/nbops/` |
| CLI | None or legacy development command | `nbops` |
| Colab default directory | Provider-specific product directory | `/content/nbops/` |
| Generic default directory | Provider-neutral selected root | `<root>/nbops/` |
| Report/bundle product metadata | Legacy identity where present | `nbops` plus explicit legacy provenance on old inputs |
| Schema identifiers | Legacy URNs where present | Versioned `urn:nbops:*` identifiers, with legacy readers retained |
| Platform copy | Product equated with Colab | `nbops` for Google Colab |

## Compatibility fixture set

Before moving implementation files, freeze:

- supported public function/class signatures;
- lifecycle and rerun behavior;
- static display semantics;
- current Colab capability and failure behavior;
- current SQLite/report/bundle read behavior;
- representative old notebook imports;
- default-output behavior and path containment;
- no-telemetry/no-public-server/no-keepalive boundaries.

Then add target fixtures for:

- `pip`/wheel metadata using `nbops`;
- `from nbops import ...`;
- `nbops` CLI help/version behavior;
- `/content/nbops/` defaults;
- `nbops` report/bundle/schema metadata;
- no stale candidate names in active docs and generated artifacts.

## Legacy import policy

The migration implementation SHOULD include a temporary legacy shim when repository evidence shows current notebooks or fixtures depend on it. The shim:

- re-exports only supported public API;
- contains no separate implementation;
- does not fork state or versioning;
- does not import absent optional frameworks;
- has explicit compatibility tests;
- is absent from current quickstarts and primary API docs.

If target-repository evidence proves no compatibility need, removal requires recording that evidence before implementation.

## Artifact and schema migration

New writers use `nbops` product metadata and versioned schema identifiers. Legacy readers preserve old identity as provenance rather than rewriting it. Unknown new fields remain ignorable when safe; missing new fields remain unknown/legacy rather than fabricated.

## Default path migration

Current documentation and new default constructors use `nbops` child directories. User-provided explicit paths remain unchanged. Legacy directories are never silently moved or deleted.

## Validation matrix

| Gate | Evidence |
|---|---|
| New import and CLI | Clean-wheel and command tests |
| Legacy import, if retained | Compatibility fixture |
| Colab behavior | Three-cell fixture and managed-runtime matrix |
| Legacy artifact reads | Golden database/report/bundle fixtures |
| New identity metadata | Schema/report/bundle golden tests |
| Default path containment | Unit/security negatives |
| Whole-repo identity convergence | Deterministic text/path scan |
| No split package implementation | Source tree and import graph audit |

## Rollback

Before publication, revert the package move, build metadata, CLI entry point, current docs/examples, default path, and new schema IDs as one atomic migration. Preserve legacy artifact fixtures. Do not roll back only one user-facing surface and leave a split identity.
