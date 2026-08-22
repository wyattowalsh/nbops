"""Unit tests for cell helpers."""

from __future__ import annotations

from nbops.cells import cell_source, is_empty_cell, non_empty_line_count, preview, source_lines


def test_source_helpers() -> None:
    cell = {"source": ["import os\n", "\n", "x = 1\n"]}
    assert "import os" in cell_source(cell)
    assert source_lines(cell)[0] == "import os"
    assert non_empty_line_count(cell) == 2
    assert is_empty_cell({"source": "  \n"}) is True
    assert preview("one   two   three", limit=7) == preview("one two three", limit=7)
    assert len(preview("abcdefghij", limit=7)) == 7


def test_source_non_string() -> None:
    assert cell_source({"source": 123}) == ""
    assert cell_source({}) == ""
