"""Core notebook-analysis logic for nbops.

This module is intentionally dependency-light: it parses the standard Jupyter
notebook JSON format (nbformat v4) and derives useful, deterministic statistics.
Keeping the logic pure (no I/O) makes it trivial to unit test and reuse from both
the CLI and the HTTP API.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class NotebookStats(BaseModel):
    """Deterministic summary of a Jupyter notebook."""

    total_cells: int = Field(..., ge=0, description="Total number of cells.")
    code_cells: int = Field(..., ge=0, description="Number of code cells.")
    markdown_cells: int = Field(..., ge=0, description="Number of markdown cells.")
    raw_cells: int = Field(..., ge=0, description="Number of raw cells.")
    code_lines: int = Field(..., ge=0, description="Total non-empty lines of code.")
    kernel: str | None = Field(None, description="Kernel display name, if declared.")
    language: str | None = Field(None, description="Notebook language, if declared.")


def _source_to_lines(source: Any) -> list[str]:
    """Normalize a cell ``source`` (str or list[str]) into individual lines."""
    if isinstance(source, list):
        text = "".join(source)
    elif isinstance(source, str):
        text = source
    else:
        return []
    return text.splitlines()


def compute_stats(notebook: dict[str, Any]) -> NotebookStats:
    """Compute :class:`NotebookStats` from an in-memory notebook mapping.

    Args:
        notebook: A parsed notebook document (nbformat v4 shape).

    Returns:
        A populated :class:`NotebookStats` instance.

    Raises:
        ValueError: If ``notebook`` is not a mapping with a ``cells`` list.
    """
    if not isinstance(notebook, dict) or not isinstance(notebook.get("cells"), list):
        raise ValueError("Invalid notebook: expected a mapping with a 'cells' list.")

    cells = notebook["cells"]
    code_cells = markdown_cells = raw_cells = code_lines = 0

    for cell in cells:
        if not isinstance(cell, dict):
            continue
        cell_type = cell.get("cell_type")
        if cell_type == "code":
            code_cells += 1
            code_lines += sum(1 for line in _source_to_lines(cell.get("source")) if line.strip())
        elif cell_type == "markdown":
            markdown_cells += 1
        elif cell_type == "raw":
            raw_cells += 1

    raw_metadata = notebook.get("metadata")
    metadata = raw_metadata if isinstance(raw_metadata, dict) else {}
    raw_kernelspec = metadata.get("kernelspec")
    kernelspec = raw_kernelspec if isinstance(raw_kernelspec, dict) else {}
    raw_language_info = metadata.get("language_info")
    language_info = raw_language_info if isinstance(raw_language_info, dict) else {}

    return NotebookStats(
        total_cells=len(cells),
        code_cells=code_cells,
        markdown_cells=markdown_cells,
        raw_cells=raw_cells,
        code_lines=code_lines,
        kernel=kernelspec.get("display_name"),
        language=language_info.get("name") or kernelspec.get("language"),
    )


def load_notebook(path: str | Path) -> dict[str, Any]:
    """Read and parse a notebook file from disk.

    Args:
        path: Path to a ``.ipynb`` file.

    Returns:
        The parsed notebook document.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        ValueError: If the file does not contain valid JSON.
    """
    notebook_path = Path(path)
    if not notebook_path.is_file():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")
    try:
        return json.loads(notebook_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - exercised via CLI tests
        raise ValueError(f"Not a valid JSON notebook: {notebook_path} ({exc})") from exc


def stats_for_file(path: str | Path) -> NotebookStats:
    """Convenience helper: load a notebook file and compute its stats."""
    return compute_stats(load_notebook(path))
