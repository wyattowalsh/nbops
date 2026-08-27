---
status: proposed
type: data-model
change: generalize-notebook-runtime-observer
tags:
  - runtime-profile
  - schema
  - evidence
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Runtime profile model

**Path:** `docs/planning/generalize-notebook-runtime-observer/runtime-profile-model.md`  
**Purpose:** Define the canonical profile facets, evidence model, conflict handling, serialization, privacy, and compatibility expectations.  
**Status:** Proposed

## Problem

A single platform field cannot explain what the observer can see or do. “Colab,” “Jupyter,” and “Deepnote” mix provider, frontend, kernel, storage, process isolation, quota, and transport facts. Treating them as one enum encourages false capability inference.

## Proposed logical model

```python
RuntimeProfile(
    schema_version=...,
    provider=FacetClaim(...),
    frontend=FacetClaim(...),
    kernel=KernelProfile(...),
    execution_scope=...,
    resource_scope=...,
    limit_sources=(...),
    storage_locations=(...),
    display_transports=(...),
    capabilities=(...),
    support=SupportEvidence(...),
    evidence=(...),
    conflicts=(...),
    generated_at=...,
)
```

This is a logical contract. Exact classes, field names, and module paths belong to implementation tasks and may change without changing the behavior spec.

## Facets

### Provider

| Field | Meaning |
|---|---|
| `id` | Stable bounded provider identifier, or `generic`/`unknown`. |
| `release` | Provider runtime/release evidence when non-sensitive and available. |
| `confidence` | Confirmed/probable/weak/unknown equivalent. |
| `evidence_ids` | References to bounded evidence entries. |
| `limitations` | Why the claim may be incomplete or stale. |

### Frontend

Possible initial identities:

- terminal IPython;
- JupyterLab;
- Jupyter Notebook;
- Google Colab;
- Deepnote;
- VS Code notebook;
- unknown rich frontend;
- none/terminal.

Frontend identity is not required for static display. It is required for a frontend-specific transport support claim.

### Kernel

- language;
- implementation;
- version;
- process identity reduced to non-sensitive local metadata;
- kernel protocol capability when directly evidenced.

Python is required for the package. Detecting a Jupyter environment with an R or Julia kernel does not make the Python package support that kernel.

### Scope

See `measurement-scope.md`. Profile-level scope describes the default interpretation; observations may override it when a collector has narrower or stronger evidence.

### Storage locations

Each location records:

- logical role: output root, staging, persistent destination, provider workspace, custom;
- safe normalized path or redacted descriptor;
- class;
- persistence expectation;
- throughput posture;
- write semantics/limitations;
- evidence/confidence;
- whether it was selected, user-configured, or merely detected.

### Display transports

Each transport records:

- identifier;
- status: available/unavailable/experimental/disabled;
- support evidence;
- activation mode: automatic, explicit, unsupported;
- local-asset/network/public-service properties;
- fallback transport;
- limitations.

### Support evidence

The runtime profile records what the current release knows about this exact environment combination. Product docs may summarize this data but cannot silently upgrade it.

## Evidence record

| Field | Contract |
|---|---|
| `id` | Deterministic within the profile. |
| `adapter_id` | First-party adapter producing the claim. |
| `facet` | Provider, frontend, scope, storage, transport, capability, or support. |
| `claim` | Bounded enum/value. |
| `source_type` | Runtime API, module metadata, path capability, environment presence, user config, server provider, or fixture. |
| `confidence` | Ordered, documented scale. |
| `observed_at` | Offset-aware timestamp. |
| `limitations` | Human-readable bounded limitations. |
| `sensitivity` | Public, redacted, sensitive-not-exported equivalent. |
| `raw_value` | Not persisted by default; use reduced evidence only. |

## Confidence policy

Recommended scale:

| Level | Meaning | Example |
|---|---|---|
| Confirmed | Direct provider/runtime API or representative harness | Managed Colab module plus `/content` and release evidence in a real Colab run |
| Probable | Multiple independent local signatures | Provider module spec plus provider-specific path/capability |
| Weak | One heuristic with plausible collisions | Environment variable presence alone |
| Unknown | No adequate evidence | Generic Python process |

Capability activation defines its required minimum confidence. Static/text behavior requires no provider claim.

## Conflict policy

A conflict is first-class when:

- equal/high-confidence claims disagree;
- user override conflicts with measured capability;
- provider identity and frontend evidence imply incompatible transports;
- storage classification evidence disagrees materially;
- server evidence and kernel-local evidence disagree about scope/limits.

Conflict outcomes:

- retain both claims and evidence;
- select neither for behavior that requires resolution;
- use safe generic fallback;
- surface the conflict in profile/report/support bundle;
- allow explicit user review, not silent coercion.

## Capability derivation

Capabilities should be derived from evidence and contract rules, not freely emitted booleans.

Examples:

```text
ipython rich display evidence
+ static renderer available
=> static-html available

confirmed Colab provider
+ direct comm implementation present
+ current release evidence absent
=> direct-comm experimental, explicit only

kernel-only Jupyter evidence
+ no server provider
=> server metrics unavailable
```

## Privacy

The model must not require or default-export:

- usernames;
- email/account IDs;
- workspace/project IDs;
- full hostnames;
- notebook names or source;
- raw environment values;
- server tokens;
- kernel connection file contents;
- full process commands;
- unrestricted paths.

Paths follow existing redaction/containment policy. Evidence prefers bounded categories and booleans.

## Serialization

Requirements:

- explicit profile schema version;
- canonical ordering;
- stable enum values;
- deterministic evidence IDs/digest;
- no dependence on Python object identity or detector order;
- offset-aware timestamps;
- finite numeric values only;
- bounded evidence/conflict lists;
- JSON Schema parity in root and wheel;
- legacy profile absence accepted by readers.

## Persistence options

### Option A: inline profile on every observation

Reject. Too much repetition and export size.

### Option B: one run profile plus per-observation scope override

Recommended. Most evidence is run-level; metric scope can vary.

### Option C: profile snapshots over time

Defer. Useful if environments mutate, but adds complexity before explicit refresh behavior exists.

## Review questions

- Is provider identity useful enough to expose publicly, or should consumers rely primarily on capabilities?
- What confidence levels are safe to make API-stable?
- Should support tier be runtime profile data or release evidence joined by environment key?
- How should user overrides be serialized without confusing them with measured facts?

## Acceptance checklist

- [ ] Equivalent evidence produces equivalent canonical profile.
- [ ] Unknown facets do not suppress known facets.
- [ ] Conflicts are preserved and disable unsafe capability inference.
- [ ] Sensitive raw evidence is not persisted/exported.
- [ ] Legacy runs load with unknown/legacy profile state.
- [ ] Profile data does not dominate observation/storage size.
