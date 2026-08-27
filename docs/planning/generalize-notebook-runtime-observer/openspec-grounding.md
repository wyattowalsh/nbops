---
status: active
type: openspec-grounding
change: generalize-notebook-runtime-observer
tags: [openspec, traceability, grounding]
updated: 2026-08-22
cssclasses: [planning-doc]
---

# OpenSpec grounding

**Path:** `docs/planning/generalize-notebook-runtime-observer/openspec-grounding.md`  
**Purpose:** Map every derived plan, decision, task, support claim, and handoff to the follow-on OpenSpec change and protected Colab baseline.  
**Status:** Active  
**Load/use when:** Reviewing authority, preventing scope drift, or updating downstream artifacts after proposal/spec/design changes.

## Grounding rule

The implemented baseline remains `build-colab-observer`. The follow-on proposal defines why and scope; delta specs define observable behavior; design/ADRs define the approach; tasks define implementation and validation order. Derived planning docs may add evidence, sequencing, risks, and handoff mechanics but may not invent behavior.

| Derived artifact | OpenSpec/baseline anchor | Drift rule |
|---|---|---|
| Product and positioning | follow-on proposal; baseline proposal | Colab-first remains protected until explicit naming decision |
| Runtime profile/scope/storage/display | corresponding delta specs + design | Update tasks, schemas, tests, and support matrix after changes |
| Adapter and diagnostics plans | platform-adapters/platform-diagnostics specs | No platform-specific activation without required evidence |
| Migration and naming | migration-compatibility spec + ADR-016 | Compatibility fixtures precede refactor/rename |
| Support matrix | compatibility-support spec + validation evidence | Detection never equals support |
| Goal/handoff/PLANS | tasks + validation + traceability | Begin at TASK-103 and respect approvals |
| Finalization | proposal success criteria + validation | Planning completion is not implementation PASS |

## Reconciliation checklist

- [ ] Baseline API/default/artifact protections remain explicit.
- [ ] Every requirement maps to scenarios and tasks.
- [ ] Every support claim maps to representative evidence or BLOCKED status.
- [ ] Every ADR maps to requirements/tasks/validation.
- [ ] Any proposal/spec/design edit invalidates affected tasks, diagrams, handoffs, and support labels until updated.
- [ ] Apply, verify/sync, and archive are not claimed without implementation evidence and approval.
