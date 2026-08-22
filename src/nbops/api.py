"""FastAPI application exposing notebook operations over HTTP."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from nbops import __version__
from nbops.clean import clean_notebook
from nbops.convert import convert_notebook
from nbops.diff import diff_notebooks
from nbops.inspect import compute_stats, extract_imports, outline
from nbops.lint import lint_notebook
from nbops.models import (
    CleanOptions,
    ConvertResult,
    HealthResponse,
    LintReport,
    NotebookDiff,
    NotebookPayload,
    NotebookStats,
)
from nbops.transform import concat_notebooks, set_kernelspec

app = FastAPI(
    title="nbops",
    version=__version__,
    summary="General operations toolkit for Jupyter notebooks.",
)


class InspectResponse(BaseModel):
    stats: NotebookStats
    outline: list[dict[str, Any]]
    imports: list[dict[str, Any]]


class ConvertRequest(NotebookPayload):
    format: str = Field("py", description="py, script, or md")


class CleanRequest(NotebookPayload):
    options: CleanOptions = Field(default_factory=CleanOptions)


class ConcatRequest(BaseModel):
    notebooks: list[dict[str, Any]] = Field(..., min_length=1)


class KernelRequest(NotebookPayload):
    name: str
    display_name: str | None = None
    language: str | None = None


class DiffRequest(BaseModel):
    left: dict[str, Any]
    right: dict[str, Any]


class NotebookDocument(BaseModel):
    notebook: dict[str, Any]


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    """Liveness/readiness probe."""
    return HealthResponse(version=__version__)


@app.post("/notebooks/stats", response_model=NotebookStats, tags=["notebooks"])
def notebook_stats(request: NotebookPayload) -> NotebookStats:
    """Compute statistics for a posted notebook document."""
    try:
        return compute_stats(request.notebook)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/notebooks/inspect", response_model=InspectResponse, tags=["notebooks"])
def notebook_inspect(request: NotebookPayload) -> InspectResponse:
    """Return stats, headings, and imports for a posted notebook."""
    try:
        document = request.notebook
        return InspectResponse(
            stats=compute_stats(document),
            outline=[item.model_dump() for item in outline(document)],
            imports=[item.model_dump() for item in extract_imports(document)],
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/notebooks/lint", response_model=LintReport, tags=["notebooks"])
def notebook_lint(request: NotebookPayload) -> LintReport:
    """Lint a posted notebook document."""
    return lint_notebook(request.notebook)


@app.post("/notebooks/clean", response_model=NotebookDocument, tags=["notebooks"])
def notebook_clean(request: CleanRequest) -> NotebookDocument:
    """Return a cleaned copy of a posted notebook."""
    try:
        return NotebookDocument(notebook=clean_notebook(request.notebook, request.options))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/notebooks/convert", response_model=ConvertResult, tags=["notebooks"])
def notebook_convert(request: ConvertRequest) -> ConvertResult:
    """Convert a posted notebook to py, script, or md."""
    try:
        return convert_notebook(request.notebook, request.format)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/notebooks/concat", response_model=NotebookDocument, tags=["notebooks"])
def notebook_concat(request: ConcatRequest) -> NotebookDocument:
    """Concatenate posted notebook documents."""
    return NotebookDocument(notebook=concat_notebooks(request.notebooks))


@app.post("/notebooks/kernel", response_model=NotebookDocument, tags=["notebooks"])
def notebook_kernel(request: KernelRequest) -> NotebookDocument:
    """Update kernelspec metadata on a posted notebook."""
    return NotebookDocument(
        notebook=set_kernelspec(
            request.notebook,
            name=request.name,
            display_name=request.display_name,
            language=request.language,
        )
    )


@app.post("/notebooks/diff", response_model=NotebookDiff, tags=["notebooks"])
def notebook_diff(request: DiffRequest) -> NotebookDiff:
    """Diff two posted notebook documents."""
    return diff_notebooks(request.left, request.right)
