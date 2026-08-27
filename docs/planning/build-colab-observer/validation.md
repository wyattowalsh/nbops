---
status: active
type: validation
change: build-colab-observer
tags:
  - validation
  - tests
  - runtime
  - security
  - final-assurance
updated: 2026-07-25
cssclasses:
  - planning-doc
---
# Validation: runtime-evidence hardening

## Decision boundary

The local product slice is `final-with-known-risks`. The overall change remains `one-more-material-loop`. Local Linux, Jupyter, Chromium, provider-fixture, and package evidence prove only the recorded surfaces. They do not establish managed Google Colab, accelerator, Python 3.11/3.12, reviewed dependency-security, publication, deployment, or WCAG conformance.

Working evidence root:

```text
/mnt/data/colab-observer-next-evidence-20260725
```

Final delivery paths and SHA-256 values are recorded in the external validation summary, artifact audit, delivery manifest, and final response so the source bundle does not contain a self-referential archive hash.

## Exact commands and results

### Hermetic repository gate

```bash
PYTHONDONTWRITEBYTECODE=1 make check
```

Result: **249 tests passed; exit 0**. The gate also passed repository hygiene, high-confidence secret scanning, prohibited-behavior scanning, four public schemas and fixtures, Python/JSON-Schema/TypeScript protocol parity, notebook synchronization, eleven OpenSpec domains, eleven nested `AGENTS.md`, least-privilege workflow source checks, eighteen pre-commit source hooks, Fumadocs source contracts, forty-seven module imports, Python 3.11 grammar parsing across 104 files, and Python compilation.

### Branch-aware coverage

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=src \
PYTHONDONTWRITEBYTECODE=1 \
python -W error::ResourceWarning -m pytest \
  -p pytest_cov.plugin -p no:cacheprovider \
  --cov=colab_observer --cov-branch \
  --cov-report=term-missing \
  --cov-report=json:<evidence>/coverage.json \
  --cov-fail-under=85
```

| Metric | Result |
|---|---:|
| Tests | 249 passed |
| Combined line-and-branch total | 87.4176% |
| Required gate | 85% |
| Statements | 4,162 |
| Covered statements/lines | 3,750 |
| Branches | 1,298 |
| Covered branches | 1,023 |
| Partial branches | 241 |
| `ResourceWarning` | Promoted to failure |

### Targeted runtime-boundary regressions

The full suite includes explicit failures and repairs for:

- terminal/fatal phase-marker and user-note rejection;
- immediate fatal sampler `failed`/non-running status;
- stale active-observer cleanup;
- finite non-negative flush deadlines;
- writer close failure containment;
- strict CPU/memory/disk/network/process/Drive/framework provider fields;
- per-core CPU and NVML device cardinality caps;
- export elapsed-range datetime/SQLite domain overflow.

Evidence: `runtime-evidence-hardening-20260725.md` and the corresponding integration/unit tests.

### TypeScript and Node protocol

```bash
python scripts/run_ui_protocol_runtime_smoke.py --output <evidence>/ui-protocol-runtime
tsc -p packages/dashboard-ui/tsconfig.json --noEmit
```

Result: **9/9** runtime checks and TypeScript no-emit pass, with no dependency installation or network access.

### Chromium

```bash
PYTHONPATH=src python scripts/run_browser_smoke.py --output <evidence>/browser-smoke
```

Result: **21/21** checks pass, with zero remote requests, page errors, or dialogs. The checks include semantic names/roles, keyboard order, visible focus, 44-pixel tested disclosure controls, narrow reflow, light/dark contrast, forced colors, reduced motion, table parity, malformed/stale/cross-run recovery, CSV-formula neutralization, and temporary-download cleanup. This is local automated evidence, not a WCAG conformance claim.

### Local Jupyter kernel

```bash
PYTHONPATH=src python scripts/run_jupyter_smoke.py --output <evidence>/jupyter-smoke
```

| Metric | Result |
|---|---:|
| Checks | 10/10 |
| Observations | 491 |
| Dropped batches | 0 |
| Semantic script-free dashboard | Pass |
| Remote scripts or URLs | None |
| HTML/Markdown/bundle exports | Pass |
| Lingering observer threads | 0 |
| Representative managed Colab | No |

### Local lifecycle/export smoke

```bash
PYTHONPATH=src python scripts/run_local_smoke.py \
  --output <evidence>/local-smoke --duration 2.0
```

| Metric | Result |
|---|---:|
| Observations | 1,127 |
| Dropped batches | 0 |
| Queue depth at end | 0 |
| Final status | `stopped` |
| Remote telemetry | None |
| Public service | None |

### Local performance regression signals

```bash
PYTHONPATH=src python scripts/benchmark_smoke.py \
  --duration 6.0 --interval 2.0 --output <evidence>/benchmark-default.json
PYTHONPATH=src python scripts/benchmark_smoke.py \
  --duration 3.0 --interval 0.2 --output <evidence>/benchmark-stress.json
