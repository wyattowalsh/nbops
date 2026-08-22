"""Inspect notebooks: statistics, outlines, imports, and outputs."""

from __future__ import annotations

import ast
import re
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from nbops.cells import (
    as_mapping,
    cell_source,
    cell_tags,
    cells_of,
    declared_code_language,
    is_empty_cell,
    is_python_notebook,
    nested_mapping,
    non_empty_line_count,
    parse_code_cell,
    preview,
)
from nbops.io import load_notebook
from nbops.models import Heading, ImportRecord, NotebookStats, OutputRecord

if TYPE_CHECKING:
    from pathlib import Path

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def compute_stats(notebook: Mapping[str, Any] | Any) -> NotebookStats:
    """Compute :class:`NotebookStats` from an in-memory notebook mapping.

    This function is intentionally lenient so callers can inspect incomplete
    documents. Strict schema validation belongs in :func:`nbops.io.validate_notebook`
    or :func:`nbops.io.load_notebook` with ``validate=True``.
    """
    if not isinstance(notebook, Mapping) or not isinstance(notebook.get("cells"), list):
        raise ValueError("Invalid notebook: expected a mapping with a 'cells' list.")

    cells = cells_of(notebook)
    code_cells = markdown_cells = raw_cells = 0
    code_lines = markdown_lines = empty_cells = 0
    executed_code_cells = error_outputs = stream_outputs = display_outputs = 0
    tags: set[str] = set()

    for cell in cells:
        if not isinstance(cell, dict):
            continue
        if is_empty_cell(cell):
            empty_cells += 1
        tags.update(cell_tags(cell))
        cell_type = cell.get("cell_type")
        if cell_type == "code":
            code_cells += 1
            code_lines += non_empty_line_count(cell)
            if cell.get("execution_count") is not None:
                executed_code_cells += 1
            for output in cell.get("outputs") or []:
                if not isinstance(output, dict):
                    continue
                output_type = output.get("output_type")
                if output_type == "error":
                    error_outputs += 1
                elif output_type == "stream":
                    stream_outputs += 1
                elif output_type in {"display_data", "execute_result"}:
                    display_outputs += 1
        elif cell_type == "markdown":
            markdown_cells += 1
            markdown_lines += non_empty_line_count(cell)
        elif cell_type == "raw":
            raw_cells += 1

    metadata = as_mapping(notebook.get("metadata"))
    kernelspec = nested_mapping(metadata, "kernelspec")
    widgets = metadata.get("widgets")
    has_widgets = isinstance(widgets, dict) and bool(widgets)

    major = notebook.get("nbformat")
    minor = notebook.get("nbformat_minor")

    return NotebookStats(
        total_cells=len(cells),
        code_cells=code_cells,
        markdown_cells=markdown_cells,
        raw_cells=raw_cells,
        code_lines=code_lines,
        markdown_lines=markdown_lines,
        empty_cells=empty_cells,
        executed_code_cells=executed_code_cells,
        error_outputs=error_outputs,
        stream_outputs=stream_outputs,
        display_outputs=display_outputs,
        kernel=kernelspec.get("display_name"),
        kernel_name=kernelspec.get("name"),
        language=declared_code_language(notebook),
        nbformat_major=major if isinstance(major, int) else None,
        nbformat_minor=minor if isinstance(minor, int) else None,
        has_widgets=has_widgets,
        tags=sorted(tags),
    )


def outline(notebook: Mapping[str, Any]) -> list[Heading]:
    """Extract markdown headings in document order."""
    headings: list[Heading] = []
    for index, cell in enumerate(cells_of(notebook)):
        if not isinstance(cell, dict) or cell.get("cell_type") != "markdown":
            continue
        for line in cell_source(cell).splitlines():
            match = _HEADING_RE.match(line.strip())
            if match is None:
                continue
            headings.append(
                Heading(level=len(match.group(1)), title=match.group(2).strip(), cell_index=index)
            )
    return headings


def extract_imports(notebook: Mapping[str, Any]) -> list[ImportRecord]:
    """Extract top-level import statements from code cells."""
    if not is_python_notebook(notebook):
        return []
    records: list[ImportRecord] = []
    for index, cell in enumerate(cells_of(notebook)):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = cell_source(cell)
        try:
            tree = parse_code_cell(source)
        except SyntaxError:
            continue
        if tree is None:
            continue
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    records.append(
                        ImportRecord(
                            module=alias.name,
                            names=[alias.asname or alias.name],
                            cell_index=index,
                            raw=ast.unparse(node),
                        )
                    )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [alias.asname or alias.name for alias in node.names]
                records.append(
                    ImportRecord(
                        module=module,
                        names=names,
                        cell_index=index,
                        raw=ast.unparse(node),
                    )
                )
    return records


def list_outputs(notebook: Mapping[str, Any]) -> list[OutputRecord]:
    """Inventory code-cell outputs in document order."""
    records: list[OutputRecord] = []
    for cell_index, cell in enumerate(cells_of(notebook)):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        outputs = cell.get("outputs")
        if not isinstance(outputs, list):
            continue
        for output_index, output in enumerate(outputs):
            if not isinstance(output, dict):
                continue
            output_type = str(output.get("output_type") or "unknown")
            name = _output_name(output, output_type)
            text = _output_text(output, output_type)
            records.append(
                OutputRecord(
                    cell_index=cell_index,
                    output_index=output_index,
                    output_type=output_type,
                    name=name,
                    preview=preview(text) if text else None,
                    size=len(text),
                )
            )
    return records


def stats_for_file(path: str | Path, *, validate: bool = False) -> NotebookStats:
    """Load a notebook file and compute its stats."""
    return compute_stats(load_notebook(path, validate=validate))


def _output_name(output: Mapping[str, Any], output_type: str) -> str | None:
    if output_type == "stream":
        name = output.get("name")
        return str(name) if name else "stdout"
    if output_type == "error":
        ename = output.get("ename")
        return str(ename) if ename else "error"
    return None


def _output_text(output: Mapping[str, Any], output_type: str) -> str:
    if output_type == "error":
        evalue = output.get("evalue")
        traceback = output.get("traceback")
        parts: list[str] = []
        if evalue:
            parts.append(str(evalue))
        if isinstance(traceback, list):
            parts.extend(str(line) for line in traceback)
        return "\n".join(parts)
    text = output.get("text")
    if isinstance(text, list):
        return "".join(str(part) for part in text)
    if isinstance(text, str):
        return text
    data = output.get("data")
    if isinstance(data, dict):
        for key in ("text/plain", "text/html"):
            value = data.get(key)
            if isinstance(value, list):
                return "".join(str(part) for part in value)
            if isinstance(value, str):
                return value
        return " ".join(str(value) for value in data.values())
    return ""
