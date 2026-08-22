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
| TASK-002 | I/O via nbformat (load/save/validate/new) | done | `src/nbops/io.py`; `nbops validate`; `POST /notebooks/validate` |
| TASK-003 | Inspect (stats, outline, imports, outputs) | done | `src/nbops/inspect.py`; `nbops outputs` |
| TASK-004 | Clean outputs/counts/ids/empty cells | done | `src/nbops/clean.py`; widgets and output-linked cell keys stripped with outputs |
| TASK-005 | Transform (filter, concat, split, kernel, tags, ids) | done | `src/nbops/transform.py`; `add_tags` / `remove_tags` |
| TASK-006 | Lint catalog NB000–NB011 | done | `src/nbops/lint.py` |
| TASK-007 | Convert to percent py / script / md, plus percent roundtrip | done | `src/nbops/convert.py`; cell tags round-trip; `[md]` alias; Jupytext YAML kernelspec |
| TASK-008 | Cell-level diff | done | `src/nbops/diff.py` |
| TASK-009 | Directory batch + tqdm | done | `src/nbops/batch.py`; `nbops batch {stats,lint,clean,validate}` |
| TASK-010 | Optional `nbops[execute]` | done | `src/nbops/execute.py` |
| TASK-011 | Typer CLI for every catalog operation | done | `src/nbops/cli.py`; system commands `version`/`serve` are not catalog ops |
| TASK-012 | FastAPI surface + `GET /operations` | done | `src/nbops/api.py` |
| TASK-013 | Preserve stats scaffold contract | done | `core.py`, `stats`, `/notebooks/stats` |
| TASK-014 | Tests mirroring src, coverage ≥90% | done | `tests/`, `--cov-fail-under=90` |
| TASK-015 | CI: actionlint + ruff + ty + pytest 3.12/3.13 | done | `.github/workflows/ci.yml` |
| TASK-016 | AGENTS.md, CONTRIBUTING.md, README, CHANGELOG | done | repo root + `CODE_OF_CONDUCT.md` + `CLAUDE.md` |
| TASK-017 | uv lockfile + justfile | done | `uv.lock`, `justfile` (`check`, `quality-gates`, `smoke`) |
| TASK-018 | Shared operations catalog | done | `src/nbops/operations.py` |
| TASK-019 | `NBOPS_` pydantic-settings + optional `.env` | done | `src/nbops/settings.py`; `.env.example` |
| TASK-020 | SECURITY.md | done | `SECURITY.md` |
| TASK-021 | Dependabot (pip + github-actions) | done | `.github/dependabot.yml` |
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
