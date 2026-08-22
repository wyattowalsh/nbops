"""Unit tests for nbops.inspect and core compatibility exports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from nbops.core import NotebookStats, compute_stats, load_notebook, stats_for_file
from nbops.inspect import extract_imports, outline


def test_compute_stats_counts_cells(sample_notebook: dict[str, Any]) -> None:
    result = compute_stats(sample_notebook)
    assert isinstance(result, NotebookStats)
    assert result.total_cells == 4
    assert result.code_cells == 2
    assert result.markdown_cells == 1
    assert result.raw_cells == 1


def test_compute_stats_counts_non_empty_code_lines(sample_notebook: dict[str, Any]) -> None:
    result = compute_stats(sample_notebook)
    assert result.code_lines == 4
    assert result.markdown_lines == 2
    assert result.executed_code_cells == 1
    assert result.stream_outputs == 1
    assert result.tags == ["setup"]
    assert result.kernel_name == "python3"
    assert result.nbformat_major == 4


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
    loaded = load_notebook(sample_notebook_file, validate=False)
    assert loaded["nbformat"] == 4
    result = stats_for_file(sample_notebook_file)
    assert result.total_cells == 4


def test_outline_and_imports(sample_notebook: dict[str, Any]) -> None:
    headings = outline(sample_notebook)
    assert headings[0].level == 1
    assert headings[0].title == "Title"
    imports = extract_imports(sample_notebook)
    assert imports[0].module == "os"
    assert imports[0].cell_index == 1


def test_extract_imports_from_import(sample_notebook: dict[str, Any]) -> None:
    sample_notebook["cells"][2]["source"] = "from pathlib import Path, PurePath\n"
    imports = extract_imports(sample_notebook)
    modules = {item.module for item in imports}
    assert "os" in modules
    assert "pathlib" in modules
