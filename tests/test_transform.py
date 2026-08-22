"""Unit tests for notebook transforms."""

from __future__ import annotations

from typing import Any

import pytest

from nbops.transform import (
    add_tags,
    concat_notebooks,
    filter_cells,
    set_kernelspec,
    split_by_headings,
)


def test_filter_by_type_and_tag(sample_notebook: dict[str, Any]) -> None:
    code_only = filter_cells(sample_notebook, cell_types=["code"])
    assert len(code_only["cells"]) == 2
    tagged = filter_cells(sample_notebook, tags=["setup"])
    assert len(tagged["cells"]) == 1
    assert tagged["cells"][0]["id"] == "code-os"


def test_concat_notebooks(sample_notebook: dict[str, Any]) -> None:
    other = {
        "cells": [{"cell_type": "markdown", "metadata": {}, "source": "# Other\n"}],
        "metadata": sample_notebook["metadata"],
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    merged = concat_notebooks([sample_notebook, other])
    assert len(merged["cells"]) == 5
    empty = concat_notebooks([])
    assert empty["cells"] == []


def test_split_by_headings() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "preamble\n"},
            {"cell_type": "markdown", "metadata": {}, "source": "# Alpha\n"},
            {"cell_type": "code", "metadata": {}, "source": "a = 1\n", "outputs": []},
            {"cell_type": "markdown", "metadata": {}, "source": "# Beta\n"},
            {"cell_type": "code", "metadata": {}, "source": "b = 2\n", "outputs": []},
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    sections = split_by_headings(notebook, level=1)
    titles = [title for title, _ in sections]
    assert titles == ["preamble", "Alpha", "Beta"]
    assert len(sections[1][1]["cells"]) == 2


def test_set_kernelspec_and_tags(sample_notebook: dict[str, Any]) -> None:
    updated = set_kernelspec(sample_notebook, name="ir", display_name="R", language="r")
    assert updated["metadata"]["kernelspec"]["name"] == "ir"
    assert updated["metadata"]["language_info"]["name"] == "r"
    tagged = add_tags(updated, 0, ["intro"])
    assert "intro" in tagged["cells"][0]["metadata"]["tags"]
    with pytest.raises(IndexError):
        add_tags(sample_notebook, 99, ["x"])
