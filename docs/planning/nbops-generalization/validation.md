# Validation

Run from the repository root after `uv sync --locked --group dev`.

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run ty check
uv run pytest
uv run nbops version
uv run nbops ops
uv run nbops stats examples/demo.ipynb --json
uv run nbops lint examples/demo.ipynb
```

Compatibility invariants:

- `compute_stats` remains importable from `nbops` and `nbops.core`
- `nbops stats` remains the CLI stats command
- `POST /notebooks/stats` remains the HTTP stats endpoint

The original artifact `nbops-generalization-codex-kickoff-context-20260822` is
still missing. These gates validate the recovered G1–G19 program only.
