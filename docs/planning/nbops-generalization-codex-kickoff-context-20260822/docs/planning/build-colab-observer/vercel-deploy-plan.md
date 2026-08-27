---
status: proposed
type: deployment-plan
change: build-colab-observer
tags:
  - vercel
  - docs
  - deployment
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Vercel documentation deployment plan

## Recommendation

Use Vercel’s GitHub integration as the default docs delivery path. It naturally provides commit/PR previews and production deployment without maintaining a second custom deployment implementation. Use GitHub Actions only for pre-deploy validation or if a protected orchestration requirement cannot be expressed through Vercel deployment checks.

No Vercel project, account, domain, secret, or deployment is created during planning.

## Environments

| Environment | Source | Indexing | Data/secrets | Purpose |
|---|---|---|---|---|
| Local | developer | none | no production secrets | implementation/validation |
| Preview | trusted PR/branch according to policy | `noindex` | public docs config only | review UI/content |
| Production | protected main/release commit | indexable | minimal public runtime config | canonical docs |

The docs app should require no secret for normal public rendering/search. Provider-generated identifiers are configuration, not embedded credentials. Optional analytics/search services require a separate review.

## Proposed setup sequence, approval-gated

1. Confirm GitHub owner/repository and Vercel account/team.
2. Create/import one Vercel project rooted at `apps/docs`.
3. Detect/confirm pnpm and build/output settings from repository scripts.
4. Configure production branch and preview trust policy.
5. Add only required environment variable **names** to `.env.example`; set values in provider UI, never in source/chat.
6. Configure deployment checks to require docs build/accessibility/metadata jobs.
7. Set preview robots/noindex behavior and production canonical base URL.
8. Deploy preview, run smoke/accessibility/SEO checks.
9. Approve production deployment and optional custom domain separately.
10. Record rollback and ownership in runbook.

## Proposed variables

Likely none are required for the base site. If needed:

```text
NEXT_PUBLIC_SITE_URL
NEXT_PUBLIC_GITHUB_REPOSITORY
NEXT_PUBLIC_PACKAGE_NAME
```

These names are examples until the implementation confirms necessity. Do not place tokens in `NEXT_PUBLIC_*` variables.

Vercel and PyPI credentials are not required in application environment variables when using provider Git integration and trusted publishing respectively.

## Deployment checks

- Fumadocs/Next production build.
- route and asset smoke.
- internal links and canonical URLs.
- sitemap/robots behavior for environment.
- JSON-LD parse/XSS fixtures.
- `llms.txt`, `llms-full.txt`, `ai-index.json` validity.
- keyboard/automated accessibility on key routes.
- package/docs version compatibility.
- no preview URL embedded as production canonical.

## Headers and security

Plan and test:

- content-type and caching appropriate to immutable/static assets versus docs pages;
- frame policy compatible with intended docs embedding, not unnecessarily permissive;
- content security policy compatible with Fumadocs/shadcn and no unapproved runtime CDN;
- `X-Content-Type-Options`, referrer policy, and reasonable permissions policy;
- no sensitive source maps or environment values in client bundles.

Do not cargo-cult a CSP before observing the built app; generate a minimal policy and test it.

## Rollback

1. Identify last known good deployment and source commit.
2. Promote/rollback in Vercel after approval.
3. Verify canonical, sitemap, quickstart, API, and download links.
4. Open a source repair rather than treating provider rollback as the final fix.
5. Record incident and docs/package compatibility impact.

## Stop conditions

Stop for explicit approval before Vercel sign-in, team/project creation, GitHub app authorization, environment variable changes, custom domain/DNS, deployment, protection changes, or billing-impacting settings.
