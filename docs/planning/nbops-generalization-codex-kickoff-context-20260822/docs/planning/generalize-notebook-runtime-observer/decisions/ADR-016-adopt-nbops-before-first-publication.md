---
status: accepted
type: adr
change: generalize-notebook-runtime-observer
tags:
  - decision
  - naming
  - packaging
  - migration
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# ADR-016: Adopt `nbops` before first publication

**Path:** `docs/planning/generalize-notebook-runtime-observer/decisions/ADR-016-adopt-nbops-before-first-publication.md`  
**Purpose:** Fix the canonical product, distribution, import-package, and CLI identity before platform generalization increases migration cost.  
**Status:** Accepted  
**Decision date:** 2026-08-22

## Context and constraints

The implementation began under a Google-Colab-specific working identity, but the approved architecture is now a platform-capable Python notebook runtime observer. The project has not been publicly released, so this is the lowest-cost point to align the canonical identity with the actual product boundary.

The historical OpenSpec change ID `build-colab-observer` and its planning paths remain stable provenance. They are not the product's canonical name.

## Decision

Adopt the exact lowercase identity `nbops` for:

| Surface | Canonical value |
|---|---|
| Product/brand | `nbops` |
| Python distribution | `nbops` |
| Python import package | `nbops` |
| CLI entry point | `nbops` |
| Default local artifact directory | `nbops` |
| Descriptive category | Local-first runtime observability for Python notebooks |
| Flagship platform copy | `nbops` for Google Colab |

Keep one distribution and one platform-neutral core. Do not create per-platform packages.

A temporary `colab_observer` compatibility shim MAY be retained only to protect existing local notebooks and fixtures during migration. It is explicitly legacy, MUST re-export the same supported API, and MUST NOT remain the canonical documentation path.

## Alternatives considered

| Option | Pros | Cons | Outcome |
|---|---|---|---|
| Keep the provider-specific identity | No local rename work | Misstates the generalized product; increases later migration cost | Superseded |
| Defer naming until three runtime validations | Evidence before public positioning | Freezes the wrong package/import identity first | Rejected |
| Adopt `nbops` now | Platform-neutral, concise, aligned with package/CLI use | Requires bounded pre-public migration | Selected |
| Split per-platform distributions | Clear provider names | Duplicated releases, schemas, support, and security surface | Rejected |

## Consequences

### Positive

- Product identity matches the platform-neutral architecture.
- Package, import, CLI, output paths, docs, and examples converge before publication.
- Google Colab remains the flagship adapter without owning the umbrella name.
- Future Jupyter and Deepnote support no longer looks bolted onto a Colab-only product.

### Negative / tradeoffs

- Current local source paths and fixtures require a controlled migration.
- Legacy artifacts and notebooks need explicit compatibility treatment.
- Remote repository, registry publication, domain, social handles, and trademark clearance remain separate release gates.

## Validation

- Active OpenSpec/planning/handoff surfaces use `nbops` as the canonical name.
- Previously considered alternative names are absent from current active surfaces.
- Historical `build-colab-observer` paths remain stable and are clearly labeled historical.
- New package, import, CLI, artifact, and documentation fixtures use `nbops`.
- Legacy import and artifact behavior is tested separately and labeled legacy.

## Rollback or supersession

Before public release, rollback consists of reverting this ADR and the local package migration together. After publication, any identity change requires a new OpenSpec migration with registry, redirects, compatibility, deprecation, and rollback evidence.

## Review trigger

Revisit only if an authoritative registry, legal, or ownership conflict blocks public use of `nbops`, or if the user explicitly changes the canonical identity.
