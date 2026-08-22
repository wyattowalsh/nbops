"""Typed report models for notebook operations."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version
from typing import Any, Literal

from pydantic import BaseModel, Field

try:
    _NBOPS_VERSION = package_version("nbops")
except PackageNotFoundError:  # pragma: no cover - only during local, uninstalled use
    _NBOPS_VERSION = "0.0.0.dev0"


class NotebookStats(BaseModel):
    """Deterministic summary of a Jupyter notebook."""

    total_cells: int = Field(..., ge=0, description="Total number of cells.")
    code_cells: int = Field(..., ge=0, description="Number of code cells.")
    markdown_cells: int = Field(..., ge=0, description="Number of markdown cells.")
    raw_cells: int = Field(..., ge=0, description="Number of raw cells.")
    code_lines: int = Field(..., ge=0, description="Total non-empty lines of code.")
    markdown_lines: int = Field(0, ge=0, description="Total non-empty markdown lines.")
    empty_cells: int = Field(0, ge=0, description="Cells with no source and no attachments.")
    executed_code_cells: int = Field(
        0, ge=0, description="Code cells with a non-null execution count."
    )
    error_outputs: int = Field(0, ge=0, description="Outputs with output_type error.")
    stream_outputs: int = Field(0, ge=0, description="Stream outputs.")
    display_outputs: int = Field(0, ge=0, description="Display or execute-result outputs.")
    kernel: str | None = Field(None, description="Kernel display name, if declared.")
    kernel_name: str | None = Field(None, description="Kernel name, if declared.")
    language: str | None = Field(None, description="Notebook language, if declared.")
    nbformat_major: int | None = Field(None, description="nbformat major version.")
    nbformat_minor: int | None = Field(None, description="nbformat minor version.")
    has_widgets: bool = Field(False, description="Whether widget metadata is present.")
    tags: list[str] = Field(default_factory=list, description="Sorted unique cell tags.")
    attachment_cells: int = Field(0, ge=0, description="Cells that have one or more attachments.")
    attachment_files: int = Field(0, ge=0, description="Total attached files across all cells.")


class Heading(BaseModel):
    """A markdown heading extracted from a notebook."""

    level: int = Field(..., ge=1, le=6)
    title: str
    cell_index: int = Field(..., ge=0)


class ImportRecord(BaseModel):
    """A top-level import found in a code cell."""

    module: str
    names: list[str] = Field(default_factory=list)
    cell_index: int = Field(..., ge=0)
    raw: str


class OutputRecord(BaseModel):
    """One code-cell output from a notebook."""

    cell_index: int = Field(..., ge=0)
    output_index: int = Field(..., ge=0)
    output_type: str
    name: str | None = None
    preview: str | None = None
    size: int = Field(0, ge=0)


class AttachmentRecord(BaseModel):
    """One nbformat cell attachment."""

    cell_index: int = Field(..., ge=0)
    filename: str
    mime_types: list[str] = Field(default_factory=list)
    size: int = Field(0, ge=0)


class ValidateResponse(BaseModel):
    """Result of nbformat schema validation."""

    valid: bool
    error: str | None = None


class LintIssue(BaseModel):
    """A single structural or quality finding."""

    code: str
    severity: Literal["error", "warning", "info"]
    message: str
    cell_index: int | None = None


class LintReport(BaseModel):
    """Aggregated lint findings for one notebook."""

    issue_count: int = Field(..., ge=0)
    error_count: int = Field(..., ge=0)
    warning_count: int = Field(..., ge=0)
    passed: bool
    issues: list[LintIssue] = Field(default_factory=list)


class CleanOptions(BaseModel):
    """Options controlling which notebook residue to strip."""

    outputs: bool = True
    execution_counts: bool = True
    cell_ids: bool = False
    empty_cells: bool = False
    metadata_keys: list[str] = Field(default_factory=list)


class CellDiff(BaseModel):
    """One cell-level difference between two notebooks."""

    index: int = Field(..., ge=0)
    change: Literal["equal", "added", "removed", "changed"]
    left_type: str | None = None
    right_type: str | None = None
    left_preview: str | None = None
    right_preview: str | None = None


class NotebookDiff(BaseModel):
    """Structural diff of two notebooks."""

    left_cells: int = Field(..., ge=0)
    right_cells: int = Field(..., ge=0)
    equal: int = Field(..., ge=0)
    changed: int = Field(..., ge=0)
    added: int = Field(..., ge=0)
    removed: int = Field(..., ge=0)
    identical: bool
    cells: list[CellDiff] = Field(default_factory=list)


class ConvertResult(BaseModel):
    """Text conversion of a notebook."""

    format: Literal["py", "md", "script"]
    text: str


class BatchItem[T](BaseModel):
    """One result from a directory batch operation."""

    path: str
    ok: bool
    result: T | None = None
    error: str | None = None


class HealthResponse(BaseModel):
    """Liveness payload matching the original stats-scaffold defaults."""

    status: str = "ok"
    version: str = _NBOPS_VERSION


class NotebookPayload(BaseModel):
    """Request body carrying a raw notebook document."""

    notebook: dict[str, Any] = Field(..., description="A parsed Jupyter notebook document.")
