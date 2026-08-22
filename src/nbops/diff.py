"""Structural cell-level diffs for notebooks."""

from __future__ import annotations

from collections.abc import Mapping
from difflib import SequenceMatcher

from nbops.cells import cell_source, cells_of, preview
from nbops.models import CellDiff, NotebookDiff


def diff_notebooks(left: Mapping[str, object], right: Mapping[str, object]) -> NotebookDiff:
    """Diff two notebooks by cell type and source using sequence matching."""
    left_cells = [_signature(cell) for cell in cells_of(left)]
    right_cells = [_signature(cell) for cell in cells_of(right)]
    matcher = SequenceMatcher(a=left_cells, b=right_cells, autojunk=False)
    results: list[CellDiff] = []
    equal = changed = added = removed = 0
    emit_index = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for offset in range(i2 - i1):
                results.append(
                    CellDiff(
                        index=emit_index + offset,
                        change="equal",
                        left_type=left_cells[i1 + offset][0],
                        right_type=right_cells[j1 + offset][0],
                    )
                )
            equal += i2 - i1
            emit_index += i2 - i1
        elif tag == "replace":
            span = max(i2 - i1, j2 - j1)
            for offset in range(span):
                left_sig = left_cells[i1 + offset] if i1 + offset < i2 else None
                right_sig = right_cells[j1 + offset] if j1 + offset < j2 else None
                if left_sig is None:
                    added += 1
                    change = "added"
                elif right_sig is None:
                    removed += 1
                    change = "removed"
                else:
                    changed += 1
                    change = "changed"
                results.append(
                    CellDiff(
                        index=emit_index + offset,
                        change=change,
                        left_type=None if left_sig is None else left_sig[0],
                        right_type=None if right_sig is None else right_sig[0],
                        left_preview=None if left_sig is None else preview(left_sig[1]),
                        right_preview=None if right_sig is None else preview(right_sig[1]),
                    )
                )
            emit_index += span
        elif tag == "delete":
            for offset in range(i2 - i1):
                sig = left_cells[i1 + offset]
                results.append(
                    CellDiff(
                        index=emit_index + offset,
                        change="removed",
                        left_type=sig[0],
                        left_preview=preview(sig[1]),
                    )
                )
            removed += i2 - i1
            emit_index += i2 - i1
        elif tag == "insert":
            for offset in range(j2 - j1):
                sig = right_cells[j1 + offset]
                results.append(
                    CellDiff(
                        index=emit_index + offset,
                        change="added",
                        right_type=sig[0],
                        right_preview=preview(sig[1]),
                    )
                )
            added += j2 - j1
            emit_index += j2 - j1

    return NotebookDiff(
        left_cells=len(left_cells),
        right_cells=len(right_cells),
        equal=equal,
        changed=changed,
        added=added,
        removed=removed,
        identical=changed == 0 and added == 0 and removed == 0,
        cells=results,
    )


def _signature(cell: object) -> tuple[str, str]:
    if not isinstance(cell, dict):
        return ("unknown", "")
    return (str(cell.get("cell_type") or "unknown"), cell_source(cell))
