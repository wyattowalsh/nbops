"""Structural lint for Jupyter notebooks."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from nbops.cells import (
    as_mapping,
    cell_source,
    cells_of,
    is_empty_cell,
    is_python_notebook,
    nested_mapping,
    parse_code_cell,
)
from nbops.models import LintIssue, LintReport

DEFAULT_MAX_OUTPUT_CHARS = 100_000

ISSUE_CATALOG: dict[str, tuple[str, str]] = {
    "NB000": ("error", "Document is not a notebook mapping with a cells list."),
    "NB001": ("error", "Notebook has no cells."),
    "NB002": ("warning", "Notebook has no top-level markdown title."),
    "NB003": ("info", "Cell source is empty."),
    "NB004": ("error", "Code cell has an error output."),
    "NB005": ("info", "Code cell has not been executed."),
    "NB006": ("warning", "Code cell outputs exceed the size budget."),
    "NB007": ("error", "Code cell has invalid Python syntax."),
    "NB008": ("warning", "Notebook is missing a kernelspec name."),
    "NB009": ("warning", "Cell is missing an id (nbformat 4.5)."),
    "NB010": ("error", "Duplicate cell id."),
    "NB011": ("error", "Cell is not a mapping."),
}


def lint_notebook(
    notebook: Mapping[str, Any],
    *,
    max_output_chars: int = DEFAULT_MAX_OUTPUT_CHARS,
) -> LintReport:
    """Return structural quality findings for a notebook."""
    issues: list[LintIssue] = []
    cells = cells_of(notebook)
    if not isinstance(notebook, Mapping) or "cells" not in notebook:
        issues.append(
            LintIssue(
                code="NB000",
                severity="error",
                message="Document is not a notebook mapping with a cells list.",
            )
        )
        return _report(issues)

    if len(cells) == 0:
        issues.append(LintIssue(code="NB001", severity="error", message="Notebook has no cells."))

    metadata = as_mapping(notebook.get("metadata"))
    kernelspec = nested_mapping(metadata, "kernelspec")
    if not kernelspec.get("name"):
        issues.append(
            LintIssue(
                code="NB008", severity="warning", message="Notebook is missing a kernelspec name."
            )
        )

    seen_ids: dict[str, int] = {}
    has_title = False
    check_python = is_python_notebook(notebook)
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            issues.append(
                LintIssue(
                    code="NB011",
                    severity="error",
                    message="Cell is not a mapping.",
                    cell_index=index,
                )
            )
            continue
        cell_id = cell.get("id")
        if not isinstance(cell_id, str) or not cell_id:
            issues.append(
                LintIssue(
                    code="NB009",
                    severity="warning",
                    message="Cell is missing an id (nbformat 4.5).",
                    cell_index=index,
                )
            )
        elif cell_id in seen_ids:
            issues.append(
                LintIssue(
                    code="NB010",
                    severity="error",
                    message=(f"Duplicate cell id {cell_id!r} (first seen at {seen_ids[cell_id]})."),
                    cell_index=index,
                )
            )
        else:
            seen_ids[cell_id] = index
        if is_empty_cell(cell):
            issues.append(
                LintIssue(
                    code="NB003",
                    severity="info",
                    message="Cell source is empty.",
                    cell_index=index,
                )
            )
        cell_type = cell.get("cell_type")
        if cell_type == "markdown":
            source = cell_source(cell).lstrip()
            if source.startswith("# "):
                has_title = True
        if cell_type != "code":
            continue
        source = cell_source(cell)
        if source.strip():
            if check_python:
                try:
                    parse_code_cell(source)
                except SyntaxError as exc:
                    issues.append(
                        LintIssue(
                            code="NB007",
                            severity="error",
                            message=f"Code cell has invalid Python syntax: {exc.msg}.",
                            cell_index=index,
                        )
                    )
            if cell.get("execution_count") is None and not _has_outputs(cell):
                issues.append(
                    LintIssue(
                        code="NB005",
                        severity="info",
                        message="Code cell has not been executed.",
                        cell_index=index,
                    )
                )
        output_chars = 0
        for output in cell.get("outputs") or []:
            if not isinstance(output, dict):
                continue
            if output.get("output_type") == "error":
                ename = output.get("ename") or "error"
                issues.append(
                    LintIssue(
                        code="NB004",
                        severity="error",
                        message=f"Code cell has an error output ({ename}).",
                        cell_index=index,
                    )
                )
            output_chars += _output_size(output)
        if output_chars > max_output_chars:
            issues.append(
                LintIssue(
                    code="NB006",
                    severity="warning",
                    message=f"Code cell outputs exceed {max_output_chars} characters.",
                    cell_index=index,
                )
            )

    if cells and not has_title:
        issues.append(
            LintIssue(
                code="NB002",
                severity="warning",
                message="Notebook has no top-level markdown title.",
            )
        )
    return _report(issues)


def _has_outputs(cell: Mapping[str, Any]) -> bool:
    outputs = cell.get("outputs")
    return isinstance(outputs, list) and len(outputs) > 0


def _output_size(output: Mapping[str, Any]) -> int:
    text = output.get("text")
    if isinstance(text, list):
        return sum(len(str(part)) for part in text)
    if isinstance(text, str):
        return len(text)
    data = output.get("data")
    if isinstance(data, dict):
        return sum(len(str(value)) for value in data.values())
    traceback = output.get("traceback")
    if isinstance(traceback, list):
        return sum(len(str(part)) for part in traceback)
    return 0


def _report(issues: list[LintIssue]) -> LintReport:
    error_count = sum(1 for issue in issues if issue.severity == "error")
    warning_count = sum(1 for issue in issues if issue.severity == "warning")
    return LintReport(
        issue_count=len(issues),
        error_count=error_count,
        warning_count=warning_count,
        passed=error_count == 0,
        issues=issues,
    )
