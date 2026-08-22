# Contributing

1. Use `uv` for all Python operations (`uv sync`, `uv add`, `uv run`).
2. Keep source in `src/nbops/` and tests in `tests/` mirroring the package.
3. Before opening a PR, run:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run ty check
uv run pytest
```

4. Do not commit secrets, notebooks with huge outputs, or hand-edited lockfiles.
5. Prefer absolute `nbops.*` imports.
6. Follow the [Code of Conduct](./CODE_OF_CONDUCT.md).
