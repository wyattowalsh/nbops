"""Notebook source helpers shared across operations."""

from __future__ import annotations

import ast
import copy
import re
from collections.abc import Mapping
from typing import Any

Notebook = dict[str, Any]

_NON_PYTHON_CELL_MAGICS = frozenset(
    {
        "bash",
        "sh",
        "html",
        "javascript",
        "js",
        "latex",
        "markdown",
        "perl",
        "ruby",
        "script",
        "svg",
        "sql",
    }
)
_PYTHON_LANGUAGES = frozenset({"python", "ipython"})
_KERNEL_NAME_LANGUAGES = {
    "ir": "r",
    "rust": "rust",
    "octave": "octave",
}
_CELL_MAGIC = re.compile(r"^[ \t]*%%([A-Za-z_][A-Za-z0-9_]*)")
_LINE_ESCAPE = re.compile(r"^[ \t]*(?:%{1,3}[A-Za-z_][A-Za-z0-9_]*|!|\?)")
_TRAILING_HELP = re.compile(r"^[ \t]*\S+\?\s*$")
_ASSIGN_MAGIC = re.compile(
    r"^([ \t]*[A-Za-z_][A-Za-z0-9_]*[ \t]*=[ \t]*)%{1,3}[A-Za-z_][A-Za-z0-9_]*[ \t]*(.*)$"
)


def as_notebook_dict(notebook: Mapping[str, Any] | Notebook) -> Notebook:
    """Return a JSON-safe deep copy of a notebook mapping."""
    return copy.deepcopy(dict(notebook))


def cell_source(cell: Mapping[str, Any]) -> str:
    """Normalize a cell ``source`` (str or list[str]) into one string."""
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    if isinstance(source, str):
        return source
    return ""


def source_lines(cell: Mapping[str, Any]) -> list[str]:
    """Return individual source lines without trailing newlines stripped from blanks."""
    return cell_source(cell).splitlines()


def non_empty_line_count(cell: Mapping[str, Any]) -> int:
    """Count non-empty, non-whitespace source lines."""
    return sum(1 for line in source_lines(cell) if line.strip())


def is_empty_cell(cell: Mapping[str, Any]) -> bool:
    """Return True when a cell has no meaningful source."""
    return not cell_source(cell).strip()


def as_mapping(value: Any) -> dict[str, Any]:
    """Return ``value`` if it is a dict, otherwise an empty dict."""
    return dict(value) if isinstance(value, dict) else {}


def nested_mapping(mapping: Any, key: str) -> dict[str, Any]:
    """Return ``mapping[key]`` when both are dicts, otherwise ``{}``."""
    return as_mapping(as_mapping(mapping).get(key))


def cells_of(notebook: Mapping[str, Any]) -> list[Any]:
    """Return the cells list, or an empty list when missing/invalid."""
    cells = notebook.get("cells") if isinstance(notebook, Mapping) else None
    if isinstance(cells, list):
        return cells
    return []


def cell_tags(cell: Mapping[str, Any]) -> list[str]:
    """Return cell tags from metadata, if present."""
    metadata = cell.get("metadata")
    if not isinstance(metadata, dict):
        return []
    tags = metadata.get("tags")
    if isinstance(tags, list):
        return [str(tag) for tag in tags]
    return []


def preview(text: str, limit: int = 80) -> str:
    """Collapse whitespace and truncate for diffs and logs."""
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1] + "…"


def _language_from_kernelspec_name(name: Any) -> str | None:
    """Infer a language id from a kernelspec name when language fields are omitted."""
    if not isinstance(name, str) or not name.strip():
        return None
    lowered = name.strip().lower()
    if lowered in _PYTHON_LANGUAGES or lowered.startswith(("python", "ipython", "pypy")):
        return "python"
    if lowered.startswith("julia"):
        return "julia"
    return _KERNEL_NAME_LANGUAGES.get(lowered)


def declared_code_language(notebook: Mapping[str, Any]) -> str | None:
    """Return a normalized code language, or ``None`` when unspecified.

    ``language_info.name`` and ``kernelspec.language`` win. When those are
    omitted, well-known kernelspec names such as ``python3``, ``ir``, and
    ``julia-1.10`` are inferred. Unknown or missing names stay unspecified so
    the original stats scaffold still counts as Python.
    """
    metadata = as_mapping(notebook.get("metadata"))
    language_info = nested_mapping(metadata, "language_info")
    kernelspec = nested_mapping(metadata, "kernelspec")
    declared = language_info.get("name") or kernelspec.get("language")
    if isinstance(declared, str) and declared.strip():
        name = declared.strip().lower()
        return "python" if name in _PYTHON_LANGUAGES else name
    return _language_from_kernelspec_name(kernelspec.get("name"))


def is_python_notebook(notebook: Mapping[str, Any]) -> bool:
    """Return whether the notebook declares a Python (or IPython) language.

    Missing language metadata is treated as Python so the original stats
    scaffold and incomplete kernelspecs keep the historical lint/import
    behavior. Declared non-Python languages such as ``r`` skip Python AST.
    """
    language = declared_code_language(notebook)
    return language is None or language == "python"


def notebook_code_language(notebook: Mapping[str, Any]) -> str:
    """Return a Markdown fence language id for the notebook."""
    return declared_code_language(notebook) or "python"


def strip_ipython_magics(source: str) -> str | None:
    """Return cell source with IPython magics removed, or ``None`` if not Python.

    Non-Python cell magics such as ``%%bash`` return ``None`` so callers can skip
    syntax checks and import extraction. Line magics, shell bangs, and help
    suffixes are dropped; assignment magics keep the left-hand side.
    """
    lines = source.splitlines()
    for line in lines:
        if not line.strip():
            continue
        match = _CELL_MAGIC.match(line)
        if match is not None and match.group(1).lower() in _NON_PYTHON_CELL_MAGICS:
            return None
        break
    kept: list[str] = []
    for line in lines:
        if not line.strip():
            kept.append(line)
            continue
        if _CELL_MAGIC.match(line) or _LINE_ESCAPE.match(line) or _TRAILING_HELP.match(line):
            continue
        assigned = _ASSIGN_MAGIC.match(line)
        if assigned is not None:
            rhs = assigned.group(2)
            kept.append(f"{assigned.group(1)}{rhs if rhs.strip() else '...'}")
            continue
        kept.append(line)
    return "\n".join(kept)


def parse_code_cell(source: str) -> ast.Module | None:
    """Parse a notebook code cell as Python.

    Returns ``None`` when the cell is a non-Python cell magic. Invalid Python
    raises :class:`SyntaxError`. On Python 3.12+, ``ast.parse`` already accepts
    top-level ``await``.
    """
    cleaned = strip_ipython_magics(source)
    if cleaned is None:
        return None
    if not cleaned.strip():
        return ast.parse("")
    return ast.parse(cleaned)
