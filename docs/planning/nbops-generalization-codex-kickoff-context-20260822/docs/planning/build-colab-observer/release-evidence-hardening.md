---
status: active
type: implementation-evidence
change: build-colab-observer
tags:
  - implementation
  - contracts
  - browser
  - jupyter
  - colab
  - release-evidence
  - validation
updated: 2026-07-12
cssclasses:
  - planning-doc
---

# Representative-runtime and release-evidence hardening

**Path:** `docs/planning/build-colab-observer/release-evidence-hardening.md`  
**Purpose:** Record the latest material contract repairs, representative local evidence, managed-Colab evidence harness, and release blocker state.  
**Decision:** Local product slice is `final-with-known-risks`; the overall OpenSpec change remains `one-more-material-loop`.

## `/grill-me` outcome

The declared source directory contained only a continuation stub. The authoritative 304-file source ZIP was verified against SHA-256 and reconstructed into a separate workspace before mutation. No user question was necessary because the available evidence supported one safe default:

1. preserve the prior bundle;
2. repair only demonstrable contract and runtime defects;
3. deepen local Chromium, Jupyter, TypeScript/Node, package, and negative-test evidence;
4. make the managed-Colab blocker executable through a passive fail-closed evidence runner;
5. keep direct comm experimental and non-default;
6. stop before dependency resolution, installs, Git mutation, publication, deployment, secrets, accounts, permissions, or OpenSpec sync/archive.

## Material defects found and repaired

### Python models accepted values rejected by their public schemas

Several typed constructors and `Observation.from_dict()` coerced untrusted values such as numeric strings, booleans, numeric label values, non-string sources, and oversized identifiers. That could allow an in-memory object to exist even though its serialized representation violated the public JSON Schema.

The public model boundary now:

- requires exact scalar types instead of coercing them;
- bounds metric names to 256 characters, run IDs to 128, units to 128, and sources to 64;
- rejects control or format characters in identities;
- requires string label keys and values;
- requires finite numeric samples and durations;
- requires real `datetime` objects for directly constructed observation and dashboard timestamps;
- rejects malformed mappings before creating typed evidence.

The root and wheel-bundled observation/dashboard schemas were updated to match. Contract tests validate both accepted boundary values and rejected coercive values.

### Comm controls did not enforce exact run identity

The Python bridge previously accepted a `not-started` control alias even after an active snapshot existed. Controls now require exact equality with the current snapshot run ID. Snapshot and history factories must return validated kernel-to-UI snapshots for the same run.

### History-provider failures escaped the comm callback

A store or provider exception during a bounded history query could escape the callback. The bridge now emits a bounded, sanitized, recoverable `history_query_failed` error and continues serving later controls. Provider error details are not leaked.

### TypeScript runtime helpers relied too heavily on compile-time types

`createControlMessage()` now rejects unknown runtime actions, duplicate filters, oversized metrics, invalid ranges, non-history filters, hidden control characters, and invalid limits. `hasDashboardEnvelope()` rejects invalid run identities. A new TypeScript/Node smoke compiles the real source without installing tools and validates the resulting message against the public JSON Schema.

### Accessibility evidence lacked target-size and accessibility-tree checks

The static dashboard disclosure controls now provide a 44-pixel minimum height and explicit focus-visible treatment. The Chromium runner now inspects the browser accessibility tree, validates named regions/headings/groups/searchbox/combobox, measures interactive targets, exercises malformed label and stale-delta recovery, verifies temporary download-link cleanup, and retains zero-network enforcement.

## New evidence surfaces

### Managed-Colab smoke runner

`scripts/run_managed_colab_smoke.py` is a passive, reusable evidence harness for the actual blocker. It:

- fails closed outside managed Colab unless `--allow-non-colab` is explicit;
- installs nothing and performs no package resolution;
- never mounts Drive or calls account APIs;
- never activates experimental direct comm;
- starts no public endpoint and emits no remote telemetry;
- captures exact Python/platform/package/capability evidence;
- runs lifecycle, static display, persistence, reports, checksum, and bundle checks;
- labels evidence representative only when `google.colab` and `/content` are both detected.

The local harness mode passes all ten product checks with 800 observations, but remains explicitly non-representative. The default non-Colab invocation exits with a machine-readable blocked record.

### TypeScript/Node protocol runtime

