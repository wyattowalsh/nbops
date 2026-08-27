---
status: active
type: validation
change: generalize-notebook-runtime-observer
tags:
  - validation
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Validation plan

## Evidence classes

Use `PASS` only for executed evidence. Distinguish structural/schema, unit/property, simulated, clean-wheel, local runtime, managed runtime, browser/manual accessibility, security, packaging, and human-review evidence.

## Planning and kickoff gates

| Gate | Expected |
|---|---|
| Canonical name scan | Active current surfaces use exact lowercase `nbops` |
| Candidate-name scan | No rejected candidate appears in the bundle |
| Historical allowlist | Old identifiers appear only in stable paths, provenance, or legacy compatibility |
| OpenSpec syntax | Every requirement has MUST/SHALL behavior and scenarios |
| Change-pack schema | Draft 2020-12 valid |
| Task-graph schema | Draft 2020-12 valid, unique IDs, acyclic dependencies |
| Task reconciliation | `tasks.md` and `task-graph.json` contain the same 44 IDs |
| Links | No broken relative Markdown links or wikilinks |
| JSON/YAML | Parse successfully |
| Manifests | Exact path/count/byte/SHA-256 parity |
| ZIP | Deterministic, CRC-clean, one root, no traversal/absolute/backslash/symlink/encryption |
| Clean extraction | Extracted bytes equal source bytes |

## Identity implementation gates

- Distribution metadata is `nbops`.
- Canonical source package is `src/nbops/`.
- Current public import is `nbops`.
- CLI entry point is `nbops`.
- New output directories, report titles, bundles, schemas, examples, snippets, and docs use `nbops`.
- Any legacy shim is thin, compatibility-only, and fixture-backed.
- Supported legacy artifacts remain readable and retain legacy provenance.
- Mixed current identity fails release validation.

## Repository gates to discover and preserve

```bash
make check
make coverage
make smoke
python scripts/check_precommit.py
python scripts/check_distribution.py dist
```

Use only commands present in the target repository. Do not install missing tools merely to satisfy this plan.

## Runtime matrix

| Environment | Required evidence | Current state |
|---|---|---|
| Plain Python | source/wheel lifecycle, persistence, export, no-network | Future implementation validation |
| IPython | semantic static display and fallback | Future implementation validation |
| Local JupyterLab/Notebook 7 | lifecycle, scope, display, export, failures | Blocked until runtime |
| Managed Google Colab | CPU, Drive, framework, accelerator, direct-comm decision | Blocked until runtime |
| Deepnote | storage profile, static display, lifecycle, export | Blocked until runtime |
| JupyterHub/server provider | kernel-local baseline and optional authenticated server boundary | Blocked/deferred |
| Python 3.11/3.12/3.13 | source and clean-wheel matrix | Partially blocked |

## Security negatives

Prove no default telemetry, public service, hosted backend, runtime CDN, remote code, keepalive, anti-idle, hidden reconnect, timeout bypass, quota circumvention, secret capture, automatic remediation, path traversal, unsafe archive member, unbounded provider output, or silent scope fabrication.

## Release boundary

Local identity migration is approved. Remote repository rename, registry publication, domain/handle operations, announcements, deployment, secrets, account/permission changes, and OpenSpec apply/sync/archive remain separately approval-gated.
