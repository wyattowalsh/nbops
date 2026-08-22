"""Compatibility tests for the historic core module path."""

from __future__ import annotations

from pathlib import Path

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
