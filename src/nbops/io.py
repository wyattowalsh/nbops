"""Load, save, validate, and construct Jupyter notebooks."""

from __future__ import annotations

import copy
import json
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any

import nbformat
from nbformat.validator import MissingIDFieldWarning, NotebookValidationError

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
    """Parse a notebook from JSON text, bytes, or a mapping.

    Cell ids are preserved as stored. ``nbformat`` must not silently insert ids
    here: lint ``NB009`` and ``clean --strip-ids`` depend on omitted ids surviving
    a load/save roundtrip.
    """
    notebook = _mapping_from_document(document)
    notebook = _maybe_upgrade_legacy(notebook)
    if validate:
        validate_notebook(notebook)
    return notebook


def validate_notebook(notebook: dict[str, Any] | Any) -> None:
    """Validate a notebook against the nbformat schema."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", MissingIDFieldWarning)
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
        raw = notebook_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise InvalidNotebookError(f"Not a valid JSON notebook: {notebook_path} ({exc})") from exc
    try:
        notebook = _mapping_from_document(raw)
    except InvalidNotebookError as exc:
        raise InvalidNotebookError(f"Not a valid JSON notebook: {notebook_path} ({exc})") from exc
    notebook = _maybe_upgrade_legacy(notebook)
    if validate:
        validate_notebook(notebook)
    return notebook


def save_notebook(
    notebook: dict[str, Any],
    path: str | Path,
    *,
    validate: bool = True,
) -> Path:
    """Write a notebook mapping to disk as nbformat JSON."""
    notebook_path = Path(path)
    notebook_path.parent.mkdir(parents=True, exist_ok=True)
    notebook_path.write_text(dumps_notebook(notebook, validate=validate), encoding="utf-8")
    return notebook_path


def dumps_notebook(notebook: dict[str, Any], *, validate: bool = False) -> str:
    """Serialize a notebook mapping to a JSON string without inserting cell ids."""
    if validate:
        validate_notebook(notebook)
    try:
        return json.dumps(notebook, indent=1, ensure_ascii=False) + "\n"
    except (TypeError, ValueError) as exc:
        raise InvalidNotebookError(f"Notebook is not JSON-serializable: {exc}") from exc


def _mapping_from_document(document: str | bytes | dict[str, Any]) -> dict[str, Any]:
    if isinstance(document, dict):
        return copy.deepcopy(document)
    if isinstance(document, bytes):
        try:
            raw = document.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise InvalidNotebookError(f"Not a valid notebook document: {exc}") from exc
    else:
        raw = document
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InvalidNotebookError(f"Not a valid notebook document: {exc}") from exc
    if not isinstance(parsed, dict):
        raise InvalidNotebookError("Not a valid notebook document: expected a mapping.")
    return parsed


def _maybe_upgrade_legacy(notebook: dict[str, Any]) -> dict[str, Any]:
    """Convert pre-v4 documents to nbformat 4. v4+ mappings are returned as-is."""
    major = notebook.get("nbformat")
    if not isinstance(major, int) or major >= DEFAULT_NBFORMAT:
        return notebook
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", MissingIDFieldWarning)
            node = nbformat.reads(json.dumps(notebook), as_version=DEFAULT_NBFORMAT)
            upgraded = json.loads(nbformat.writes(node))
    except Exception as exc:
        raise InvalidNotebookError(f"Not a valid notebook document: {exc}") from exc
    if not isinstance(upgraded, dict):
        raise InvalidNotebookError("Not a valid notebook document: expected a mapping.")
    return upgraded
