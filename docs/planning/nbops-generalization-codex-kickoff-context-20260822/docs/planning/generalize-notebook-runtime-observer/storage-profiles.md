---
status: proposed
type: storage-plan
change: generalize-notebook-runtime-observer
tags:
  - storage
  - persistence
  - deepnote
  - colab
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Storage profiles

**Path:** `docs/planning/generalize-notebook-runtime-observer/storage-profiles.md`  
**Purpose:** Define portable storage semantics, automatic-policy limits, platform mappings, write behavior, diagnostics, and validation.  
**Status:** Proposed

## Why storage is a platform capability

The same filesystem path API can represent local SSD, ephemeral container storage, FUSE/cloud mounts, NFS, or object-backed workspaces. Persistence and throughput must not be inferred from path shape alone.

## Profile dimensions

| Dimension | Values/examples |
|---|---|
| Persistence | durable, runtime-ephemeral, session-ephemeral, unknown |
| Locality | local, mounted, remote/object-backed, unknown |
| Write posture | high-frequency suitable, batched preferred, final-artifact only, unknown |
| Atomicity | local atomic replace supported/assumed, provider-defined, unknown |
| Metadata latency | low, measured elevated, unknown |
| Capacity evidence | measured, limit, estimate, unknown |
| User role | staging, primary DB, persistent destination, custom |
| Confidence | confirmed, probable, weak, unknown |

## Canonical storage classes

### Persistent local

Use for primary database and outputs when directly confirmed writable and durable.

### Ephemeral local

Use for high-frequency sampling and temporary report generation. Warn that runtime restart can lose artifacts. Persistence requires explicit output policy/finalization.

### Mounted cloud

Use cautiously. Preserve path safety, batch writes, measure/report latency when possible, and prefer consolidated final artifacts.

### Object-backed workspace

Treat as persistent but potentially expensive for many small writes. Stage the live database locally and publish consolidated outputs, subject to explicit policy.

### Unknown

Use generic safeguards and make no durability/throughput promise.

## Initial platform mapping hypotheses

These are planning hypotheses until representative runtime evidence confirms them.

| Platform | Location | Proposed profile | Evidence posture |
|---|---|---|---|
| Colab | `/content` | Ephemeral local | Current product assumption; managed validation still required |
| Colab | mounted Drive path | Mounted cloud/persistent destination | Existing read-only detection and Drive guidance |
| Local Jupyter | user-selected local path | Persistent local or unknown | Determine from configured path/evidence |
| Deepnote | `/tmp` | Fast ephemeral local staging | Official docs; direct runtime validation required |
| Deepnote | `/work` | Persistent object-backed workspace | Official docs; direct write/persistence validation required |
| JupyterHub | deployment path | Unknown/provider-defined | Never generalize across spawners/deployments |

## Output policy

Recommended policy values:

- `explicit`: use exactly the user-selected safe path.
- `auto`: select a safe staging/output posture from profile evidence and explain it.
- `local-staging`: keep active DB locally; publish only finalized artifacts to destination.
- `persistent-direct`: write directly when the location is confirmed suitable.

Exact public names are implementation candidates.

## Automatic policy constraints

An automatic policy may:

- choose among already available safe locations;
- choose batching cadence within global bounds;
- warn before shutdown/export;
- show the selected policy and reason.

It may not:

- mount storage;
- create provider integrations;
- authenticate to accounts;
- migrate arbitrary user data;
- delete or clean user files;
- copy artifacts to a new destination without configured intent;
- weaken path containment, alias rejection, atomic publication, checksum, or redaction controls.

## Deepnote workflow

Recommended preview behavior:

```text
start observer
  -> live SQLite and temporary reports in fast ephemeral location
  -> static dashboard in notebook
  -> explicit stop/export
  -> consolidated HTML/Markdown/CSV/JSONL/SQLite/ZIP
  -> explicit finalization to persistent workspace location
```

The report should state whether the persistent copy occurred. No keepalive or machine-lifetime manipulation.

## Colab workflow

Retain current safe posture:

- `/content` local staging/default where applicable;
- Drive mount detection only, never mount automatically;
- explicit Drive destination option;
- warnings about mounted-storage I/O and persistence;
- consolidate report bundle before copy.

## Diagnostics

Possible storage findings:

- ephemeral artifact loss risk;
- output destination unavailable;
- mounted/object-backed metadata latency;
- high write amplification;
- disk/capacity pressure;
- checkpoint/report size pressure;
- finalization incomplete;
- persistence status unknown.

All findings include evidence, scope, confidence, alternatives, limitations, and non-destructive actions.

## Validation matrix

| Check | Generic local | Colab | Deepnote | JupyterHub |
|---|---:|---:|---:|---:|
| Path safety/alias containment | Required | Required | Required | Required |
| Live DB integrity | Required | Required | Required | Required |
| Persistence across runtime restart | Environment-specific | Managed test | Managed test | Deployment-specific |
| High-frequency write behavior | Benchmark | Benchmark | `/tmp` vs `/work` benchmark | Deployment-specific |
| Explicit finalization | Required | Drive optional | `/work` optional | Configured destination |
| Unknown classification fallback | Required | Required | Required | Required |
| No mount/account mutation | Required | Required | Required | Required |