```

| Profile | Observations | Drops | Incremental CPU | Peak RSS delta | Maximum lag |
|---|---:|---:|---:|---:|---:|
| 2.0-second default | 211 | 0 | 0.6687% of one core | 823,296 bytes | 0.022382 s |
| 0.2-second stress | 811 | 0 | 3.5489% of one core | 1,441,792 bytes | 0.021867 s |

These are local regression signals, not managed-Colab budgets. Host variance means raw counts are not compared to prior runs as release thresholds.

### Isolated thirty-second durability soak

```bash
PYTHONPATH=src python scripts/run_local_soak.py \
  --output <evidence>/local-soak-30s \
  --duration 30.0 --interval 0.2
```

| Metric | Result |
|---|---:|
| Actual duration | 30.056144 s |
| Persisted observations | 7,747 |
| Dropped batches | 0 |
| In-memory history | Bounded at 2,000 |
| Reader failures | 0 |
| Lingering threads | 0 |
| Peak RSS delta | 6,860,800 bytes |
| CPU signal | 11.6449% of one core |
| Lag mean / p95 / maximum | 0.005897 / 0.006409 / 0.009047 s |
| Source SQLite check | `ok` |
| Backup SQLite check | `ok` |

A combined evidence wrapper exceeded its outer execution budget before this isolated run. The isolated command passed; both facts are retained rather than converting the wrapper timeout into an unsupported product conclusion.

### Frameworks

```bash
PYTHONPATH=src python scripts/run_framework_smoke.py --framework torch --output <evidence>/framework-smoke/torch.json
PYTHONPATH=src python scripts/run_framework_smoke.py --framework jax --output <evidence>/framework-smoke/jax.json
PYTHONPATH=src python scripts/run_framework_smoke.py --framework tensorflow --output <evidence>/framework-smoke/tensorflow.json
```

| Framework | Result | Boundary |
|---|---|---|
| PyTorch | Passed, 418 observations | Local CPU, `2.10.0+cpu`, explicitly selected by workload |
| JAX | Passed, 417 observations | Local CPU, `0.9.0.1`, explicitly selected by workload |
| TensorFlow | Truthfully skipped | Package absent; no installation attempted |

### Managed-Colab harness

```bash
PYTHONPATH=src python scripts/run_managed_colab_smoke.py --output <evidence>/managed-colab-default
PYTHONPATH=src python scripts/run_managed_colab_smoke.py --output <evidence>/managed-colab-local --allow-non-colab
```

Default invocation outside managed Colab fails closed with `status=blocked`. Explicit local mode passes the bounded lifecycle/export checks with 215 observations and zero drops, but is labeled `representative_colab_evidence=false`. It installs nothing, mounts nothing, activates no direct comm, starts no public service, and uses no remote telemetry.

### OpenSpec, planning, package, and archive gates

The settled source is validated and packaged only after all source-ledger changes stop:

```bash
python /mnt/data/script_planpack.py validate-pack \
  --root <final-source-root> --change build-colab-observer
python scripts/check_distribution.py <distribution-directory>
```

Result at release freeze: fixed-epoch no-index wheel and normalized-sdist builds reproduce byte-for-byte across two clean source copies; distribution inspection and extracted-wheel smoke pass; the source, validation, and distribution ZIPs pass deterministic packaging, CRC, path/symlink, checksum, manifest/evidence-manifest, clean-extraction, and byte-comparison checks. Exact hashes and counts are recorded externally in the artifact audit and delivery manifest to avoid self-reference.

The supplied Planning Studio `schema_planning_manifest.schema.json` is a flat 40-file Project-config contract and is not semantically applicable to this nested product repository. The applicable generated-vault helper validation and exact manifest byte/hash parity pass. The OpenSpec change pack and Codex task graph remain separately schema-validated.

## Runtime matrix

| Environment | Python | Result | Representative managed Colab? |
|---|---|---|---:|
| Local Linux CPU | 3.13.5 | Pass | No |
| Local Jupyter kernel | 3.13.5 | Pass | No |
| Local Chromium static dashboard | Chromium/Playwright | 21/21 pass | No |
| Local Chromium mocked direct comm | Chromium/Playwright | Pass, experimental | No |
| Extracted wheel | 3.13.5 | Pass; local semantic display/reports/bundle, no drops or remote surface | No |
| Managed Colab CPU | Not run | Blocked | Pending |
| Managed Colab NVIDIA | Not run | Blocked | Pending |
| Managed Colab TPU and mounted Drive | Not run | Blocked | Pending |

## Remaining validation blockers

- Python 3.11 and 3.12 runtime execution.
- Reviewed `uv.lock` and `pnpm-lock.yaml` plus dependency/advisory review.
- Ruff, ty, executable pre-commit, and frozen Fumadocs production build.
- Managed Colab CPU, NVIDIA, TPU, Drive, iframe, and direct-comm evidence.
- Manual screen-reader, zoom, multi-browser, live-region, and managed-notebook review.
- Public owner/license/repository/package/release decisions.
