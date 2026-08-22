"""Transform notebooks: filter, concat, split, kernel, tags, cell ids."""

from __future__ import annotations

import re
import uuid
from typing import TYPE_CHECKING, Any

from nbops.cells import as_notebook_dict, cell_source, cell_tags, cells_of
from nbops.io import new_notebook

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Mapping, Sequence

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def filter_cells(
    notebook: Mapping[str, Any],
    *,
    cell_types: Sequence[str] | None = None,
    tags: Sequence[str] | None = None,
    predicate: Callable[[dict[str, Any]], bool] | None = None,
) -> dict[str, Any]:
    """Return a copy keeping cells that match all provided filters."""
    wanted_types = set(cell_types) if cell_types is not None else None
    wanted_tags = set(tags) if tags is not None else None
    filtered = as_notebook_dict(notebook)
    kept: list[Any] = []
    for cell in cells_of(filtered):
        if not isinstance(cell, dict):
            continue
        if wanted_types is not None and cell.get("cell_type") not in wanted_types:
            continue
        if wanted_tags is not None and wanted_tags.isdisjoint(cell_tags(cell)):
            continue
        if predicate is not None and not predicate(cell):
            continue
        kept.append(cell)
    filtered["cells"] = kept
    return filtered


def concat_notebooks(notebooks: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Concatenate cells from one or more notebooks.

    Metadata and nbformat version come from the first notebook. Later notebooks
    contribute cells only.
    """
    items = [as_notebook_dict(notebook) for notebook in notebooks]
    if not items:
        return new_notebook()
    merged = items[0]
    cells: list[Any] = list(cells_of(merged))
    for extra in items[1:]:
        cells.extend(cells_of(extra))
    merged["cells"] = cells
    return merged


def split_by_headings(
    notebook: Mapping[str, Any],
    *,
    level: int = 1,
) -> list[tuple[str, dict[str, Any]]]:
    """Split a notebook on markdown headings of ``level``.

    Cells before the first matching heading are returned as ``("preamble", ...)``
    when present.
    """
    if level < 1 or level > 6:
        raise ValueError("Heading level must be between 1 and 6.")
    prefix = "#" * level
    template = as_notebook_dict(notebook)
    template["cells"] = []
    sections: list[tuple[str, dict[str, Any]]] = []
    current_title = "preamble"
    current_cells: list[Any] = []

    def flush() -> None:
        if not current_cells and current_title == "preamble":
            return
        section = as_notebook_dict(template)
        section["cells"] = list(current_cells)
        sections.append((current_title, section))

    for cell in cells_of(notebook):
        if isinstance(cell, dict) and cell.get("cell_type") == "markdown":
            heading = _first_heading(cell_source(cell), prefix)
            if heading is not None:
                flush()
                current_title = heading
                current_cells = [as_notebook_dict(cell)]
                continue
        current_cells.append(as_notebook_dict(cell) if isinstance(cell, dict) else cell)
    flush()
    return sections


def set_kernelspec(
    notebook: Mapping[str, Any],
    *,
    name: str,
    display_name: str | None = None,
    language: str | None = None,
) -> dict[str, Any]:
    """Return a copy with kernelspec and language_info updated."""
    updated = as_notebook_dict(notebook)
    metadata = updated.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    kernelspec = metadata.get("kernelspec")
    if not isinstance(kernelspec, dict):
        kernelspec = {}
    kernelspec["name"] = name
    if display_name is not None:
        kernelspec["display_name"] = display_name
    if language is not None:
        kernelspec["language"] = language
        language_info = metadata.get("language_info")
        if not isinstance(language_info, dict):
            language_info = {}
        language_info["name"] = language
        metadata["language_info"] = language_info
    metadata["kernelspec"] = kernelspec
    updated["metadata"] = metadata
    return updated


def ensure_cell_ids(notebook: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy with unique cell ids assigned where missing or duplicated."""
    updated = as_notebook_dict(notebook)
    seen: set[str] = set()
    for cell in cells_of(updated):
        if not isinstance(cell, dict):
            continue
        cell_id = cell.get("id")
        if not isinstance(cell_id, str) or not cell_id or cell_id in seen:
            cell_id = uuid.uuid4().hex[:12]
            while cell_id in seen:
                cell_id = uuid.uuid4().hex[:12]
            cell["id"] = cell_id
        seen.add(cell_id)
    return updated


def add_tags(notebook: Mapping[str, Any], cell_index: int, tags: Sequence[str]) -> dict[str, Any]:
    """Return a copy with ``tags`` added to ``cell_index``."""
    updated = as_notebook_dict(notebook)
    cells = cells_of(updated)
    if cell_index < 0 or cell_index >= len(cells):
        raise IndexError(f"Cell index {cell_index} is out of range.")
    cell = cells[cell_index]
    if not isinstance(cell, dict):
        raise TypeError("Target cell is not a mapping.")
    metadata = cell.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    existing = (
        [str(tag) for tag in metadata.get("tags", [])]
        if isinstance(metadata.get("tags"), list)
        else []
    )
    merged = list(dict.fromkeys([*existing, *tags]))
    metadata["tags"] = merged
    cell["metadata"] = metadata
    cells[cell_index] = cell
    updated["cells"] = cells
    return updated


def _first_heading(source: str, prefix: str) -> str | None:
    for line in source.splitlines():
        stripped = line.strip()
        match = _HEADING_RE.match(stripped)
        if match is None:
            continue
        if match.group(1) == prefix:
            return match.group(2).strip()
        return None
    return None
