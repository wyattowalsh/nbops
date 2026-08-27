---
status: proposed
type: risk-register
change: generalize-notebook-runtime-observer
tags:
  - risk
  - security
  - migration
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Risk register

**Path:** `docs/planning/generalize-notebook-runtime-observer/risk-register.md`  
**Purpose:** Track product, architecture, migration, security, evidence, support, and naming risks with mitigations and triggers.  
**Status:** Proposed  

| ID | Risk | Likelihood | Impact | Mitigation | Evidence/owner | Review trigger |
|---|---|---:|---:|---|---|---|
| R-GEN-001 | “Jupyter support” overstates kernel-local scope | High | High | First-class measurement scope; support by stated scope | Specs + runtime matrix | Any public support copy |
| R-GEN-002 | Provider detection fingerprints users/workspaces | Medium | High | Allowlist, reduction, redaction, bounded evidence | Security tests | New detector/evidence field |
| R-GEN-003 | Adapter framework becomes premature public plugin API | Medium | High | Internal allowlisted registry only | Design owner | Third-party adapter request |
| R-GEN-004 | Colab extraction regresses current notebooks | Medium | High | Freeze compatibility fixtures first; additive rollout | TASK-103/122/142 | Any public API/default patch |
| R-GEN-005 | Deepnote object-backed storage causes poor SQLite behavior | High | High | `/tmp` working + explicit `/work` finalization profile | Deepnote runtime owner | Deepnote filesystem change |
| R-GEN-006 | Optional server extension expands attack surface | Medium | High | Separate extra, authn/authz, read-only bounds, no-go option | Security reviewer | Server-provider spike |
| R-GEN-007 | Frontend identity is guessed from kernel signals | High | Medium | Confidence/conflicts; unknown frontend allowed | Profile tests | New frontend detector |
| R-GEN-008 | Support tiers become stale marketing labels | Medium | High | Dated evidence, recheck triggers, generated claim checks | Release owner | Platform/runtime release |
| R-GEN-009 | Static/enhanced UI semantics drift | Medium | High | One semantic model; summary/table/CSV parity | Accessibility owner | Protocol/UI patch |
| R-GEN-010 | Schema migration breaks prior support bundles | Medium | High | Legacy golden fixtures and additive versions | Migration owner | Schema version bump |
| R-GEN-011 | `nbops` identity migration could obscure the Colab acquisition wedge | Medium | Medium/High | Evidence gate; keep Colab-first copy; explicit approval | Product owner | `nbops` publication-readiness gate completion |
| R-GEN-012 | Package splits multiply maintenance burden | Medium | Medium | One distribution; extras only for unique dependencies | Packaging owner | New platform dependency |
| R-GEN-013 | Generic CPU/RAM monitor lacks differentiation | Medium | High | Historical scope, diagnostics, accelerator/framework evidence, portable bundles | Product brief | Competitive review |
| R-GEN-014 | Cross-platform benchmarks produce false shared budget | Medium | Medium | Measure per environment; no borrowed thresholds | Performance owner | New support tier |
| R-GEN-015 | Future non-Python demand forces incompatible architecture | Low/Medium | Medium | Explicit unsupported status; separate future change | Product owner | Material user demand |

## Highest-priority gates

1. Colab compatibility regression prevention.
2. Scope truthfulness.
3. Detection privacy and failure isolation.
4. Legacy artifact migration.
5. Representative Jupyter/Deepnote/Colab evidence before support-tier and platform claims.
6. Optional server integration security/no-go decision.
