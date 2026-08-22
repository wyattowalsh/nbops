"""Unit tests for notebook I/O."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from nbops.exceptions import InvalidNotebookError, NotebookNotFoundError
from nbops.io import (
    dumps_notebook,
    load_notebook,
    new_notebook,
    parse_notebook,
    save_notebook,
    validate_notebook,
)


def test_new_notebook_has_kernelspec() -> None:
    notebook = new_notebook()
    assert notebook["nbformat"] == 4
    assert notebook["cells"] == []
    assert notebook["metadata"]["kernelspec"]["name"] == "python3"


def test_parse_and_roundtrip(sample_notebook: dict[str, Any]) -> None:
    parsed = parse_notebook(sample_notebook, validate=False)
    dumped = dumps_notebook(parsed)
    again = parse_notebook(dumped, validate=False)
    assert again["nbformat"] == 4
    assert len(again["cells"]) == 4


def test_save_and_load_roundtrip(tmp_path: Path, sample_notebook: dict[str, Any]) -> None:
    path = tmp_path / "nested" / "demo.ipynb"
    save_notebook(sample_notebook, path, validate=False)
    loaded = load_notebook(path, validate=False)
    assert loaded["nbformat"] == 4
    assert len(loaded["cells"]) == 4


def test_load_notebook_missing(tmp_path: Path) -> None:
    with pytest.raises(NotebookNotFoundError):
        load_notebook(tmp_path / "nope.ipynb")


def test_load_notebook_invalid_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.ipynb"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(InvalidNotebookError):
        load_notebook(bad, validate=False)


def test_parse_invalid_document() -> None:
    with pytest.raises(InvalidNotebookError):
        parse_notebook("not-a-notebook", validate=False)


def test_validate_rejects_wrong_shape() -> None:
    with pytest.raises(InvalidNotebookError):
        parse_notebook({"cells": "nope", "nbformat": 4, "nbformat_minor": 5}, validate=True)


def test_load_notebook_validates_new_notebook(tmp_path: Path) -> None:
    path = tmp_path / "fresh.ipynb"
    save_notebook(new_notebook(), path, validate=True)
    loaded = load_notebook(path, validate=True)
    assert loaded["cells"] == []
    assert loaded["nbformat"] == 4
    validate_notebook(loaded)
