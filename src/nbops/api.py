"""FastAPI application exposing nbops notebook analysis over HTTP."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from nbops import __version__
from nbops.core import NotebookStats, compute_stats

app = FastAPI(
    title="nbops",
    version=__version__,
    summary="Lightweight operations toolkit for Jupyter notebooks.",
)


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = __version__


class StatsRequest(BaseModel):
    """Request body carrying a raw notebook document."""

    notebook: dict[str, Any] = Field(..., description="A parsed nbformat v4 notebook document.")


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    """Liveness/readiness probe."""
    return HealthResponse()


@app.post("/notebooks/stats", response_model=NotebookStats, tags=["notebooks"])
def notebook_stats(request: StatsRequest) -> NotebookStats:
    """Compute statistics for a posted notebook document."""
    try:
        return compute_stats(request.notebook)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
