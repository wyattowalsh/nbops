"""Compatibility tests for the historic core module path."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from nbops import from_percent_python
from nbops.core import NotebookStats, compute_stats, load_notebook, stats_for_file


def test_core_reexports() -> None:
    assert callable(compute_stats)
    assert callable(load_notebook)
    assert callable(stats_for_file)
    assert NotebookStats.__name__ == "NotebookStats"


def test_demo_notebook_library_stats_contract() -> None:
    demo = Path(__file__).resolve().parents[1] / "examples" / "demo.ipynb"
    stats = stats_for_file(demo, validate=False)
    assert stats.total_cells == 4
    assert stats.code_cells == 2
    assert stats.code_lines == 4
    assert stats.kernel == "Python 3"
    assert stats.language == "python"


def test_public_from_percent_python_export() -> None:
    notebook = from_percent_python("# %%\nvalue = 1\n")
    assert notebook["cells"][0]["cell_type"] == "code"


def test_public_outputs_validate_and_convert_exports() -> None:
    from nbops import list_outputs, to_percent_python, validate_notebook
    from nbops.io import new_notebook

    notebook = new_notebook()
    validate_notebook(notebook)
    assert list_outputs(notebook) == []
    assert to_percent_python(notebook) == ""


def test_load_notebook_default_is_lenient_like_original_scaffold(tmp_path: Path) -> None:
    """The stats scaffold used json.loads with no schema check."""
    path = tmp_path / "original-sample.ipynb"
    path.write_text(
        (
            '{"cells":[{"cell_type":"markdown","source":["# Title\\n"]},'
            '{"cell_type":"code","source":["x = 1\\n"]},'
            '{"cell_type":"code","source":"y = 2\\n"},'
            '{"cell_type":"raw","source":["raw"]}],'
            '"metadata":{"kernelspec":{"display_name":"Python 3","language":"python"},'
            '"language_info":{"name":"python"}},'
            '"nbformat":4,"nbformat_minor":5}'
        ),
        encoding="utf-8",
    )
    loaded = load_notebook(path)
    assert loaded["nbformat"] == 4
    assert len(loaded["cells"]) == 4
    stats = stats_for_file(path)
    assert stats.total_cells == 4
    assert stats.code_cells == 2
    assert stats.code_lines == 2
    assert stats.kernel == "Python 3"
    assert stats.language == "python"


def test_core_load_notebook_keeps_original_exception_types(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_notebook(tmp_path / "nope.ipynb")
    bad = tmp_path / "bad.ipynb"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="valid JSON"):
        load_notebook(bad)


@pytest.mark.parametrize("bad", [None, {}, {"cells": "nope"}, [], 42])
def test_core_compute_stats_rejects_invalid_like_original_scaffold(bad: Any) -> None:
    with pytest.raises(ValueError, match="Invalid notebook"):
        compute_stats(bad)
