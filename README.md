# nbops

General operations toolkit for Jupyter notebooks.

`nbops` is a Python library, Typer CLI, and FastAPI service for inspect, lint,
clean, transform, convert, diff, batch, and optional execute workflows over
standard `nbformat` documents. The toy stats-only scaffold is preserved as a
compatibility surface (`compute_stats`, `nbops stats`, `POST /notebooks/stats`)
and generalized into a full operations toolkit.

## Requirements

- Python `>=3.12`
- [`uv`](https://docs.astral.sh/uv/) for dependency management

## Install

```bash
uv sync
uv run nbops --help
```

Optional execution extra (nbclient + ipykernel):

```bash
uv sync --extra execute
```

## Library

```python
from nbops import (
    clean_notebook,
    compute_stats,
    convert_notebook,
    diff_notebooks,
    lint_notebook,
    load_notebook,
)

notebook = load_notebook("examples/demo.ipynb", validate=False)
print(compute_stats(notebook).code_lines)
print(lint_notebook(notebook).passed)
print(convert_notebook(notebook, "md").text)
```

## CLI

```bash
uv run nbops stats examples/demo.ipynb
uv run nbops stats examples/demo.ipynb --json
uv run nbops inspect examples/demo.ipynb
uv run nbops headings examples/demo.ipynb
uv run nbops imports examples/demo.ipynb
uv run nbops lint examples/demo.ipynb
uv run nbops clean examples/demo.ipynb -o /tmp/clean.ipynb
uv run nbops convert examples/demo.ipynb --to md
uv run nbops concat a.ipynb b.ipynb -o merged.ipynb
uv run nbops split examples/demo.ipynb -o /tmp/parts
uv run nbops diff a.ipynb b.ipynb
uv run nbops new /tmp/empty.ipynb
uv run nbops filter examples/demo.ipynb --type code -o /tmp/code.ipynb
uv run nbops tag examples/demo.ipynb --cell 0 --add intro -o /tmp/tagged.ipynb
uv run nbops ids examples/demo.ipynb -o /tmp/ids.ipynb
uv run nbops ops
uv run nbops batch stats examples --json
uv run nbops batch lint examples
uv run nbops batch clean examples
```

## HTTP API

```bash
uv run uvicorn nbops.api:app --host 0.0.0.0 --port 8000
```

| Method | Path | Purpose |
| ------ | ---- | ------- |
| `GET` | `/health` | Liveness |
| `GET` | `/operations` | Operations catalog |
| `POST` | `/notebooks/stats` | Cell/code statistics |
| `POST` | `/notebooks/inspect` | Stats + outline + imports |
| `POST` | `/notebooks/lint` | Structural quality report |
| `POST` | `/notebooks/clean` | Strip outputs and residue |
| `POST` | `/notebooks/convert` | `py` / `script` / `md` |
| `POST` | `/notebooks/concat` | Concatenate notebooks |
| `POST` | `/notebooks/split` | Split on markdown headings |
| `POST` | `/notebooks/filter` | Keep cells by type/tag |
| `POST` | `/notebooks/tag` | Add cell tags |
| `POST` | `/notebooks/ids` | Assign unique cell ids |
| `POST` | `/notebooks/kernel` | Set kernelspec |
| `POST` | `/notebooks/diff` | Cell-level diff |
| `POST` | `/notebooks/execute` | Execute (`nbops[execute]`) |
| `POST` | `/notebooks/new` | Empty nbformat v4 notebook |

Interactive docs: `http://127.0.0.1:8000/docs`.

## Development

```bash
uv sync
uv run ruff check src tests
uv run ruff format src tests
uv run ty check
uv run pytest
```

Or `just check`.

## Layout

```text
src/nbops/
  io.py         load, save, validate, new
  inspect.py    stats, outline, imports
  clean.py      strip outputs / counts / ids
  transform.py  filter, concat, split, kernel, tags
  lint.py       structural quality
  convert.py    percent Python, script, Markdown
  diff.py       cell-level diff
  batch.py      directory walks
  execute.py    optional nbclient execution
  cli.py        Typer CLI
  api.py        FastAPI app
tests/          mirrors src/
examples/       demo notebook
```

## License

MIT. See [LICENSE](./LICENSE).
