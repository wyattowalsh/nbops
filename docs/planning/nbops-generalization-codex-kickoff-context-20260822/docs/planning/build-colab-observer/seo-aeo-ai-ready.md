---
status: proposed
type: discovery-plan
change: build-colab-observer
tags:
  - seo
  - aeo
  - ai-ready
  - docs
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# SEO, AEO, and AI-ready documentation

## Position

Treat SEO as the primary discipline: crawlable useful pages, precise titles/descriptions, canonical URLs, internal links, structured headings, performance, and trustworthy content. “AEO” and “GEO” are useful audience lenses, but Google’s current guidance treats optimization for its AI features as SEO and does not require `llms.txt`.

Publish `llms.txt`, `llms-full.txt`, and `ai-index.json` as optional, maintained machine-reader aids. They are not access control, not a ranking guarantee, and not a substitute for `robots.txt`, sitemap, or visible documentation.

## Conventional technical SEO

| Surface | Plan |
|---|---|
| Metadata | Unique title/description, canonical, package/version where useful |
| Sitemap | Generated from public content graph; excludes previews/private routes |
| Robots | Explicit production policy; previews discourage indexing |
| Social previews | Branded, legible OG/Twitter images with page title/category |
| Breadcrumbs | Visible breadcrumbs plus matching `BreadcrumbList` data |
| Structured data | `SoftwareApplication`/`SoftwareSourceCode` on product/repo surfaces, `TechArticle` for docs where appropriate |
| Internal links | Quickstart → concepts → reference → troubleshooting, with no orphan pages |
| Performance | Static/server rendering, bounded client bundles, optimized assets |
| Errors/redirects | Stable slugs, redirect map, useful 404, no soft-404 docs pages |

Structured data must match visible content and serialize untrusted text safely. Do not add unsupported ratings, claims, or FAQ markup solely for rich-result speculation.

## Answer-oriented content

- Start major pages with a concise “what/when/why” summary.
- Use task headings that match real questions: “Why is my GPU idle?”
- Provide direct answer, evidence, limitations, and next checks.
- Include precise code, expected output, and failure variants.
- Link metric and diagnostic identifiers to stable definitions.
- State supported versions and last-verified date for volatile behavior.
- Distinguish observation from inference in troubleshooting.
- Avoid keyword-stuffed duplicate pages.

## AI-readable artifacts

### `/llms.txt`

A concise index:

```text
# colab-observer
> Local-first, accessible runtime observability for Google Colab.

## Start
- [Quickstart](/docs/quickstart): install, start, display, export
- [Safety boundary](/docs/project/security): local-first and no keepalive

## Reference
- [API](/docs/reference/api)
- [Metrics schema](/docs/concepts/metrics)
- [Diagnostics](/docs/concepts/diagnostics)
```

### `/llms-full.txt`

A bounded concatenation or generated representation of public core docs with page titles, canonical URLs, version, and stable section delimiters. Exclude previews, private content, giant generated tables, and duplicated navigation chrome.

### `/ai-index.json`

Proposed schema:

```json
{
  "schema_version": "1",
  "project": "colab-observer",
  "package_version": "<release>",
  "generated_at": "<timestamp>",
  "entries": [
    {
      "id": "quickstart",
      "title": "Quickstart",
      "url": "<canonical>",
      "markdown_url": "<canonical markdown>",
      "summary": "...",
      "topics": ["installation", "colab", "export"],
      "source_paths": ["notebooks/snippets/start.py"],
      "updated_at": "<date>"
    }
  ]
}
```

The index contains no hidden ranking text or private repository paths.

## Markdown/source access

- Offer stable raw Markdown representations where supported.
- Preserve code fences, tables, headings, links, and callout meaning.
- Include canonical URL, package version, and source provenance metadata.
- Do not require custom headers or JavaScript to obtain core text.
- Avoid publishing internal planning notes or security-sensitive details as part of AI exports.

## Validation

- Metadata/canonical uniqueness and presence.
- Sitemap/robots parse and environment behavior.
- JSON-LD parse plus malicious-string XSS fixtures.
- Broken/orphan link checks.
- `llms.txt` link validation.
- `llms-full.txt` size, duplication, public-page coverage, and freshness.
- `ai-index.json` schema, canonical URLs, source mappings, and generated drift.
- Preview `noindex`/canonical behavior.
- Accessibility and performance checks.

## Measurement without surveillance

The initial docs plan does not require analytics. If analytics are later proposed, evaluate privacy, cookie/consent, data retention, and whether aggregate server/deployment metrics suffice. Product monitoring remains independent of docs analytics.
