---
status: proposed
type: planning
change: generalize-notebook-runtime-observer
tags:
  - scope
  - metrics
  - truthfulness
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Measurement scope

**Path:** `docs/planning/generalize-notebook-runtime-observer/measurement-scope.md`  
**Purpose:** Prevent notebook, kernel, process, container, server, host, capacity, and quota evidence from being conflated.  
**Status:** Proposed

## Core rule

> Every value must answer “what does this measure?” before the UI answers “how much?”

## Scope dimensions

### Execution scope

What execution unit produced or owns the evidence?

- observer process;
- process tree;
- Python kernel;
- container/runtime;
- Jupyter server;
- physical/virtual host;
- provider workspace or quota;
- unknown.

### Resource scope

What population does the metric cover?

- self;
- process tree;
- selected process set;
- container-visible total;
- server process tree;
- host-visible total;
- device;
- provider-defined quota;
- unknown.

### Limit source

Where did a capacity/limit come from?

- kernel/process API;
- cgroup;
- rlimit;
- operating system;
- device provider;
- Jupyter Server provider;
- hosted platform evidence;
- explicit user configuration;
- unknown.

## Scope examples

| Metric | Likely scope | What it cannot imply |
|---|---|---|
| Process RSS | Self process | Whole notebook, server, or container usage |
| Descendant RSS aggregate | Process tree | Sibling kernels or host usage |
| `psutil.virtual_memory()` in container | Container-visible/OS-visible, evidence-dependent | Physical host capacity without proof |
| NVML device memory used | GPU device | Memory attributable to this kernel unless process mapping is confirmed |
| Framework allocated VRAM | Framework/process context | Total device usage |
| Jupyter Server resource endpoint | Server-defined | Host or provider quota unless endpoint defines it |
| Deepnote/Colab quota message | Provider-defined | Current local usage unless separately measured |

## Notebook document boundary

A notebook document contains cells and outputs managed by a frontend/server. The Python kernel receives code to execute but does not inherently know which notebook document, browser tab, or user action owns every process or resource.

Therefore:

- do not label kernel metrics as “this notebook” without explicit supported mapping;
- do not read notebook source to create that mapping by default;
- do not claim sibling kernels are included;
- report “current Python runtime,” “observer process tree,” or another evidenced term.

## Resource-limit semantics

```text
usage != capacity != enforced limit != provider quota
```

Examples:

- visible RAM total may be container capacity, host total, or a virtualized view;
- cgroup limit may be a hard enforced limit;
- provider quota may cover workspace time, credits, or allocations rather than current memory;
- absence of a detected limit means unknown, not unlimited.

## Proposed observation interpretation

Each observation can inherit run-level scope and override it when necessary:

```text
run profile:
  default execution_scope = kernel/process-tree
  default resource_scope = container-visible

observation overrides:
  process.rss_bytes -> self
  process_tree.rss_bytes -> process-tree
  gpu.device.memory_used_bytes -> device
  torch.cuda.allocated_bytes -> framework/process
```

## UI wording

### Prefer

- “Visible RAM used”
- “Observer process RSS”
- “Visible process-tree CPU”
- “GPU device memory used”
- “PyTorch allocated VRAM”
- “Limit unavailable”
- “Container-visible capacity”

### Avoid unless evidenced

- “Notebook memory”
- “Machine memory”
- “Server CPU”
- “Host total”
- “Unlimited”
- “Your quota”

## Diagnostic consequences

A rule must declare required scopes.

Example: “GPU allocated but unused” may require:

- framework allocated VRAM at process/framework scope;
- device utilization at device scope;
- freshness alignment;
- workload evidence;
- alternative explanations.

It must not compare unrelated values without explaining the scope mismatch.

## Export/report consequences

Portable artifacts must preserve:

- profile digest/version;
- scope descriptor;
- limit source;
- quality/freshness;
- limitations/conflicts;
- units and source;
- whether a value was measured, estimated, user-supplied, or unavailable.

## Validation cases

- self value cannot populate process-tree field;
- container-visible value cannot be labeled host-visible;
- missing limit serializes as unknown/unavailable, not infinity;
- user-supplied limit remains labeled user-supplied;
- legacy bundle without scope remains legacy/unknown;
- report/table/chart labels use the same scope terminology;
- diagnostics reject incompatible scopes or disclose the limitation.
