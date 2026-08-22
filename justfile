test:
    uv run pytest

lint:
    uv run ruff check src tests

format:
    uv run ruff format src tests

typecheck:
    uv run ty check

check: lint typecheck test
    uv run ruff format --check src tests

cli:
    uv run nbops --help

api:
    uv run uvicorn nbops.api:app --host 0.0.0.0 --port 8000
