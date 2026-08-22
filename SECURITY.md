# Security Policy

## Scope

nbops is a local Jupyter notebook operations library, CLI, and optional HTTP API.
It does not authenticate users, store secrets, or call undocumented notebook
provider APIs.

## Supported Versions

Only the latest release on the `main` branch is supported.

| Version | Supported |
| ------- | --------- |
| latest  | Yes |
| < latest | No |

## Reporting a Vulnerability

Report security issues to **wyattowalsh@gmail.com**.

Include a description, reproduction steps, and impact. Please do not open a
public GitHub issue for undisclosed vulnerabilities.

**In scope**

- Path traversal or unexpected file writes from CLI/API notebook paths
- Dependency vulnerabilities in runtime extras
- Secrets accidentally committed to this repository

**Out of scope**

- Malicious notebook content executed via `nbops[execute]` (kernels run caller code)
- Jupyter/nbformat/nbclient issues that belong upstream
- Denial of service against a locally started uvicorn process

## Response

- Acknowledgment within 72 hours
- Coordinated disclosure: do not publish details until a fix ships or 90 days
  have passed, whichever comes first
