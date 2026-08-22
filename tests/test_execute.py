"""Unit tests for optional notebook execution."""

from __future__ import annotations

from typing import Any

import pytest

import nbops
from nbops.exceptions import ExecuteError, MissingExtraError
from nbops.execute import _apply_original_cell_ids, _original_cell_ids, execute_notebook
from nbops.lint import lint_notebook


def test_execute_notebook_is_exported() -> None:
    assert nbops.execute_notebook is execute_notebook


def test_execute_requires_extra(
    monkeypatch: pytest.MonkeyPatch, sample_notebook: dict[str, Any]
) -> None:
    monkeypatch.setattr(
        "nbops.execute._notebook_client_class",
        lambda: (_ for _ in ()).throw(MissingExtraError("missing")),
    )
    with pytest.raises(MissingExtraError, match="missing"):
        execute_notebook(sample_notebook)


def test_execute_success_with_fake_client(
    monkeypatch: pytest.MonkeyPatch, sample_notebook: dict[str, Any]
) -> None:
    class FakeClient:
        def __init__(self, node: Any, **kwargs: Any) -> None:
            self.node = node

        def execute(self) -> Any:
            return self.node

    monkeypatch.setattr("nbops.execute._notebook_client_class", lambda: FakeClient)
    executed = execute_notebook(sample_notebook, timeout=5, kernel_name="python3", cwd=".")
    assert executed["nbformat"] == 4
    assert len(executed["cells"]) == 4


def test_notebook_client_class_returns_imported_type(monkeypatch: pytest.MonkeyPatch) -> None:
    import sys
    import types

    module = types.ModuleType("nbclient")

    class NotebookClient:
        pass

    module.NotebookClient = NotebookClient
    monkeypatch.setitem(sys.modules, "nbclient", module)
    from nbops.execute import _notebook_client_class

    assert _notebook_client_class() is NotebookClient


def test_execute_wraps_client_errors(
    monkeypatch: pytest.MonkeyPatch, sample_notebook: dict[str, Any]
) -> None:
    class BoomClient:
        def __init__(self, node: Any, **kwargs: Any) -> None:
            pass

        def execute(self) -> Any:
            raise RuntimeError("kernel died")

    monkeypatch.setattr("nbops.execute._notebook_client_class", lambda: BoomClient)
    with pytest.raises(ExecuteError, match="kernel died"):
        execute_notebook(sample_notebook)


def _fake_passthrough_client() -> type:
    class FakeClient:
        def __init__(self, node: Any, **kwargs: Any) -> None:
            self.node = node

        def execute(self) -> Any:
            return self.node

    return FakeClient


def test_execute_preserves_omitted_cell_ids(
    monkeypatch: pytest.MonkeyPatch, original_shipped_demo_notebook: dict[str, Any]
) -> None:
    monkeypatch.setattr("nbops.execute._notebook_client_class", _fake_passthrough_client)
    executed = execute_notebook(original_shipped_demo_notebook, timeout=5)
    assert all("id" not in cell for cell in executed["cells"])
    assert any(issue.code == "NB009" for issue in lint_notebook(executed).issues)


def test_execute_keeps_existing_cell_ids(
    monkeypatch: pytest.MonkeyPatch, sample_notebook: dict[str, Any]
) -> None:
    monkeypatch.setattr("nbops.execute._notebook_client_class", _fake_passthrough_client)
    executed = execute_notebook(sample_notebook, timeout=5)
    assert [cell["id"] for cell in executed["cells"]] == [
        cell["id"] for cell in sample_notebook["cells"]
    ]


def test_original_cell_id_helpers_cover_edge_shapes() -> None:
    assert _original_cell_ids({"cells": "nope"}) == []
    assert _original_cell_ids({"cells": [{"id": ""}, "skip", {"id": "keep"}]}) == [
        None,
        None,
        "keep",
    ]
    skipped = _apply_original_cell_ids({"cells": "nope"}, ["a"])
    assert skipped["cells"] == "nope"
    mixed = _apply_original_cell_ids(
        {"cells": [{"id": "generated"}, "skip", {"id": "extra"}]},
        [None],
    )
    assert "id" not in mixed["cells"][0]
    assert mixed["cells"][1] == "skip"
    assert mixed["cells"][2]["id"] == "extra"
