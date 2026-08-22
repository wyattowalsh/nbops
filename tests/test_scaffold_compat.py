"""Compatibility locks for the original stats-only scaffold.

The ``cursor/setup-dev-environment-a5a8`` tree shipped 19 pytest cases covering
``compute_stats``, ``nbops stats``, and ``POST /notebooks/stats``, plus a README
that started the API with ``uvicorn nbops.api:app``. These tests keep that
surface working after generalization.
"""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import httpx
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from nbops import NotebookStats, __version__, compute_stats
from nbops.api import HealthResponse, StatsRequest, health
from nbops.api import app as api_app
from nbops.cli import app as cli_app
from nbops.core import load_notebook, stats_for_file
from nbops.io import save_notebook
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
    assert "Widgets       : no" in result.stdout
    assert "Attachment cells: 0" in result.stdout
    assert "Attachment files: 0" in result.stdout


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


def test_original_shipped_demo_stats_and_omitted_ids(
    original_shipped_demo_notebook: dict[str, Any],
    original_shipped_demo_notebook_file: Path,
    tmp_path: Path,
) -> None:
    result = compute_stats(original_shipped_demo_notebook)
    assert result.total_cells == 4
    assert result.code_cells == 2
    assert result.markdown_cells == 2
    assert result.raw_cells == 0
    assert result.code_lines == 4
    assert result.kernel == "Python 3"
    assert result.kernel_name == "python3"
    assert result.language == "python"

    loaded = load_notebook(original_shipped_demo_notebook_file)
    assert [cell.get("id") for cell in loaded["cells"]] == [None, None, None, None]
    assert all("id" not in cell for cell in loaded["cells"])
    assert loaded["metadata"]["language_info"]["version"] == "3.12"

    out = tmp_path / "roundtrip.ipynb"
    save_notebook(loaded, out, validate=True)
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert all("id" not in cell for cell in saved["cells"])
    assert saved["metadata"]["language_info"]["version"] == "3.12"

    file_stats = stats_for_file(original_shipped_demo_notebook_file)
    assert file_stats.total_cells == 4
    assert file_stats.code_lines == 4


def test_original_readme_uvicorn_health_and_stats(
    original_shipped_demo_notebook: dict[str, Any],
) -> None:
    """Live ``uvicorn nbops.api:app`` as documented in the original README."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "nbops.api:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    url = f"http://127.0.0.1:{port}"
    try:
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            try:
                probe = httpx.get(f"{url}/health", timeout=0.3)
            except httpx.TransportError:
                time.sleep(0.05)
                continue
            if probe.status_code == 200:
                break
        else:
            stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
            raise AssertionError(f"uvicorn nbops.api:app did not become ready\n{stderr}")

        health = httpx.get(f"{url}/health", timeout=2.0)
        assert health.status_code == 200
        assert health.json()["status"] == "ok"
        assert health.json()["version"] == __version__

        docs = httpx.get(f"{url}/docs", timeout=2.0)
        assert docs.status_code == 200

        stats = httpx.post(
            f"{url}/notebooks/stats",
            json={"notebook": original_shipped_demo_notebook},
            timeout=2.0,
        )
        assert stats.status_code == 200
        body = stats.json()
        assert body["total_cells"] == 4
        assert body["code_cells"] == 2
        assert body["code_lines"] == 4
        assert body["kernel"] == "Python 3"
        assert body["language"] == "python"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
