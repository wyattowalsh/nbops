"""Compatibility tests for the historic core module path."""

from __future__ import annotations

from nbops.core import NotebookStats, compute_stats, load_notebook, stats_for_file


def test_core_reexports() -> None:
    assert callable(compute_stats)
    assert callable(load_notebook)
    assert callable(stats_for_file)
    assert NotebookStats.__name__ == "NotebookStats"
