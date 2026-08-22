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
    from_percent_python,
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
uv run nbops --version
uv run python -m nbops version
uv run nbops stats examples/demo.ipynb
uv run nbops stats examples/demo.ipynb --json
uv run nbops inspect examples/demo.ipynb
uv run nbops headings examples/demo.ipynb
uv run nbops imports examples/demo.ipynb
uv run nbops outputs examples/demo.ipynb
uv run nbops lint examples/demo.ipynb
uv run nbops validate examples/demo.ipynb
uv run nbops clean examples/demo.ipynb -o /tmp/clean.ipynb
uv run nbops clean examples/demo.ipynb --strip-metadata collapsed -o /tmp/clean.ipynb
uv run nbops convert examples/demo.ipynb --to md
uv run nbops convert examples/demo.ipynb --to py -o /tmp/demo.py
uv run nbops from-py /tmp/demo.py -o /tmp/from-py.ipynb
uv run nbops concat a.ipynb b.ipynb -o merged.ipynb
uv run nbops split examples/demo.ipynb -o /tmp/parts
uv run nbops diff a.ipynb b.ipynb
uv run nbops new /tmp/empty.ipynb
uv run nbops new /tmp/r.ipynb --kernel ir --language r --display-name R
uv run nbops kernel examples/demo.ipynb --name python3 --language python -o /tmp/k.ipynb
uv run nbops exec examples/demo.ipynb -o /tmp/executed.ipynb
uv run nbops filter examples/demo.ipynb --type code -o /tmp/code.ipynb
uv run nbops tag examples/demo.ipynb --cell 0 --add intro -o /tmp/tagged.ipynb
uv run nbops tag examples/demo.ipynb --cell 1 --remove demo -o /tmp/untagged.ipynb
uv run nbops ids examples/demo.ipynb -o /tmp/ids.ipynb
uv run nbops ops
uv run nbops batch stats examples --json
uv run nbops batch lint examples
uv run nbops batch clean examples
uv run nbops batch validate examples
```

## HTTP API

```bash
uv run nbops serve --host 0.0.0.0 --port 8000
```

| Method | Path | Purpose |
| ------ | ---- | ------- |
| `GET` | `/health` | Liveness |
| `GET` | `/operations` | Operations catalog |
| `POST` | `/notebooks/stats` | Cell/code statistics |
| `POST` | `/notebooks/inspect` | Stats + outline + imports + outputs |
| `POST` | `/notebooks/headings` | Markdown heading outline |
| `POST` | `/notebooks/imports` | Top-level imports |
| `POST` | `/notebooks/outputs` | Code-cell output inventory |
| `POST` | `/notebooks/lint` | Structural quality report |
| `POST` | `/notebooks/clean` | Strip outputs and residue |
| `POST` | `/notebooks/convert` | `py` / `script` / `md` |
| `POST` | `/notebooks/from-py` | Percent Python → notebook |
| `POST` | `/notebooks/concat` | Concatenate notebooks |
| `POST` | `/notebooks/split` | Split on markdown headings |
| `POST` | `/notebooks/filter` | Keep cells by type/tag |
| `POST` | `/notebooks/tag` | Add or remove cell tags |
| `POST` | `/notebooks/ids` | Assign unique cell ids |
| `POST` | `/notebooks/kernel` | Set kernelspec |
| `POST` | `/notebooks/diff` | Cell-level diff |
| `POST` | `/notebooks/execute` | Execute (`nbops[execute]`) |
| `POST` | `/notebooks/new` | Empty nbformat v4 notebook |
| `POST` | `/notebooks/validate` | nbformat schema validation |

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

Runtime settings use the `NBOPS_` prefix and can be placed in a working-directory
`.env` file. See [`.env.example`](./.env.example).

## Layout

```text
src/nbops/
  io.py         load, save, validate, new
  inspect.py    stats, outline, imports, outputs
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

See also [SECURITY.md](./SECURITY.md), [CHANGELOG.md](./CHANGELOG.md), and
[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
