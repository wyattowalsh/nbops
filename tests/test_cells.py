"""Unit tests for cell helpers."""

from __future__ import annotations

import ast

import pytest

from nbops.cells import (
    cell_source,
    is_empty_cell,
    is_python_notebook,
    non_empty_line_count,
    parse_code_cell,
    preview,
    source_lines,
    strip_ipython_magics,
)


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


def test_cell_tags_non_list() -> None:
    from nbops.cells import cell_tags

    assert cell_tags({"metadata": {"tags": "setup"}}) == []
    assert cell_tags({"metadata": "nope"}) == []


def test_strip_ipython_magics_and_parse_code_cell() -> None:
    mixed = "%matplotlib inline\nimport os\nx = %time 1 + 1\n"
    cleaned = strip_ipython_magics(mixed)
    assert cleaned is not None
    assert "import os" in cleaned
    assert "%matplotlib" not in cleaned
    assert "x = 1 + 1" in cleaned
    tree = parse_code_cell(mixed)
    assert tree is not None
    assert any(isinstance(node, ast.Import) for node in tree.body)

    assert strip_ipython_magics("%%bash\necho hi\n") is None
    assert parse_code_cell("%%bash\necho hi\n") is None
    timed = strip_ipython_magics("%%time\nimport os\n")
    assert timed is not None
    assert "import os" in timed
    assert parse_code_cell("%pwd\n").body == []
    pwd = strip_ipython_magics("result = %pwd\n")
    assert pwd is not None and "result = ..." in pwd
    help_line = strip_ipython_magics("str?\nimport json\n")
    assert help_line is not None and "import json" in help_line
    bang = strip_ipython_magics("!ls\nprint(1)\n")
    assert bang is not None and "print(1)" in bang
    prefix_help = strip_ipython_magics("?\nimport os\n")
    assert prefix_help is not None and "import os" in prefix_help
    blanked = strip_ipython_magics("%pwd\n\nimport os\n")
    assert blanked is not None and "import os" in blanked
    formatted = parse_code_cell('value = "%s" % name\n')
    assert formatted is not None
    awaited = parse_code_cell("await fetch()\n")
    assert awaited is not None
    assert strip_ipython_magics("\n\n%%HTML\n<div></div>\n") is None
    assert strip_ipython_magics("%%sql\nSELECT 1\n") is None
    with pytest.raises(SyntaxError):
        parse_code_cell("def (\n")
    assert strip_ipython_magics("") == ""
    assert parse_code_cell("   \n").body == []


def test_is_python_notebook_defaults_and_declared_languages() -> None:
    assert is_python_notebook({"cells": []}) is True
    assert is_python_notebook({"metadata": {"language_info": {"name": "Python"}}}) is True
    assert is_python_notebook({"metadata": {"language_info": {"name": "ipython"}}}) is True
    assert is_python_notebook({"metadata": {"language_info": {"name": "  "}}}) is True
    assert is_python_notebook({"metadata": {"language_info": {"name": 3}}}) is True
    assert is_python_notebook({"metadata": {"kernelspec": {"language": "r"}}}) is False
    assert is_python_notebook({"metadata": {"language_info": {"name": "r"}}}) is False
