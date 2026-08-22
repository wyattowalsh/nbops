"""Convert notebooks to percent-format Python, scripts, and Markdown."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from nbops.cells import cell_source, cells_of
from nbops.models import ConvertResult


def to_percent_python(notebook: Mapping[str, Any]) -> str:
    """Render a notebook as a Jupytext-style percent script."""
    chunks: list[str] = []
    for cell in cells_of(notebook):
        if not isinstance(cell, dict):
            continue
        cell_type = cell.get("cell_type")
        source = cell_source(cell).rstrip()
        if cell_type == "markdown":
            quoted = "\n".join(f"# {line}" if line else "#" for line in source.splitlines()) or "#"
            chunks.append(f"# %% [markdown]\n{quoted}")
        elif cell_type == "raw":
            quoted = "\n".join(f"# {line}" if line else "#" for line in source.splitlines()) or "#"
            chunks.append(f"# %% [raw]\n{quoted}")
        else:
            chunks.append(f"# %%\n{source}")
    text = "\n\n".join(chunks).rstrip() + "\n"
    return text if chunks else ""


def to_script(notebook: Mapping[str, Any]) -> str:
    """Render only code cells as a plain Python script."""
    chunks: list[str] = []
    for cell in cells_of(notebook):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = cell_source(cell).rstrip()
        if source:
            chunks.append(source)
    return ("\n\n".join(chunks).rstrip() + "\n") if chunks else ""


def to_markdown(notebook: Mapping[str, Any]) -> str:
    """Render a notebook as Markdown with fenced Python code cells."""
    chunks: list[str] = []
    for cell in cells_of(notebook):
        if not isinstance(cell, dict):
            continue
        cell_type = cell.get("cell_type")
        source = cell_source(cell).rstrip()
        if cell_type == "markdown" or cell_type == "raw":
            if source:
                chunks.append(source)
        else:
            chunks.append(f"```python\n{source}\n```" if source else "```python\n```")
    return ("\n\n".join(chunks).rstrip() + "\n") if chunks else ""


def convert_notebook(notebook: Mapping[str, Any], fmt: str) -> ConvertResult:
    """Convert a notebook to ``py``, ``script``, or ``md``."""
    normalized = fmt.lower().strip()
    if normalized in {"py", "percent"}:
        return ConvertResult(format="py", text=to_percent_python(notebook))
    if normalized in {"script", "python"}:
        return ConvertResult(format="script", text=to_script(notebook))
    if normalized in {"md", "markdown"}:
        return ConvertResult(format="md", text=to_markdown(notebook))
    raise ValueError(f"Unsupported conversion format: {fmt}")
