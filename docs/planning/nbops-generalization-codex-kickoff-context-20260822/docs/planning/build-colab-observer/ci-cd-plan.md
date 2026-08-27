---
status: proposed
type: ci-cd-plan
change: build-colab-observer
tags:
  - github-actions
  - ci
  - release
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# CI/CD plan

## Workflow topology

```text
.github/workflows/
├── ci-python.yml
├── ci-web.yml
├── ci-notebooks.yml
├── ci-policy.yml
├── docs-preview.yml
├── release-candidate.yml
├── publish-pypi.yml
└── vercel-production.yml   # only if Git integration alone is insufficient
```

Prefer Vercel Git integration for docs previews/production rather than duplicating deployment in GitHub Actions. Keep a workflow-based path only when required for protected checks or explicit orchestration.

## Global hardening

- Top-level `permissions: contents: read` and job-specific additions only.
- Pin third-party actions to full commit SHAs; document update source/version in comments or dependency automation.
- Concurrency groups cancel superseded PR runs.
- No `pull_request_target` execution of untrusted checkout code.
- Fork PRs receive no publishing/deployment secrets.
- Use environment protection for release and production docs.
- Retain artifacts for a bounded period and exclude secrets/run dumps.
- Shell scripts use strict modes; interpolate untrusted data through environment variables rather than command construction.
- Dependency caches key on lockfiles and never become a source of truth.

## Pull-request jobs

### Python CI

- matrix over the verified supported Python range;
- `uv sync --frozen`/lock-equivalent;
- Ruff format/check;
- ty;
- unit/contract/integration tests with fake providers;
- coverage artifact and threshold policy;
- package build, metadata check, wheel/sdist content audit;
- install wheel in a clean environment and public API smoke;
- CPU-only degraded-capability end-to-end test.

### Web/docs CI

- pnpm frozen install;
- format/lint/type/unit tests;
- build private dashboard assets;
- generated asset drift and wheel inclusion input check;
- Fumadocs build;
- internal links, metadata, sitemap/robots, JSON-LD, AI index, snippet/API/diagnostic drift;
- component and docs accessibility tests;
- browser tests against fixture states.

### Notebook/policy CI

- JSON/metadata/output/size validation;
- canonical snippet sync;
- secret and prohibited-behavior scans;
- source-level smoke execution outside Colab;
- policy-negative fixtures;
- optional scheduled/manual current Colab CPU/GPU matrix, not falsely represented by standard runners.

### OpenSpec/planning CI

- delta syntax and strict validation where the pinned tool supports it;
- requirement/task/traceability checks;
- schema validation for task graph and manifests;
- docs-vault path/link validation when planning artifacts are retained in the repo.

## Release candidate workflow

Trigger: protected manual dispatch or signed/versioned tag policy after all required checks.

1. Checkout immutable commit.
2. Build dashboard assets from lock.
3. Build wheel/sdist once.
4. Inspect, install, and run smoke/contract tests on the built artifacts.
5. Generate checksums and SBOM/provenance evidence where supported.
6. Build release-aligned docs and notebooks.
7. Upload immutable candidate artifacts for review.
8. Do not publish.

## PyPI publication proposal

After explicit repository/account approval, use PyPI Trusted Publishing through OIDC rather than a long-lived API token. A pending publisher does not reserve the project name until first publication, so name availability is rechecked at release. The publish job:

- depends on reviewed candidate artifacts rather than rebuilding;
- uses a protected GitHub environment;
- grants `id-token: write` only to the publication job;
- verifies artifact checksums/provenance;
- publishes one version once;
- records the release URL and immutable hashes;
- cannot run from pull requests.

GitHub artifact attestations may be added for public-repository builds after reviewing permission and plan availability.

## Documentation delivery

- Every PR builds docs.
- Vercel preview eligibility follows trust policy and deployment checks.
- Production docs deploy from protected main/release state only after package/docs compatibility and accessibility checks.
- Production deployment is not coupled to package publication in a way that leaves mismatched docs without rollback.
- A prior deployment can be promoted/rolled back through the provider after human approval.

## Scheduled maintenance

Optional scheduled, read-only checks:

- dependency/security update visibility;
- external link health;
- current Colab compatibility smoke;
- generated docs drift;
- package-name/security advisory monitoring.

Scheduled jobs do not auto-publish or mutate protected branches.

## Branch/check protection proposal

Require at minimum:

- Python CI;
- UI/docs CI;
- notebook/policy CI;
- OpenSpec/traceability check while the change is active;
- code-owner review for workflows, security policy, collectors, UI accessibility, and release files;
- resolved review conversations and current branch.

Actual repository rules require explicit approval and repository administration access.
