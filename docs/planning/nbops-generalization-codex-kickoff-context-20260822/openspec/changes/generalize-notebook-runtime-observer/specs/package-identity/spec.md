---
status: proposed
type: openspec-delta-spec
change: generalize-notebook-runtime-observer
tags:
  - openspec
  - spec
  - package-identity
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Delta spec: package-identity

**Path:** `openspec/changes/generalize-notebook-runtime-observer/specs/package-identity/spec.md`  
**Purpose:** Observable identity, migration, and publication-boundary behavior for `nbops`.  
**Status:** Proposed

## ADDED Requirements

### Requirement: Canonical `nbops` identity
**Trace ID:** `REQ-IDN-001`  
The system MUST use the exact lowercase identity `nbops` for the canonical product, repository, Python distribution, Python import package, command-line entry point, source-package target, and new user-facing artifact metadata.

#### Scenario: Canonical surfaces agree
- **WHEN** a user installs, imports, invokes, documents, or exports the product
- **THEN** the canonical identity is `nbops`
- **AND** Google Colab, Jupyter, Deepnote, or another provider appears only as a platform or adapter label

#### Scenario: Competing canonical identity is rejected
- **WHEN** release validation scans current metadata, imports, snippets, examples, docs, and generated artifacts
- **THEN** a competing product, package, import, CLI, repository, or new-artifact identity causes validation to fail
- **UNLESS** it is an explicitly allowlisted historical identifier or migration fixture

### Requirement: Behavior-preserving identity migration
**Trace ID:** `REQ-IDN-002`  
The system MUST preserve observable lifecycle, collection, diagnostics, persistence, display, reporting, and portable-artifact readability while moving the canonical implementation to `nbops`.

#### Scenario: Behavior is frozen before migration
- **WHEN** the identity migration begins
- **THEN** executable fixtures already capture the supported observer behavior independently of the prior source or import path

#### Scenario: Legacy artifacts remain readable
- **WHEN** `nbops` opens a supported artifact produced before the identity migration
- **THEN** the artifact remains readable
- **AND** its historical metadata is not rewritten as new execution evidence

### Requirement: Compatibility shims require evidence
**Trace ID:** `REQ-IDN-003`  
The system MUST NOT add or retain a prior import-package shim unless repository, release, or verified user evidence identifies an actual compatibility requirement.

#### Scenario: No demonstrated external dependency
- **WHEN** no external dependency on the prior import path is verified
- **THEN** the current implementation exposes only the canonical `nbops` package

#### Scenario: Demonstrated compatibility requirement
- **WHEN** verified external usage requires a temporary shim
- **THEN** the shim delegates to `nbops`
- **AND** its scope, warning behavior, removal criterion, and tests are documented

### Requirement: Publication identity is separately gated
**Trace ID:** `REQ-IDN-004`  
The system MUST treat package, repository, domain, social-handle, and trademark readiness as publication evidence rather than implementation assumptions.

#### Scenario: Preliminary namespace signal is insufficient
- **WHEN** an exact package or repository page appears unclaimed
- **THEN** the result is recorded only as a preliminary signal
- **AND** ownership or publication readiness is not claimed

#### Scenario: External identity action remains approval-gated
- **WHEN** publication-readiness checks pass
- **THEN** registry reservation, remote repository creation or rename, domain changes, publication, and announcements still require separate explicit approval
