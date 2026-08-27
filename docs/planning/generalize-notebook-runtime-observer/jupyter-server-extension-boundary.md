---
status: proposed
type: security-design
change: generalize-notebook-runtime-observer
tags:
  - jupyter
  - server-extension
  - security
updated: 2026-08-22
cssclasses:
  - planning-doc
---

# Optional Jupyter Server integration boundary

**Path:** `docs/planning/generalize-notebook-runtime-observer/jupyter-server-extension-boundary.md`  
**Purpose:** Bound the optional server-level evidence spike, security posture, interoperability question, and no-go criteria.  
**Status:** Proposed  

## Why it is separate

A kernel package and a Jupyter Server extension have different installation, authority, authentication, and deployment surfaces. Server integration is therefore optional and cannot be required for core operation.

## Candidate value

- server/child process totals;
- sibling-kernel inventory where authorized;
- configured resource limits or cgroup evidence closer to the spawner;
- server/frontend version evidence;
- reconciliation with `jupyter-resource-usage` rather than duplicating its gauge.

## Required controls

- explicit install and enablement;
- authenticated requests;
- authorization for each evidence resource/action;
- read-only, bounded, namespaced endpoints;
- no token/key export;
- localhost/server-origin use, no public bind by default;
- no notebook contents or unrelated user data;
- rate, response-size, and cardinality limits;
- documented disable/uninstall and kernel-only fallback;
- no automatic package or server configuration mutation.

## Interoperability options

| Option | Advantage | Risk | Initial posture |
|---|---|---|---|
| Consume `jupyter-resource-usage` API when installed | Reuses established server metrics | API/version dependency | Investigate first |
| Independent minimal provider | Stable project-specific schema | Duplicates logic and attack surface | Spike only if needed |
| No server provider | Lowest burden/security surface | Kernel scope only | Acceptable default/no-go outcome |

## Go criteria

- A real Jupyter/JupyterHub deployment shows material diagnostic value unavailable from the kernel.
- Authentication and authorization are testable in representative setups.
- Interoperability/version strategy is maintainable.
- Package size/startup/support costs are acceptable.

## No-go criteria

- Requires server tokens in notebook output/config.
- Requires public unauthenticated endpoints.
- Duplicates `jupyter-resource-usage` without differentiated value.
- Breaks managed-hosted notebook compatibility or core install simplicity.
- Cannot reliably separate users/kernels in multi-user deployments.
