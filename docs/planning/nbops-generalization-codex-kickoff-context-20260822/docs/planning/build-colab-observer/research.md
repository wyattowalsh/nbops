---
status: complete
type: research-brief
change: build-colab-observer
tags:
  - research
  - synthesis
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Research synthesis

## Bottom line

The best implementation is not a modernized clone of the original `colab_monitor`. It is a small local observability runtime whose live dashboard is a progressively enhanced view over a durable, versioned evidence model. The strongest existing OSS projects validate individual pieces, especially GPU/provider handling and terminal density, but not the combined Colab-native, accessible, report-first product.

## Key findings translated into the plan

| Finding | Implication |
|---|---|
| Colab resources and limits vary and sessions can end | Never promise persistence beyond the runtime; support mounted/local exports and no keepalive. |
| Custom widget behavior is an integration surface, not a platform invariant | Isolate transport and preserve static fallback. |
| NVML exposes useful device/process signals | Prefer official NVML binding, with strict `nvidia-smi` fallback. |
| `psutil` has warm-up and platform-specific semantics | Record provider/quality, ignore meaningless first percentage sample, test unavailable fields. |
| Operational charts can be inaccessible | Treat semantic table and textual interpretation as part of each visualization contract. |
| Fumadocs supports Tailwind v4 and shadcn theming | Use it for product/API docs, but keep docs subordinate to package work. |
| Google does not require `llms.txt` for AI-search visibility | Keep conventional SEO primary; publish AI-reader aids as maintained optional exports. |
| GitHub Actions and deployment supply chain are high-agency surfaces | Use immutable pins, least privilege, protected environments, and approval-gated release/deploy. |
| Existing Colab monitor repos are fragmented or infrastructure-heavy | Defend the local, copyable, accessible, evidence-bearing niche. |

## Evidence versus inference

### Evidence

- Official platform/library/standards behavior listed in [[docs/planning/build-colab-observer/source-registry]].
- Repository feature sets and current issue/release surfaces listed in [[docs/planning/build-colab-observer/github-ecosystem-audit]].
- Static skill parse and extraction results listed in [[docs/planning/build-colab-observer/source-skill-audit]].

### Inference

- A daemon thread is likely more robust than notebook asyncio for this product.
- SQLite is the best default durability/installation tradeoff.
- Preact + ECharts SVG is likely a good frontend size/capability balance.
- A custom widget plus static fallback is likely more robust than a server/port iframe.

Each inference has a spike, benchmark, or validation task before it becomes a release promise.

## Recheck triggers

- Colab runtime image or widget behavior changes.
- Fumadocs/shadcn/Tailwind/Next major version changes.
- NVML binding/package ownership or compatibility changes.
- OpenSpec command/profile changes.
- WCAG/WAI-ARIA normative updates.
- Vercel/GitHub Actions deployment or security changes.
- Package/repository naming immediately before publication.
