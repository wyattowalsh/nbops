"""Tests for the nbops FastAPI application."""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from nbops.api import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_notebook_stats_endpoint(sample_notebook: dict[str, Any]) -> None:
    response = client.post("/notebooks/stats", json={"notebook": sample_notebook})
    assert response.status_code == 200
    body = response.json()
    assert body["total_cells"] == 4
    assert body["code_cells"] == 2
    assert body["code_lines"] == 4


def test_notebook_stats_rejects_invalid() -> None:
    response = client.post("/notebooks/stats", json={"notebook": {"cells": "nope"}})
    assert response.status_code == 422


def test_inspect_lint_clean_convert(sample_notebook: dict[str, Any]) -> None:
    inspect = client.post("/notebooks/inspect", json={"notebook": sample_notebook})
    assert inspect.status_code == 200
    assert inspect.json()["outline"][0]["title"] == "Title"

    lint = client.post("/notebooks/lint", json={"notebook": sample_notebook})
    assert lint.status_code == 200
    assert lint.json()["passed"] is True

    cleaned = client.post("/notebooks/clean", json={"notebook": sample_notebook})
    assert cleaned.status_code == 200
    assert cleaned.json()["notebook"]["cells"][1]["outputs"] == []

    converted = client.post(
        "/notebooks/convert", json={"notebook": sample_notebook, "format": "md"}
    )
    assert converted.status_code == 200
    assert "# Title" in converted.json()["text"]


def test_concat_kernel_diff(sample_notebook: dict[str, Any]) -> None:
    concat = client.post(
        "/notebooks/concat", json={"notebooks": [sample_notebook, sample_notebook]}
    )
    assert concat.status_code == 200
    assert len(concat.json()["notebook"]["cells"]) == 8

    kernel = client.post(
        "/notebooks/kernel",
        json={"notebook": sample_notebook, "name": "ir", "language": "r"},
    )
    assert kernel.status_code == 200
    assert kernel.json()["notebook"]["metadata"]["kernelspec"]["name"] == "ir"

    diff = client.post("/notebooks/diff", json={"left": sample_notebook, "right": sample_notebook})
    assert diff.status_code == 200
    assert diff.json()["identical"] is True


def test_inspect_and_clean_reject_invalid() -> None:
    inspect = client.post("/notebooks/inspect", json={"notebook": {"cells": "nope"}})
    assert inspect.status_code == 422
    cleaned = client.post("/notebooks/clean", json={"notebook": {"cells": "nope"}})
    assert cleaned.status_code == 422


def test_convert_rejects_unknown_format(sample_notebook: dict[str, Any]) -> None:
    response = client.post(
        "/notebooks/convert",
        json={"notebook": sample_notebook, "format": "pdf"},
    )
    assert response.status_code == 422
