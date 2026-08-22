"""Clean notebook residue: outputs, execution counts, ids, empty cells."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from nbops.cells import as_notebook_dict, is_empty_cell
from nbops.models import CleanOptions

if TYPE_CHECKING:
    from collections.abc import Mapping

_OUTPUT_RESET_METADATA = ("collapsed", "scrolled", "ExecuteTime")


def clean_notebook(
    notebook: Mapping[str, Any],
    options: CleanOptions | None = None,
) -> dict[str, Any]:
    """Return a cleaned copy of ``notebook`` without mutating the input."""
    opts = options or CleanOptions()
    cleaned = as_notebook_dict(notebook)
    cells = cleaned.get("cells")
    if not isinstance(cells, list):
        raise ValueError("Invalid notebook: expected a mapping with a 'cells' list.")

    kept: list[Any] = []
    for cell in cells:
        if not isinstance(cell, dict):
            kept.append(cell)
            continue
        if opts.empty_cells and is_empty_cell(cell):
            continue
        if cell.get("cell_type") == "code":
            if opts.outputs:
                cell["outputs"] = []
            if opts.execution_counts:
                cell["execution_count"] = None
        metadata = cell.get("metadata")
        if isinstance(metadata, dict):
            if opts.outputs:
                for key in _OUTPUT_RESET_METADATA:
                    metadata.pop(key, None)
            for key in opts.metadata_keys:
                metadata.pop(key, None)
            cell["metadata"] = metadata
        if opts.cell_ids:
            cell.pop("id", None)
        kept.append(cell)
    cleaned["cells"] = kept
    if opts.outputs:
        notebook_metadata = cleaned.get("metadata")
        if isinstance(notebook_metadata, dict):
            notebook_metadata.pop("widgets", None)
            cleaned["metadata"] = notebook_metadata
    return cleaned
