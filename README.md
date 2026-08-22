# nbops

> Lightweight operations toolkit for Jupyter notebooks — a small, well-tested Python
> package exposing notebook analysis through both a CLI and an HTTP API.

`nbops` parses standard Jupyter notebook (`nbformat` v4) documents and derives
deterministic statistics (cell counts by type, non-empty lines of code, kernel and
language metadata). It ships two entry points backed by the same pure core logic:

- a **Typer** command line interface (`nbops`)
- a **FastAPI** service (`nbops.api:app`)

## Requirements

- Python `>=3.12`
- [`uv`](https://docs.astral.sh/uv/) for dependency management

## Quickstart

```bash
# Install dependencies into a project-local virtual environment
uv sync

# Show the CLI help
uv run nbops --help

# Analyze a notebook
uv run nbops stats examples/demo.ipynb

# Machine-readable output
uv run nbops stats examples/demo.ipynb --json
```

## Running the API

```bash
# Start the development server (http://127.0.0.1:8000)
uv run uvicorn nbops.api:app --host 0.0.0.0 --port 8000

# In another shell:
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/notebooks/stats \
  -H 'content-type: application/json' \
  -d "{\"notebook\": $(cat examples/demo.ipynb)}"
```

Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## Development

```bash
uv sync              # install runtime + dev dependencies
uv run ruff check .  # lint
uv run ruff format . # format
uv run pytest        # run the test suite
```

## Project layout

```
src/nbops/
  core.py   # pure notebook-analysis logic (no I/O side effects)
  cli.py    # Typer CLI
  api.py    # FastAPI application
tests/      # pytest suite (unit + API)
examples/   # sample notebook for demos
```

## License

See [LICENSE](./LICENSE).
