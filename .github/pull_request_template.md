## Description

<!-- Briefly describe what this PR does and why. -->

## Related Issues

<!-- Fixes #123 / Closes #456 -->

## Change Type

- [ ] `feat:` New feature
- [ ] `fix:` Bug fix
- [ ] `refactor:` Code restructuring (no behavior change)
- [ ] `docs:` Documentation only
- [ ] `test:` Test additions or fixes
- [ ] `chore:` Build, CI, or dependency update

## Checklist

- [ ] Tests added or updated (`uv run pytest`)
- [ ] Lint passes (`uv run ruff check src tests`)
- [ ] Format passes (`uv run ruff format --check src tests`)
- [ ] Type check passes (`uv run ty check`)
- [ ] Compatibility invariants hold (`compute_stats`, `nbops stats`, `POST /notebooks/stats`)
- [ ] Catalog CLI/API strings still match live surfaces (`nbops ops` / `GET /operations`)
