"""Frozen unit tests for ``nbops.core`` from the stats-only scaffold."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from nbops.core import NotebookStats, compute_stats, load_notebook, stats_for_file


def test_compute_stats_counts_cells(sample_notebook: dict[str, Any]) -> None:
    result = compute_stats(sample_notebook)
    assert isinstance(result, NotebookStats)
    assert result.total_cells == 4
    assert result.code_cells == 2
    assert result.markdown_cells == 1
    assert result.raw_cells == 1


def test_compute_stats_counts_non_empty_code_lines(sample_notebook: dict[str, Any]) -> None:
    # First code cell: "import os", "print(...)" (blank line ignored) -> 2
    # Second code cell: "x = 1", "y = 2" -> 2
    result = compute_stats(sample_notebook)
    assert result.code_lines == 4


def test_compute_stats_reads_metadata(sample_notebook: dict[str, Any]) -> None:
    result = compute_stats(sample_notebook)
    assert result.kernel == "Python 3"
    assert result.language == "python"


def test_compute_stats_empty_notebook() -> None:
    result = compute_stats({"cells": []})
    assert result.total_cells == 0
    assert result.code_lines == 0
    assert result.kernel is None


@pytest.mark.parametrize("bad", [None, {}, {"cells": "nope"}, [], 42])
def test_compute_stats_rejects_invalid(bad: Any) -> None:
    with pytest.raises(ValueError, match="Invalid notebook"):
        compute_stats(bad)


def test_load_and_stats_for_file(sample_notebook_file: Path) -> None:
    loaded = load_notebook(sample_notebook_file)
    assert loaded["nbformat"] == 4
    result = stats_for_file(sample_notebook_file)
    assert result.total_cells == 4


def test_load_notebook_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_notebook(tmp_path / "nope.ipynb")


def test_load_notebook_invalid_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.ipynb"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="valid JSON"):
        load_notebook(bad)
