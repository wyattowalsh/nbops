set shell := ["bash", "-euo", "pipefail", "-c"]

alias qg := quality-gates

test:
    uv run pytest

lint:
    uv run ruff check src tests

format:
    uv run ruff format src tests

format-check:
    uv run ruff format --check src tests

typecheck:
    uv run ty check

check: lint typecheck format-check test

smoke:
    uv run nbops version
    uv run nbops --version
    uv run python -m nbops version
    uv run nbops ops
    uv run nbops stats examples/demo.ipynb --json
    uv run nbops lint examples/demo.ipynb
    uv run nbops convert examples/demo.ipynb --to py
    uv run nbops validate examples/demo.ipynb
    uv run nbops outputs examples/demo.ipynb --json
    uv run nbops batch validate examples
    uv run nbops serve --help

quality-gates: check smoke

cli:
    uv run nbops --help

api:
    uv run nbops serve --host 0.0.0.0 --port 8000
