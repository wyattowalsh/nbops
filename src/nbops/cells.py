"""Notebook source helpers shared across operations."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

Notebook = dict[str, Any]


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
