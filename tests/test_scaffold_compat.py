"""Compatibility locks for the original stats-only scaffold.

The ``cursor/setup-dev-environment-a5a8`` tree shipped 19 pytest cases covering
``compute_stats``, ``nbops stats``, and ``POST /notebooks/stats``, plus a README
that started the API with ``uvicorn nbops.api:app``. These tests keep that
surface working after generalization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient
from typer.testing import CliRunner

from nbops import NotebookStats, __version__, compute_stats
from nbops.api import HealthResponse, StatsRequest, health
from nbops.api import app as api_app
from nbops.cli import app as cli_app
from nbops.core import load_notebook, stats_for_file
from nbops.models import HealthResponse as ModelHealthResponse
from nbops.models import NotebookPayload

ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()
client = TestClient(api_app)


def test_readme_documents_original_uvicorn_and_curl_stats() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "uv run nbops serve --host 0.0.0.0 --port 8000" in text
    assert "uv run uvicorn nbops.api:app --host 0.0.0.0 --port 8000" in text
    assert "curl -s http://127.0.0.1:8000/health" in text
    assert "http://127.0.0.1:8000/notebooks/stats" in text
    assert "Interactive API docs are available at `http://127.0.0.1:8000/docs`." in text


def test_package_root_still_exports_original_compute_stats() -> None:
    assert callable(compute_stats)
    assert NotebookStats.__name__ == "NotebookStats"


def test_original_scaffold_stats_library(original_scaffold_notebook: dict[str, Any]) -> None:
    result = compute_stats(original_scaffold_notebook)
    assert isinstance(result, NotebookStats)
    assert result.total_cells == 4
    assert result.code_cells == 2
    assert result.markdown_cells == 1
    assert result.raw_cells == 1
    assert result.code_lines == 4
    assert result.kernel == "Python 3"
    assert result.language == "python"


def test_original_scaffold_load_and_stats_for_file(
    original_scaffold_notebook_file: Path,
) -> None:
    loaded = load_notebook(original_scaffold_notebook_file)
    assert loaded["nbformat"] == 4
    assert "name" not in loaded["metadata"]["kernelspec"]
    result = stats_for_file(original_scaffold_notebook_file)
    assert result.total_cells == 4
    assert result.code_lines == 4
    assert result.kernel == "Python 3"


def test_original_scaffold_cli_table_prints_seven_rows(
    original_scaffold_notebook_file: Path,
) -> None:
    result = runner.invoke(cli_app, ["stats", str(original_scaffold_notebook_file)])
    assert result.exit_code == 0
    assert f"Notebook: {original_scaffold_notebook_file}" in result.stdout
    assert "Total cells   : 4" in result.stdout
    assert "Code cells    : 2" in result.stdout
    assert "Markdown cells: 1" in result.stdout
    assert "Raw cells     : 1" in result.stdout
    assert "Code lines    : 4" in result.stdout
    assert "Kernel        : Python 3" in result.stdout
    assert "Language      : python" in result.stdout


def test_original_scaffold_cli_invalid_json_fails_cleanly(tmp_path: Path) -> None:
    """Library ValueError on bad JSON must surface as a CLI error, not a traceback."""
    bad = tmp_path / "bad.ipynb"
    bad.write_text("{not json", encoding="utf-8")
    result = runner.invoke(cli_app, ["stats", str(bad)])
    assert result.exit_code != 0
    assert "valid JSON" in result.output


def test_original_scaffold_cli_json(original_scaffold_notebook_file: Path) -> None:
    result = runner.invoke(cli_app, ["stats", str(original_scaffold_notebook_file), "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["total_cells"] == 4
    assert payload["language"] == "python"
    assert payload["kernel"] == "Python 3"


def test_original_scaffold_http_health_and_stats(
    original_scaffold_notebook: dict[str, Any],
) -> None:
    health = client.get("/health")
    assert health.status_code == 200
    body = health.json()
    assert body["status"] == "ok"
    assert body["version"] == __version__

    response = client.post("/notebooks/stats", json={"notebook": original_scaffold_notebook})
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_cells"] == 4
    assert stats["code_cells"] == 2
    assert stats["code_lines"] == 4
    assert stats["kernel"] == "Python 3"
    assert stats["language"] == "python"


def test_original_scaffold_health_response_defaults() -> None:
    payload = HealthResponse()
    assert payload.status == "ok"
    assert payload.version == __version__
    assert health() == payload
    assert ModelHealthResponse is HealthResponse


def test_original_scaffold_stats_request_openapi_name() -> None:
    assert issubclass(StatsRequest, NotebookPayload)
    schema = api_app.openapi()
    assert schema["info"]["title"] == "nbops"
    assert "Jupyter notebooks" in schema["info"]["summary"]
    assert "StatsRequest" in schema["components"]["schemas"]
    health_schema = schema["components"]["schemas"]["HealthResponse"]
    required = set(health_schema.get("required") or [])
    assert "status" not in required
    assert "version" not in required
    assert health_schema["properties"]["status"].get("default") == "ok"
    assert health_schema["properties"]["version"].get("default") == __version__
    request_schema = StatsRequest.model_json_schema()
    assert (
        request_schema["properties"]["notebook"]["description"]
        == "A parsed nbformat v4 notebook document."
    )


def test_original_scaffold_interactive_docs_available() -> None:
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
