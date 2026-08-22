"""Unit tests for directory batch operations."""

from __future__ import annotations

from pathlib import Path

from nbops.batch import iter_notebooks, map_notebooks, notebook_paths
from nbops.inspect import stats_for_file


def test_iter_and_map(tmp_path: Path, sample_notebook_file: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    other = nested / "other.ipynb"
    other.write_text(sample_notebook_file.read_text(encoding="utf-8"), encoding="utf-8")
    checkpoint = tmp_path / ".ipynb_checkpoints" / "sample-checkpoint.ipynb"
    checkpoint.parent.mkdir()
    checkpoint.write_text("{}", encoding="utf-8")

    paths = iter_notebooks(tmp_path)
    assert sample_notebook_file in paths
    assert other in paths
    assert checkpoint not in paths

    items = map_notebooks(tmp_path, lambda path: stats_for_file(path).total_cells)
    oks = [item for item in items if item.ok]
    assert len(oks) == 2
    assert all(item.result == 4 for item in oks)

    expanded = notebook_paths([tmp_path, sample_notebook_file])
    assert len(expanded) == 2


def test_map_captures_errors(tmp_path: Path) -> None:
    bad = tmp_path / "bad.ipynb"
    bad.write_text("{not json", encoding="utf-8")
    items = map_notebooks(tmp_path, lambda path: stats_for_file(path).total_cells)
    assert items[0].ok is False
    assert items[0].error