`scripts/run_ui_protocol_runtime_smoke.py` compiles `packages/dashboard-ui/src/protocol.ts` into a temporary directory using already-present `tsc`, executes it with already-present Node, and validates the generated control message against the packaged JSON Schema. Nine of nine checks pass with no install or network access.

### Expanded local Chromium evidence

The browser suite now passes 21 of 21 checks, including:

- named accessibility-tree roles and names;
- 24-pixel-or-larger interactive targets, with product controls at 44 pixels high;
- keyboard focus/order and disclosure activation;
- light/dark contrast, forced colors, and reduced motion;
- 320-pixel page reflow without page-level overflow;
- malformed observation and label isolation;
- cross-run, wrong-version, and stale-delta isolation;
- later valid-message recovery;
- bounded controls and no invalid-filter control emission;
- CSV formula neutralization and transient-link cleanup;
- zero remote HTTP/HTTPS/WebSocket requests, dialogs, or page errors.

This is automated local Chromium evidence, not a WCAG conformance claim or managed-Colab browser evidence.

## Current validation summary

| Surface | Result | Boundary |
|---|---:|---|
| Repository gate | 133 tests pass | Python 3.13.5 only |
| Combined line-and-branch coverage | 89.1486%, gate 85% | Local source checkout |
| Python compatibility syntax | 102 files parse under Python 3.11 grammar | Not Python 3.11 execution |
| Local Chromium | 21/21 checks pass | Mocked comm, not managed Colab |
| TypeScript/Node protocol runtime | 9/9 checks pass | Local Node 22 / TypeScript 5.8.3 |
| Local Jupyter kernel | 10/10 checks; 950 observations; zero drops | Not managed Colab |
| Local lifecycle/export smoke | 2,198 observations; zero drops; 17 bundle entries; 16 checksums | Non-representative Linux runtime |
| Default 2-second benchmark | 415 observations; zero drops; 1.9334% one-core signal; 5,877,760-byte peak RSS delta | Local regression signal |
| Aggressive 200-ms benchmark | 1,627 observations; zero drops; 14.4174% one-core signal | Stress signal only |
| 30-second durability soak | 15,448 persisted; zero drops; history bounded at 2,000; both SQLite checks `ok` | Not a 30-minute Colab soak |
| PyTorch/JAX | Local CPU selected-workload smokes pass | Not managed Colab/device evidence |
| TensorFlow | Truthfully skipped | Package absent; no install attempted |
| Managed-Colab runner | Fail-closed blocker record + local harness pass | Representative run still pending |

## Transport decision

Direct comm remains `experimental`, `explicit`, `non-default`, and absent from the package root API. Local mocked-browser evidence is now stronger, but it still cannot establish managed-Colab iframe, comm-open, rerun, disconnect, network, or assistive-technology behavior.

The hosted custom-widget-manager route remains incompatible with the project’s no-runtime-CDN invariant. Promotion requires successful execution of the managed-Colab runner plus a separate direct-comm/browser matrix in actual Colab.

## Safety assertions

- No keepalive, anti-idle, hidden reconnect, timeout bypass, activity simulation, quota circumvention, public service, hosted backend, remote code, runtime CDN, automatic remediation, or default telemetry was added.
- No dependency installation or online package resolution occurred.
- No Git mutation, commit, push, PR, publication, deployment, secret/account/DNS/payment/permission action, or OpenSpec verify/sync/archive occurred.
- Unsupported, malformed, stale, degraded, and lost evidence remains explicit and non-fatal.
- Browser, Jupyter, TypeScript, and managed-Colab harnesses are validation tools, not runtime dependencies.

## Reassessment

The local work had positive marginal utility because it exposed public-contract drift, a cross-run control weakness, and an uncontained provider failure. Those defects are now covered by tests and cross-language evidence.

Another implementation loop is justified only when at least one material surface becomes available:

- managed Colab CPU, NVIDIA, TPU, Drive, or direct-comm execution;
- Python 3.11 or 3.12 execution;
- approved dependency resolution for reviewed `uv.lock` and `pnpm-lock.yaml`;
- representative browser and assistive-technology testing;
- owner, OSS license, repository, namespace, canonical URL, support, and release decisions.

Until then, preserve the bundle in final-assured maintenance rather than reopening cosmetic work.
