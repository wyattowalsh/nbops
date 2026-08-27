---
status: accepted
type: adr
change: build-colab-observer
tags:
  - adr
  - exports
  - security
updated: 2026-07-17
cssclasses:
  - planning-doc
---

# ADR-009: Separate logical run identity from filesystem artifact naming

## Context

Run IDs are persisted data identifiers and may originate from imported or older run records. Treating an opaque identifier as a directory or ZIP filename allowed path separators and traversal segments to affect export location. The product must preserve the logical ID for traceability without trusting it as a path segment.

## Decision

Keep `run_id` unchanged in models, SQLite, reports, manifests, and exported metadata. Derive a separate deterministic filesystem artifact name:

- preserve identifiers that already satisfy the reviewed single-segment safe alphabet and reserved-name rules;
- map every other identifier to a hash-prefixed name in a namespace that safe logical IDs cannot occupy;
- use only that derived name for report directories, database copies, and ZIP filenames;
- confine all final outputs to the caller-selected root;
- require package-generated child directories such as `exports` and per-run directories to be real contained directories rather than symbolic-link aliases;
- publish final files atomically where supported and remove attempt-local partial files after failure.

## Alternatives considered

| Option | Pros | Cons | Outcome |
|---|---|---|---|
| Use raw run ID as path | Human-readable, no mapping | Traversal, separators, reserved names, Unicode/filesystem ambiguity | Rejected |
| Reject every unsafe stored run ID | Simple invariant | Existing/imported evidence becomes unexportable; logical identity conflated with storage | Rejected |
| Slugify only | Readable | Collisions and lossy identity mapping | Rejected |
| Deterministic disjoint hash namespace | Contained, collision-resistant, stable, preserves metadata identity | Unsafe names are less human-readable | Accepted |

## Consequences

### Positive

- Opaque IDs cannot escape the selected output root.
- Existing logical IDs remain traceable in portable artifacts.
- Repeated exports produce stable names.
- Safe and hashed namespaces are structurally disjoint.
- Failure cleanup is testable independently from logical identity.

### Negative / tradeoffs

- Unsafe identifiers produce non-human-readable filenames.
- Users must inspect `run.json` or `MANIFEST.json` for the original identifier.
- Any future public naming change requires compatibility and collision review.

## Validation

- traversal and separator-bearing run-ID regression tests;
- safe/reserved/dotted/Unicode name fixtures;
- deterministic-repeat and namespace-disjointness tests;
- manifest logical-ID preservation checks;
- rename/copy failure cleanup tests;
- package-generated export-root and per-run-directory symbolic-link rejection tests;
- source/distribution ZIP path-safety audit.

## Review trigger

Revisit only if a public artifact naming contract is introduced, the package begins exporting to a non-filesystem object store, or collision/security evidence invalidates the current mapping.
