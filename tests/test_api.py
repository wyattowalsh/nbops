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
