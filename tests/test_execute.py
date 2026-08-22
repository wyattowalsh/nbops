"""Unit tests for optional notebook execution."""

from __future__ import annotations

from typing import Any

import pytest

from nbops.exceptions import ExecuteError, MissingExtraError
from nbops.execute import execute_notebook


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
    executed = execute_notebook(sample_notebook, timeout=5, kernel_name="python3")
    assert executed["nbformat"] == 4
    assert len(executed["cells"]) == 4


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
