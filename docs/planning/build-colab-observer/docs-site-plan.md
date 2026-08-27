---
status: proposed
type: docs-plan
change: build-colab-observer
tags:
  - fumadocs
  - documentation
  - site
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Fumadocs documentation site plan

## Role

`apps/docs` is the authoritative public learning and reference surface for `colab-observer`, but it is not the product runtime. Its content is grounded in tested public APIs, schemas, snippet fragments, diagnostic catalog, and release metadata.

## Stack decision

- Next.js App Router.
- Fumadocs content and UI.
- Tailwind CSS v4.
- Fumadocs `shadcn` theme preset plus selected shadcn/ui primitives.
- TypeScript and pnpm workspace.
- Local search by default; an external search service requires a separate decision and privacy review.
- Vercel as the proposed hosting target after approval.

Fumadocs currently documents Tailwind v4 support and a shadcn preset. Exact package versions are resolved during implementation and committed to the lockfile.

## Route/content graph

```text
/
/docs
  /quickstart
  /installation
  /concepts
    /lifecycle
    /capabilities-and-quality
    /privacy-and-local-first
  /guides
    /dashboard
    /diagnostics
    /exports
    /drive-output
    /phase-markers
  /metrics
    /system
    /gpu
    /frameworks
    /schema
  /diagnostics/<rule-id>
  /api
    /config
    /observer
    /models
    /exceptions
  /examples
    /cpu-only
    /pytorch
    /tensorflow
    /jax
    /degraded-modes
  /integrations
  /accessibility
  /security-and-colab-policy
  /troubleshooting
  /compatibility
  /contributing
  /roadmap
  /changelog
```

## Landing page

Primary narrative:

1. Observe your Colab runtime locally.
2. Understand bottlenecks through evidence.
3. Keep accessible reports after the session.

Primary actions: “Open quickstart,” “Open in Colab,” “View dashboard,” “Read safety boundary.” Repository/tooling/deployment links sit below product value.

## Content source-of-truth rules

| Content | Source |
|---|---|
| Quickstart cells | `notebooks/snippets/*.py` |
| Public API signatures | Python source/static extraction candidate such as Griffe |
| Metric names/units | versioned schema/registry |
| Diagnostic pages | diagnostic catalog data |
| CLI/config examples | tested examples |
| Compatibility | smoke-test evidence and support policy |
| Changelog | release metadata |
| `llms*` / AI index | docs content graph and public source metadata |

Generated pages include a “generated from” note in source metadata and fail CI when stale.

## Docs components

- Accessible code block with language, title, copy status, and source link.
- “Open in Colab” link with clear external-navigation label.
- Metric reference table with unit/source/quality and downloadable schema.
- Diagnostic evidence card with rule version, thresholds, caveats, and next checks.
- Capability matrix with explicit unavailable/degraded states.
- Chart/table demo using fixture data, not a hidden live backend.
- Callouts for safety, privacy, approximation, and version compatibility.
- Version badge showing docs/package relationship.

## Navigation and search

- Product journey order precedes repository contributor docs.
- Stable page titles and heading IDs.
- Search indexes visible content, API names, metric IDs, diagnostic IDs, and error codes.
- Search result context includes section and version.
- Keyboard shortcut and focus behavior are documented and tested.
- Static sitemap/content index remains available if search JavaScript fails.

## Accessibility

The docs share [[docs/planning/build-colab-observer/accessibility-ux]] requirements. Special attention:

- heading hierarchy and skip links;
- sidebar/mobile navigation focus and disclosure semantics;
- code block line wrapping/scrolling and copy feedback;
- tabbed content with correct tab pattern and non-JS fallback;
- Mermaid/diagram adjacent text and tables;
- search modal/dialog focus;
- contrast and forced colors;
- no content hidden behind animation, hover, or color.

## Build and validation

Proposed workspace commands, to verify after scaffold:

```bash
pnpm --filter docs lint
pnpm --filter docs typecheck
pnpm --filter docs test
pnpm --filter docs build
pnpm --filter docs test:a11y
pnpm --filter docs check:links
pnpm --filter docs check:metadata
pnpm --filter docs check:generated
```

CI uses `pnpm install --frozen-lockfile`. No production deploy occurs from a content build job.

## Preview and release

- Pull-request docs builds always run.
- Vercel preview is preferred for trusted branches/PRs under the configured integration policy.
- Forks must not receive production secrets.
- Production deploy follows protected branch/environment and required checks.
- Docs rollback targets the last known good Vercel deployment and source commit.
- Package docs remain version-conscious; do not show unreleased API as stable without a banner.
