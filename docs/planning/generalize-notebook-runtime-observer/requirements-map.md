---
status: active
type: requirements-map
change: generalize-notebook-runtime-observer
tags:
  - requirements
  - traceability
  - nbops
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Requirements map

| Domain | Requirements | Scenarios | Source |
|---|---:|---:|---|
| `compatibility-support` | 3 | 6 | `openspec/changes/generalize-notebook-runtime-observer/specs/compatibility-support/spec.md` |
| `measurement-scope` | 3 | 6 | `openspec/changes/generalize-notebook-runtime-observer/specs/measurement-scope/spec.md` |
| `migration-compatibility` | 3 | 7 | `openspec/changes/generalize-notebook-runtime-observer/specs/migration-compatibility/spec.md` |
| `notebook-display` | 3 | 6 | `openspec/changes/generalize-notebook-runtime-observer/specs/notebook-display/spec.md` |
| `package-identity` | 4 | 8 | `openspec/changes/generalize-notebook-runtime-observer/specs/package-identity/spec.md` |
| `platform-adapters` | 3 | 6 | `openspec/changes/generalize-notebook-runtime-observer/specs/platform-adapters/spec.md` |
| `platform-diagnostics` | 2 | 4 | `openspec/changes/generalize-notebook-runtime-observer/specs/platform-diagnostics/spec.md` |
| `runtime-profiles` | 3 | 6 | `openspec/changes/generalize-notebook-runtime-observer/specs/runtime-profiles/spec.md` |
| `security-policy` | 3 | 6 | `openspec/changes/generalize-notebook-runtime-observer/specs/security-policy/spec.md` |
| `storage-profiles` | 3 | 6 | `openspec/changes/generalize-notebook-runtime-observer/specs/storage-profiles/spec.md` |

## Totals

- Domains: 10
- Requirements: 30
- Scenarios: 61
- Tasks: 44

The `package-identity` domain fixes `nbops` as the current identity. `migration-compatibility` protects supported Colab behavior and legacy evidence without preserving the old identity as canonical.
