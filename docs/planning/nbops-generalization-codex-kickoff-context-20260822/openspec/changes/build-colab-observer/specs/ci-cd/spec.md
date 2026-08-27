---
status: proposed
type: openspec-delta-spec
change: build-colab-observer
tags:
  - openspec
  - requirements
  - ci-cd
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Delta spec: CI/CD

## ADDED Requirements

### Requirement: Least-privilege pull-request CI
Pull-request workflows MUST run with minimal permissions, avoid production secrets for untrusted contributions, cancel superseded runs, and produce reviewable results for Python, UI, docs, notebooks, security, and OpenSpec checks.

#### Scenario: Untrusted fork
- GIVEN a pull request from a fork
- WHEN CI executes
- THEN tests and builds use no production publishing or deployment credential
- AND workflow permissions are read-only unless a specific job requires a narrower documented permission

### Requirement: Supported-runtime matrix
CI MUST exercise the supported Python range and MUST distinguish hardware-independent tests from explicitly gated NVIDIA or Colab smoke validation.

#### Scenario: No GPU runner
- GIVEN standard CI has no NVIDIA device
- WHEN the test suite runs
- THEN fake-provider and fallback parsing tests cover GPU behavior
- AND hardware smoke tests are reported as gated rather than falsely passing

### Requirement: Package and frontend artifact verification
CI MUST build the Python distribution and private dashboard assets from locks, inspect wheel and source-distribution contents, install the wheel in a clean environment, and run a public-API smoke test.

#### Scenario: Runtime CDN dependency
- GIVEN a built dashboard references an unapproved remote runtime asset
- WHEN artifact policy validation runs
- THEN the release job fails

### Requirement: Documentation validation and previews
CI MUST build and validate the docs site, links, metadata, structured data, search/index artifacts, accessibility checks, and preview eligibility before production deployment.

#### Scenario: Broken notebook snippet in docs
- GIVEN the documented snippet no longer matches the tested source snippet
- WHEN docs CI runs
- THEN the drift check fails and identifies the source of truth

### Requirement: Approval-gated releases
Package publication and production documentation deployment MUST be isolated from pull-request CI, use protected triggers/environments, and require explicit human-approved setup before first use.

#### Scenario: Tag without approval
- GIVEN a release tag exists but required protected-environment approval or provenance checks are incomplete
- WHEN the release workflow reaches publication
- THEN publication does not occur
- AND the job reports the unmet gate

### Requirement: Pinned and auditable automation
Third-party workflow actions and release tooling MUST be pinned to immutable references or otherwise governed by a documented update and review process.

#### Scenario: Action update
- GIVEN a pinned workflow action needs an update
- WHEN the update is proposed
- THEN provenance, release notes, permission impact, and validation are reviewed before the pin changes
