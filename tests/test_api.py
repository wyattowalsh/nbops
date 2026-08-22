"""Tests for the nbops FastAPI application."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from nbops.api import app
from nbops.io import load_notebook

client = TestClient(app)


def test_lint_and_clean_preserve_missing_cell_ids() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "# Title\n",
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    lint = client.post("/notebooks/lint", json={"notebook": notebook})
    assert lint.status_code == 200
    assert any(issue["code"] == "NB009" for issue in lint.json()["issues"])

    cleaned = client.post(
        "/notebooks/clean",
        json={
            "notebook": {
                **notebook,
                "cells": [
                    {
                        "cell_type": "markdown",
                        "id": "keep-me",
                        "metadata": {},
                        "source": "# Title\n",
                    }
                ],
            },
            "options": {"cell_ids": True, "outputs": False, "execution_counts": False},
        },
    )
    assert cleaned.status_code == 200
    assert "id" not in cleaned.json()["notebook"]["cells"][0]


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
    assert body["attachment_cells"] == 0
    assert body["attachment_files"] == 0
    assert body["has_widgets"] is False


def test_notebook_stats_rejects_invalid() -> None:
    response = client.post("/notebooks/stats", json={"notebook": {"cells": "nope"}})
    assert response.status_code == 422


def test_demo_notebook_stats_http_contract() -> None:
    demo = load_notebook(
        Path(__file__).resolve().parents[1] / "examples" / "demo.ipynb",
        validate=True,
    )
    response = client.post("/notebooks/stats", json={"notebook": demo})
    assert response.status_code == 200
    body = response.json()
    assert body["total_cells"] == 4
    assert body["code_cells"] == 2
    assert body["code_lines"] == 4
    assert body["kernel"] == "Python 3"
    assert body["language"] == "python"
    assert body["tags"] == ["demo"]


def test_inspect_inventories_attachments() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "See plot\n",
                "attachments": {"plot.png": {"image/png": "aaa"}},
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    inspect = client.post("/notebooks/inspect", json={"notebook": notebook})
    assert inspect.status_code == 200
    body = inspect.json()
    assert body["stats"]["attachment_cells"] == 1
    assert body["stats"]["attachment_files"] == 1
    assert body["attachments"] == [
        {
            "cell_index": 0,
            "filename": "plot.png",
            "mime_types": ["image/png"],
            "size": 3,
        }
    ]


def test_inspect_headings_imports_from_py(sample_notebook: dict[str, Any]) -> None:
    inspect = client.post("/notebooks/inspect", json={"notebook": sample_notebook})
    assert inspect.status_code == 200
    assert inspect.json()["outline"][0]["title"] == "Title"
    assert inspect.json()["outputs"][0]["output_type"] == "stream"
    assert inspect.json()["stats"]["attachment_cells"] == 0
    assert inspect.json()["attachments"] == []

    headings = client.post("/notebooks/headings", json={"notebook": sample_notebook})
    assert headings.status_code == 200
    assert headings.json()[0]["title"] == "Title"

    imports = client.post("/notebooks/imports", json={"notebook": sample_notebook})
    assert imports.status_code == 200
    assert imports.json()[0]["module"] == "os"

    outputs = client.post("/notebooks/outputs", json={"notebook": sample_notebook})
    assert outputs.status_code == 200
    assert outputs.json()[0]["output_type"] == "stream"

    from_py = client.post(
        "/notebooks/from-py",
        json={"text": "# %% [markdown]\n# Hello\n\n# %%\nprint(1)\n"},
    )
    assert from_py.status_code == 200
    cells = from_py.json()["notebook"]["cells"]
    assert [cell["cell_type"] for cell in cells] == ["markdown", "code"]
    assert all("id" not in cell for cell in cells)

    json_meta = client.post(
        "/notebooks/from-py",
        json={
            "text": (
                '# %% [markdown] {"tags": ["intro"], "collapsed": true}\n'
                "# Hello\n\n"
                "# %% collapsed=false\n"
                "print(1)\n"
            )
        },
    )
    assert json_meta.status_code == 200
    json_cells = json_meta.json()["notebook"]["cells"]
    assert json_cells[0]["cell_type"] == "markdown"
    assert json_cells[0]["metadata"]["tags"] == ["intro"]
    assert json_cells[0]["metadata"]["collapsed"] is True
    assert json_cells[1]["metadata"]["collapsed"] is False
    assert all("id" not in cell for cell in json_cells)


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

    scripted = client.post(
        "/notebooks/convert", json={"notebook": sample_notebook, "format": "script"}
    )
    assert scripted.status_code == 200
    assert scripted.json()["format"] == "script"
    assert "import os" in scripted.json()["text"]
    assert "# Title" not in scripted.json()["text"]


def test_operations_split_filter_tag_ids_new(sample_notebook: dict[str, Any]) -> None:
    catalog = client.get("/operations")
    assert catalog.status_code == 200
    names = {item["name"] for item in catalog.json()}
    assert "stats" in names
    assert "exec" in names
    assert "ops" in names
    assert "from-py" in names
    assert "outputs" in names
    assert "validate" in names

    split = client.post("/notebooks/split", json={"notebook": sample_notebook, "level": 1})
    assert split.status_code == 200
    assert split.json()["sections"]

    filtered = client.post(
        "/notebooks/filter",
        json={"notebook": sample_notebook, "cell_types": ["code"]},
    )
    assert filtered.status_code == 200
    assert len(filtered.json()["notebook"]["cells"]) == 2

    tagged = client.post(
        "/notebooks/tag",
        json={"notebook": sample_notebook, "cell_index": 0, "tags": ["intro"]},
    )
    assert tagged.status_code == 200
    assert "intro" in tagged.json()["notebook"]["cells"][0]["metadata"]["tags"]

    untagged = client.post(
        "/notebooks/tag",
        json={"notebook": sample_notebook, "cell_index": 1, "remove": ["setup"]},
    )
    assert untagged.status_code == 200
    assert untagged.json()["notebook"]["cells"][1]["metadata"]["tags"] == []

    empty_tag = client.post(
        "/notebooks/tag",
        json={"notebook": sample_notebook, "cell_index": 0},
    )
    assert empty_tag.status_code == 422

    ids = client.post("/notebooks/ids", json={"notebook": sample_notebook})
    assert ids.status_code == 200
    assert ids.json()["notebook"]["cells"][0]["id"]

    created = client.post("/notebooks/new")
    assert created.status_code == 200
    assert created.json()["notebook"]["cells"] == []

    created_kernel = client.post(
        "/notebooks/new",
        params={"kernel_name": "ir", "language": "r", "display_name": "R"},
    )
    assert created_kernel.status_code == 200
    assert created_kernel.json()["notebook"]["metadata"]["kernelspec"]["name"] == "ir"

    valid = client.post("/notebooks/validate", json={"notebook": created.json()["notebook"]})
    assert valid.status_code == 200
    assert valid.json()["valid"] is True

    invalid = client.post("/notebooks/validate", json={"notebook": {"cells": "nope"}})
    assert invalid.status_code == 200
    assert invalid.json()["valid"] is False


def test_execute_endpoint_reports_missing_extra(
    monkeypatch: pytest.MonkeyPatch, sample_notebook: dict[str, Any]
) -> None:
    from nbops import execute as execute_mod
    from nbops.exceptions import MissingExtraError

    monkeypatch.setattr(
        execute_mod,
        "_notebook_client_class",
        lambda: (_ for _ in ()).throw(MissingExtraError("need extra")),
    )
    response = client.post("/notebooks/execute", json={"notebook": sample_notebook})
    assert response.status_code == 503


def test_concat_kernel_diff(sample_notebook: dict[str, Any]) -> None:
    concat = client.post(
        "/notebooks/concat", json={"notebooks": [sample_notebook, sample_notebook]}
    )
    assert concat.status_code == 200
    assert len(concat.json()["notebook"]["cells"]) == 8
    ids = [cell["id"] for cell in concat.json()["notebook"]["cells"]]
    assert len(set(ids)) == 8

    too_few = client.post("/notebooks/concat", json={"notebooks": [sample_notebook]})
    assert too_few.status_code == 422

    kernel = client.post(
        "/notebooks/kernel",
        json={"notebook": sample_notebook, "name": "ir", "language": "r"},
    )
    assert kernel.status_code == 200
    assert kernel.json()["notebook"]["metadata"]["kernelspec"]["name"] == "ir"

    diff = client.post("/notebooks/diff", json={"left": sample_notebook, "right": sample_notebook})
    assert diff.status_code == 200
    assert diff.json()["identical"] is True


def test_concat_http_preserves_omitted_cell_ids(
    original_shipped_demo_notebook: dict[str, Any],
) -> None:
    concat = client.post(
        "/notebooks/concat",
        json={"notebooks": [original_shipped_demo_notebook, original_shipped_demo_notebook]},
    )
    assert concat.status_code == 200
    cells = concat.json()["notebook"]["cells"]
    assert len(cells) == 8
    assert all("id" not in cell for cell in cells)


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


def test_tag_and_execute_error_paths(
    monkeypatch: pytest.MonkeyPatch, sample_notebook: dict[str, Any]
) -> None:
    tagged = client.post(
        "/notebooks/tag",
        json={"notebook": sample_notebook, "cell_index": 99, "tags": ["x"]},
    )
    assert tagged.status_code == 422

    from nbops import execute as execute_mod

    class Boom:
        def __init__(self, node: Any, **kwargs: Any) -> None:
            pass

        def execute(self) -> Any:
            raise RuntimeError("kernel died")

    monkeypatch.setattr(execute_mod, "_notebook_client_class", lambda: Boom)
    response = client.post("/notebooks/execute", json={"notebook": sample_notebook})
    assert response.status_code == 422


def test_lifespan_enters_and_health_still_works() -> None:
    with TestClient(app) as lifespan_client:
        response = lifespan_client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_split_maps_library_valueerror(
    monkeypatch: pytest.MonkeyPatch, sample_notebook: dict[str, Any]
) -> None:
    def _raise_level(*_args: Any, **_kwargs: Any) -> Any:
        raise ValueError("Heading level must be between 1 and 6.")

    monkeypatch.setattr("nbops.api.split_by_headings", _raise_level)
    response = client.post("/notebooks/split", json={"notebook": sample_notebook, "level": 1})
    assert response.status_code == 422
    assert "Heading level" in response.json()["detail"]


def test_execute_endpoint_success(
    monkeypatch: pytest.MonkeyPatch, sample_notebook: dict[str, Any]
) -> None:
    def fake_execute(notebook: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        assert kwargs["kernel_name"] == "python3"
        updated = dict(notebook)
        updated["metadata"] = {**dict(notebook.get("metadata") or {}), "executed": True}
        return updated

    monkeypatch.setattr("nbops.execute.execute_notebook", fake_execute)
    response = client.post(
        "/notebooks/execute",
        json={"notebook": sample_notebook, "kernel_name": "python3", "timeout": 5},
    )
    assert response.status_code == 200
    assert response.json()["notebook"]["metadata"]["executed"] is True
