"""Load, save, validate, and construct Jupyter notebooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import nbformat
from nbformat.validator import NotebookValidationError

from nbops.exceptions import InvalidNotebookError, NotebookNotFoundError

if TYPE_CHECKING:
    from nbops.cells import Notebook

DEFAULT_NBFORMAT = 4
DEFAULT_NBFORMAT_MINOR = 5


def new_notebook(
    *,
    kernel_name: str = "python3",
    display_name: str = "Python 3",
    language: str = "python",
) -> Notebook:
    """Create an empty nbformat v4 notebook with a kernelspec."""
    notebook = nbformat.v4.new_notebook()
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": display_name,
            "language": language,
            "name": kernel_name,
        },
        "language_info": {"name": language},
    }
    return json.loads(nbformat.writes(notebook))


def parse_notebook(document: str | bytes | dict[str, Any], *, validate: bool = True) -> Notebook:
    """Parse a notebook from JSON text, bytes, or a mapping."""
    if isinstance(document, dict):
        raw = json.dumps(document)
    elif isinstance(document, bytes):
        raw = document.decode("utf-8")
    else:
        raw = document
    try:
        notebook = nbformat.reads(raw, as_version=DEFAULT_NBFORMAT)
    except Exception as exc:
        raise InvalidNotebookError(f"Not a valid notebook document: {exc}") from exc
    if validate:
        validate_notebook(notebook)
    return json.loads(nbformat.writes(notebook))


def validate_notebook(notebook: dict[str, Any] | Any) -> None:
    """Validate a notebook against the nbformat schema."""
    try:
        node = notebook if hasattr(notebook, "cells") else nbformat.from_dict(notebook)
        nbformat.validate(node)
    except NotebookValidationError as exc:
        raise InvalidNotebookError(f"Notebook failed schema validation: {exc}") from exc
    except Exception as exc:
        raise InvalidNotebookError(f"Notebook failed schema validation: {exc}") from exc


def load_notebook(path: str | Path, *, validate: bool = True) -> Notebook:
    """Read and parse a notebook file from disk."""
    notebook_path = Path(path)
    if not notebook_path.is_file():
        raise NotebookNotFoundError(f"Notebook not found: {notebook_path}")
    try:
        notebook = nbformat.read(notebook_path, as_version=DEFAULT_NBFORMAT)
    except Exception as exc:
        raise InvalidNotebookError(f"Not a valid JSON notebook: {notebook_path} ({exc})") from exc
    if validate:
        validate_notebook(notebook)
    return json.loads(nbformat.writes(notebook))


def save_notebook(
    notebook: dict[str, Any],
    path: str | Path,
    *,
    validate: bool = True,
) -> Path:
    """Write a notebook mapping to disk as nbformat JSON."""
    if validate:
        validate_notebook(notebook)
    notebook_path = Path(path)
    notebook_path.parent.mkdir(parents=True, exist_ok=True)
    node = nbformat.from_dict(notebook)
    nbformat.write(node, notebook_path)
    return notebook_path


def dumps_notebook(notebook: dict[str, Any], *, validate: bool = False) -> str:
    """Serialize a notebook mapping to a JSON string."""
    if validate:
        validate_notebook(notebook)
    return nbformat.writes(nbformat.from_dict(notebook))
