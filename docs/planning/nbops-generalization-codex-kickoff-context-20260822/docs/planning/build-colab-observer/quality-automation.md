---
status: proposed
type: quality-plan
change: build-colab-observer
tags:
  - pre-commit
  - quality
  - developer-experience
updated: 2026-07-11
cssclasses:
  - planning-doc
---

# Quality automation and pre-commit plan

## Principles

- One documented command per concern, reused locally and in CI.
- Fast staged checks; heavier checks in pre-push/manual/CI.
- Locked environments and deterministic generated artifacts.
- Hooks report and fail; they do not perform surprising broad mutation.
- No network requirement for the routine staged gate.
- Product policy and accessibility receive executable checks, not prose only.

## Proposed command surface

```bash
uv sync --all-groups
pnpm install --frozen-lockfile

uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest
uv build

pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm build

pre-commit run --all-files
pre-commit run --hook-stage pre-push --all-files
```

Verify exact commands after repository scaffold. `uv` manages Python environments/locks even if the selected build backend is not `uv_build`.

## Hook stages

### Commit stage: fast and offline

| Hook | Scope | Behavior |
|---|---|---|
| trailing whitespace/end-of-file/mixed line endings | text | Safe narrow fixes or check-only policy |
| merge conflict/case conflict/symlink checks | repo | Fail with paths |
| JSON/YAML/TOML syntax | metadata | Parse only; schema checks where local |
| Markdown lint/style | docs | No mass rewrite; changed files where possible |
| Ruff format/check | Python | Changed files or bounded repository pass |
| TypeScript format/lint | web | Changed files through pnpm scripts |
| notebook structure/output | notebooks | Validate JSON, metadata, unexpected output/size |
| secret/private-key scan | all | Baseline-reviewed detections; no secret values in baseline |
| large file/archive/cache guard | all | Reject accidental artifacts and nested zips |
| prohibited behavior scan | executable/notebooks | Context-aware keepalive/anti-idle/bypass rules |
| OpenSpec syntax check | change specs | Requirement/scenario headings and behavior boundary heuristics |
| snippet drift | source/docs/notebooks | Canonical snippet equality |

### Pre-push/manual stage: heavier

- full Ruff and ty;
- targeted/full pytest;
- frontend type/unit tests;
- docs build and generated checks;
- notebook smoke source tests;
- package build/wheel-content inspection;
- OpenSpec strict validation when installed;
- accessibility component tests that do not require deployed browser infrastructure.

### CI-only or explicit local stage

- full browser/widget end-to-end;
- external link check;
- current Colab CPU/GPU smoke;
- dependency/security network scans;
- Vercel preview/deployment checks;
- publish/release dry runs.

## Hook implementation choice

Use pinned standard pre-commit hooks for generic repository hygiene. Use project-local `language: system` wrapper scripts for commands that must share the `uv`/`pnpm` locks with CI. Bootstrap docs state dependencies clearly; hooks must not silently install or contact the network.

## Policy scanners

### Prohibited behavior

Scan executable Python, JavaScript/TypeScript, shell, and notebook cells for patterns related to:

- repeated UI clicks or DOM activity simulation;
- auto reconnect/connect loops;
- keepalive/anti-idle naming and timing loops;
- hidden audio/video/worker activity intended to extend sessions;
- quota/resource-allocation circumvention.

Allow occurrences only in safety documentation, rule configuration, and negative-test fixtures through path- and syntax-aware exclusions. Any executable allowlist requires review.

### Sensitive data

- Reject `.env`, credentials, tokens, private keys, cookies, service-account files, and notebook auth output.
- Generate `.env.example` only if an optional integration later needs variable names.
- Reject full exported observer run bundles from source control unless a minimal redacted fixture is explicitly reviewed.

### Generated assets

- Dashboard build writes only to its controlled generated directory.
- Check source hash/build metadata and fail on stale output.
- Inspect the wheel for required local assets and forbidden sourcemaps/internal files.
- Generate docs indexes and API/diagnostic pages deterministically.

## Failure UX

Each hook prints:

1. concise rule and file;
2. why it matters;
3. exact safe local command to reproduce/fix;
4. whether the hook changed a file;
5. how to request a reviewed exception.

Skipping hooks is not a completion signal; CI remains authoritative.
