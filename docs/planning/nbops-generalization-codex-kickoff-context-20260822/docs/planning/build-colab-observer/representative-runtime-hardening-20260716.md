---
status: active
type: implementation-evidence
change: build-colab-observer
tags:
  - evidence
  - contracts
  - exports
  - security
  - validation
updated: 2026-07-16
cssclasses:
  - planning-doc
---

# Representative-runtime hardening — 2026-07-16

**Path:** `docs/planning/build-colab-observer/representative-runtime-hardening-20260716.md`  
**Purpose:** Record the evidence-gated product repairs and validation completed after reconstructing the 2026-07-13 authoritative source bundle.  
**Status:** Local product slice final-with-known-risks; representative managed-Colab and release gates remain open.

## `/grill-me` result

The declared workspace contained only continuation state, while the authoritative source ZIP and SHA-256 sidecar were intact. The source ZIP hash matched `476fef289d6979dfb61b5e21ac78b18b325858b785c7a029d8fda617ba62cbfe`, so the complete workspace was reconstructed at `/mnt/data/colab-observer-representative-runtime-20260716` before any mutation.

No material user question was required. The evidence-determined default was to preserve the prior artifact, work in a separate reconstructed directory, avoid dependency installation/network resolution, and use the already available Python 3.13, Node/TypeScript, Chromium, Playwright, Jupyter, pytest, coverage, and JSON Schema surfaces.

The runtime/tool inventory still lacks Python 3.11/3.12, Ruff, ty, executable pre-commit, pnpm, managed Colab, representative accelerators, and assistive-technology environments. The highest-value safe work was therefore a public-model, schema, export-containment, atomic-publication, and failure-cleanup audit.

## Material defects found and repaired

| Defect | Prior behavior | Risk | Repair |
|---|---|---|---|
| Ambiguous disk-path configuration | A string path could be treated as a sequence of characters | Invalid filesystem probes and surprising configuration | `disk_paths` now requires an actual sequence of path-like entries and reports bounded configuration errors |
| Label coercion and collisions | Mixed label types could raise incidental `TypeError` or normalize into colliding keys | Untrusted evidence could fail inconsistently or lose label identity | Label maps now require string keys/values, reject invalid mappings and post-normalization collisions, and fail at the public boundary |
| Public dataclass drift | Several exported models accepted invalid scalars and failed later during serialization | Invalid evidence could enter stores/UI before surfacing | Capability, event, diagnostic, process, run, and status models now validate immediately and normalize accepted timestamps/JSON data |
| Observation decoder permissiveness | Missing/unknown fields and coercive scalar shapes were accepted inconsistently | Python and bundled schemas could disagree | `Observation.from_dict()` now requires the exact public field set and strict scalar/bounds/label behavior |
| Unavailable observations carrying values | `quality="unavailable"` could coexist with a numeric/text value | Missing evidence could be misread as real data | Unavailable observations now retain provenance/unit metadata but contain neither numeric nor text values; both schema copies match |
| External schema identity | Public schemas used an external web-domain identifier not owned by the project | Offline identity and domain-ownership ambiguity | Public schemas now use stable non-network URNs and remain bundled with the wheel |
| Opaque run IDs used as paths | A run ID such as `../escape` was joined directly into export directories/ZIP names | Directory traversal outside the selected output root | Logical run IDs remain unchanged in metadata while filesystem artifacts use a deterministic safe single-segment name in a disjoint namespace |
| Partial export cleanup | Rename/copy failures could leave temporary or partial artifacts | Failed exports could leave ambiguous files or overwrite evidence | Atomic publication paths now remove temporary/partial files in `finally` paths and preserve existing valid destinations where safe |

## Observable behavior after repair

