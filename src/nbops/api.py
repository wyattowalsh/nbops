"""FastAPI application exposing notebook operations over HTTP."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from nbops import __version__
from nbops.clean import clean_notebook
from nbops.convert import convert_notebook, from_percent_python
from nbops.diff import diff_notebooks
from nbops.exceptions import ExecuteError, MissingExtraError
from nbops.inspect import compute_stats, extract_imports, outline
from nbops.io import new_notebook
from nbops.lint import lint_notebook
from nbops.models import (
    CleanOptions,
    ConvertResult,
    HealthResponse,
    Heading,
    ImportRecord,
    LintReport,
    NotebookDiff,
    NotebookPayload,
    NotebookStats,
)
from nbops.operations import OPERATIONS, Operation
from nbops.settings import configure_logging, get_settings
from nbops.transform import (
    add_tags,
    concat_notebooks,
    ensure_cell_ids,
    filter_cells,
    set_kernelspec,
    split_by_headings,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    yield


app = FastAPI(
    title="nbops",
    version=__version__,
    summary="General operations toolkit for Jupyter notebooks.",
    lifespan=lifespan,
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


class SplitRequest(NotebookPayload):
    level: int = Field(1, ge=1, le=6)


class SplitSection(BaseModel):
    title: str
    notebook: dict[str, Any]


class SplitResponse(BaseModel):
    sections: list[SplitSection]


class FilterRequest(NotebookPayload):
    cell_types: list[str] | None = None
    tags: list[str] | None = None


class TagRequest(NotebookPayload):
    cell_index: int = Field(..., ge=0)
    tags: list[str] = Field(..., min_length=1)


class ExecuteRequest(NotebookPayload):
    timeout: int | None = Field(None, ge=1)
    kernel_name: str | None = None
    allow_errors: bool = False


class FromPyRequest(BaseModel):
    text: str


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    """Liveness/readiness probe."""
    return HealthResponse(version=__version__)


@app.get("/operations", response_model=list[Operation], tags=["system"])
def list_operations() -> list[Operation]:
    """Return the canonical operations catalog."""
    return list(OPERATIONS)


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


@app.post("/notebooks/headings", response_model=list[Heading], tags=["notebooks"])
def notebook_headings(request: NotebookPayload) -> list[Heading]:
    """Return markdown headings for a posted notebook."""
    return outline(request.notebook)


@app.post("/notebooks/imports", response_model=list[ImportRecord], tags=["notebooks"])
def notebook_imports(request: NotebookPayload) -> list[ImportRecord]:
    """Return top-level imports for a posted notebook."""
    return extract_imports(request.notebook)


@app.post("/notebooks/lint", response_model=LintReport, tags=["notebooks"])
def notebook_lint(request: NotebookPayload) -> LintReport:
    """Lint a posted notebook document."""
    return lint_notebook(
        request.notebook,
        max_output_chars=get_settings().max_output_chars,
    )


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


@app.post("/notebooks/split", response_model=SplitResponse, tags=["notebooks"])
def notebook_split(request: SplitRequest) -> SplitResponse:
    """Split a posted notebook on markdown headings."""
    try:
        sections = split_by_headings(request.notebook, level=request.level)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return SplitResponse(
        sections=[SplitSection(title=title, notebook=section) for title, section in sections]
    )


@app.post("/notebooks/filter", response_model=NotebookDocument, tags=["notebooks"])
def notebook_filter(request: FilterRequest) -> NotebookDocument:
    """Keep cells matching type and/or tag filters."""
    return NotebookDocument(
        notebook=filter_cells(
            request.notebook,
            cell_types=request.cell_types,
            tags=request.tags,
        )
    )


@app.post("/notebooks/tag", response_model=NotebookDocument, tags=["notebooks"])
def notebook_tag(request: TagRequest) -> NotebookDocument:
    """Add tags to a cell in a posted notebook."""
    try:
        return NotebookDocument(
            notebook=add_tags(request.notebook, request.cell_index, request.tags)
        )
    except (IndexError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/notebooks/ids", response_model=NotebookDocument, tags=["notebooks"])
def notebook_ids(request: NotebookPayload) -> NotebookDocument:
    """Assign unique cell ids where they are missing or duplicated."""
    return NotebookDocument(notebook=ensure_cell_ids(request.notebook))


@app.post("/notebooks/execute", response_model=NotebookDocument, tags=["notebooks"])
def notebook_execute(request: ExecuteRequest) -> NotebookDocument:
    """Execute a posted notebook (requires the optional extra nbops[execute])."""
    from nbops.execute import execute_notebook

    try:
        executed = execute_notebook(
            request.notebook,
            timeout=request.timeout or get_settings().execute_timeout,
            kernel_name=request.kernel_name,
            allow_errors=request.allow_errors,
        )
    except MissingExtraError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except (ExecuteError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return NotebookDocument(notebook=executed)


@app.post("/notebooks/new", response_model=NotebookDocument, tags=["notebooks"])
def notebook_new() -> NotebookDocument:
    """Return a new empty nbformat v4 notebook."""
    return NotebookDocument(notebook=new_notebook())


@app.post("/notebooks/from-py", response_model=NotebookDocument, tags=["notebooks"])
def notebook_from_py(request: FromPyRequest) -> NotebookDocument:
    """Parse a percent-format Python script into a notebook."""
    return NotebookDocument(notebook=from_percent_python(request.text))
