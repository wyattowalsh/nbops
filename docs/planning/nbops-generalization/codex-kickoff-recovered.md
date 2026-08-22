# Recovered Codex kickoff program (not the original dump)

> [!WARNING]
> This is **not** `nbops-generalization-codex-kickoff-context-20260822`. That
> file was never found. This recovered program is the union of:
>
> 1. Wyatt’s **Build • Codex kickoff** composition (`aiteam` + `aitasks` +
>    `devbase` + `aiverify` + `aifinal`) plus `devpy` Python defaults
> 2. The empty `main` tree and the stats-only `cursor/setup-dev-environment-a5a8`
>    scaffold
> 3. The nbadb / proxywhirl Python library quality bar
>
> If the original dump is attached later, rebase onto it.

## TASK graph

| ID | Task | Status | Evidence |
| -- | ---- | ------ | -------- |
| TASK-001 | Domain-general `src/nbops` package | done | `src/nbops/` |
| TASK-002 | I/O via nbformat (load/save/validate/new); v4 omitted cell ids preserved | done | `src/nbops/io.py`; `nbops validate`; `POST /notebooks/validate` |
| TASK-003 | Inspect (stats, outline, imports, outputs) | done | `src/nbops/inspect.py`; `nbops outputs`; `extract_imports` skips IPython magics / non-Python kernels / `%%writefile`; heading outline is ATX+setext and skips fences; `compute_stats` reports `attachment_cells` / `attachment_files`; CLI extras print widgets and attachment counts |
| TASK-004 | Clean outputs/counts/ids/empty cells | done | `src/nbops/clean.py`; widgets and output-linked cell keys stripped with outputs; attachments kept; attachment-only cells are not dropped as empty |
| TASK-005 | Transform (filter, concat, split, kernel, tags, ids) | done | `src/nbops/transform.py`; `add_tags` / `remove_tags` |
| TASK-006 | Lint catalog NB000–NB011 | done | `src/nbops/lint.py`; `NB007` is IPython-aware and skipped for non-Python kernels and file-body magics; `NB002` uses the shared heading extractor |
| TASK-007 | Convert to percent py / script / md, plus percent roundtrip | done | `src/nbops/convert.py`; tags, ids, optional Jupytext titles, generic `key=value`/JSON cell metadata, and kernelspec YAML round-trip; `[md]` alias; omitted ids stay omitted; markdown inlines `attachment:` and code-cell `image/*` outputs as `data:` URIs, emits stream/error/text outputs, and appends unreferenced image attachments |
| TASK-008 | Cell-level diff | done | `src/nbops/diff.py`; signature is type + source + attachments |
| TASK-009 | Directory batch + tqdm | done | `src/nbops/batch.py`; `nbops batch {stats,lint,clean,validate}` |
| TASK-010 | Optional `nbops[execute]` | done | `src/nbops/execute.py`; omitted cell ids restored after execute |
| TASK-011 | Typer CLI for every catalog operation | done | `src/nbops/cli.py`; system commands `version`/`serve` are not catalog ops |
| TASK-012 | FastAPI surface + `GET /operations` | done | `src/nbops/api.py` |
| TASK-013 | Preserve stats scaffold contract | done | `core.py`, `stats`, `/notebooks/stats`; original seven-row CLI table; `uvicorn nbops.api:app` and `/docs` in README; `HealthResponse()` defaults; OpenAPI `StatsRequest`; original shipped demo; live uvicorn; frozen original suite in `tests/original_scaffold/` |
| TASK-014 | Tests mirroring src, coverage ≥90% | done | `tests/` including `tests/original_scaffold/`; `--cov-fail-under=90` |
| TASK-015 | CI: actionlint + ruff + ty + pytest 3.12/3.13 | done | `.github/workflows/ci.yml` |
| TASK-016 | AGENTS.md, CONTRIBUTING.md, README, CHANGELOG | done | repo root + `CODE_OF_CONDUCT.md` + `CLAUDE.md`; OpenSpec baseline in `openspec/specs/` |
| TASK-017 | uv lockfile + justfile | done | `uv.lock`, `justfile` (`check`, `quality-gates`, `smoke`) |
| TASK-018 | Shared operations catalog | done | `src/nbops/operations.py` |
| TASK-019 | `NBOPS_` pydantic-settings + optional `.env` | done | `src/nbops/settings.py`; `.env.example` |
| TASK-020 | SECURITY.md | done | `SECURITY.md` |
| TASK-021 | Dependabot (uv + github-actions) | done | `.github/dependabot.yml` `uv` ecosystem (updates `uv.lock`); `.github/labels.yml` catalogs referenced label names |
| TASK-022 | Pre-commit (hooks + ruff) | done | `.pre-commit-config.yaml` |
| TASK-023 | Ruff TCH + nbadb-like select | done | `pyproject.toml` |

## Gates

```bash
uv sync --locked --group dev
uv run ruff check src tests
uv run ruff format --check src tests
uv run ty check
uv run pytest
uv run nbops stats examples/demo.ipynb --json
uv run nbops --version
uv run python -m nbops version
uv run nbops serve --help
```

Compatibility invariant: `compute_stats`, `nbops stats`, `POST /notebooks/stats`.