- Public configuration and evidence models reject invalid types, non-finite numbers, naive timestamps, unknown fields, malformed labels, and control/format characters with bounded errors.
- Missing telemetry remains semantically distinct from zero or text values.
- Root schemas, wheel-bundled schemas, Python decoders, and the TypeScript protocol agree for the tested public boundaries.
- Schema identity is stable and offline. Compatibility is determined from bundled schemas and declared versions, not a network fetch.
- A persisted run ID is opaque data. It cannot escape the selected export root or become an unintended nested path.
- Safe run IDs retain human-readable artifact names; unsafe IDs map deterministically to a hash-prefixed filesystem name that cannot collide with the safe namespace.
- Export publication failures do not claim success and clean up attempt-local partial files where safe.
- Existing CPU-only lifecycle, persistence, diagnostics, static dashboard, reports, and experimental direct-comm behavior remain unchanged outside the hardened boundaries.

## OpenSpec alignment

The material repairs update observable requirements in:

- `metrics-collectors`: unavailable evidence has no numeric/text value and is never converted to zero.
- `export-reporting`: opaque identifiers cannot become paths; publication is atomic where supported; schema identity is offline.
- `security-policy`: all generated files remain contained under the selected output location.

Implementation choices such as the artifact-name helper, hash namespace, cleanup order, and URN strings remain in `design.md`, source, tests, and this evidence record rather than in behavior-level specs.

## Validation evidence

| Check | Result |
|---|---:|
| Final repository suite | 208 passed |
| Combined line-and-branch coverage | 87.1906%, gate 85% |
| Covered statements / branches | 3,498 / 3,888; 940 / 1,202 |
| TypeScript/Node protocol runtime | 9/9 pass |
| TypeScript no-emit compile | Pass |
| Local Chromium | 21/21 pass; zero remote requests, page errors, or dialogs |
| Local Jupyter kernel | 10/10 pass; 950 observations; zero drops |
| Managed-Colab harness outside Colab | Fail-closed as designed |
| Explicit non-representative local Colab harness | 10/10 pass; 368 observations; zero drops |
| Local lifecycle/export smoke | 2,198 observations; zero drops; 17 entries; 16 verified checksums |
| Default two-second benchmark | 415 observations; zero drops; 2.2388% one-core signal; 5,275,648-byte peak RSS delta |
| Stress 200-millisecond benchmark | 1,627 observations; zero drops; 14.8125% one-core signal; 3,338,240-byte peak RSS delta |
| Thirty-second local soak | 15,448 persisted; zero drops; bounded 2,000-row history; SQLite source/backup `ok` |
| PyTorch selected-workload smoke | Pass, version `2.10.0+cpu`, 826 observations |
| JAX selected-workload smoke | Pass, version `0.9.0.1`, 825 observations |
| TensorFlow selected-workload smoke | Truthfully skipped because absent; no install attempted |

Evidence root:

```text
/mnt/data/colab-observer-representative-runtime-validation-20260716
```

These are local Linux/Python 3.13.5 regression signals. They are not managed-Colab, accelerator, Python 3.11/3.12, or WCAG conformance claims.

## Task-state impact

The original OpenSpec task counts remain:

```text
17 complete
24 partial with validated subsets
4 blocked or deferred
```

The repairs strengthen `TASK-002`, `TASK-010`, `TASK-032`, `TASK-034`, and `TASK-071`, but do not satisfy their remaining release-level acceptance gaps such as reviewed locks/toolchain, optional DuckDB evidence, managed Colab, manual accessibility, and public release identity.

## Remaining evidence gates

- Managed Google Colab CPU, NVIDIA, TPU/XLA, mounted Drive, iframe, and direct comm.
- Python 3.11 and Python 3.12 execution.
- Reviewed `uv.lock` and `pnpm-lock.yaml`, dependency licenses/advisories, Ruff, ty, executable pre-commit, and frozen docs build.
- Manual keyboard, screen-reader, zoom, multiple-browser, managed-notebook, and live-region review.
- Owner, OSS license, repository, package namespace, canonical URLs, support policy, release channels, publication, and deployment.

## Reassessment

This loop had high positive marginal utility because it found a concrete directory-traversal vulnerability, contract contradictions, unsafe public-model coercions, and partial-artifact cleanup gaps. Those defects are repaired and regression-tested. Further local feature expansion now has lower expected value than the blocked representative surfaces. Preserve this slice in final-assured maintenance unless a material defect, failed validation, stale authoritative fact, unsafe drift, explicit request, or newly available runtime/tool/ownership surface appears.
