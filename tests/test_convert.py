"""Unit tests for notebook conversion."""

from __future__ import annotations

from typing import Any

import pytest

from nbops.cells import cell_source
from nbops.convert import (
    convert_notebook,
    from_percent_python,
    to_markdown,
    to_percent_python,
    to_script,
)


def test_percent_and_script_and_markdown(sample_notebook: dict[str, Any]) -> None:
    percent = to_percent_python(sample_notebook)
    assert "# %% [markdown]" in percent
    assert "# %%" in percent
    assert "import os" in percent
    script = to_script(sample_notebook)
    assert "import os" in script
    assert "# Title" not in script
    markdown = to_markdown(sample_notebook)
    assert "# Title" in markdown
    assert "```python" in markdown


def test_convert_notebook_formats(sample_notebook: dict[str, Any]) -> None:
    assert convert_notebook(sample_notebook, "py").format == "py"
    assert convert_notebook(sample_notebook, "script").format == "script"
    assert convert_notebook(sample_notebook, "md").format == "md"
    with pytest.raises(ValueError, match="Unsupported"):
        convert_notebook(sample_notebook, "pdf")


def test_percent_roundtrip_preserves_cell_types_and_source(sample_notebook: dict[str, Any]) -> None:
    restored = from_percent_python(to_percent_python(sample_notebook))
    original_cells = sample_notebook["cells"]
    assert len(restored["cells"]) == len(original_cells)
    for left, right in zip(original_cells, restored["cells"], strict=True):
        assert left["cell_type"] == right["cell_type"]
        assert cell_source(left).rstrip() == cell_source(right).rstrip()
        assert isinstance(right.get("id"), str) and right["id"]


def test_from_percent_python_empty_and_preamble() -> None:
    empty = from_percent_python("")
    assert empty["cells"] == []
    preamble = from_percent_python("print(1)\n")
    assert len(preamble["cells"]) == 1
    assert preamble["cells"][0]["cell_type"] == "code"
    assert "print(1)" in cell_source(preamble["cells"][0])


def test_from_percent_python_skips_jupytext_front_matter() -> None:
    text = (
        "\n"
        "# ---\n"
        "# jupyter:\n"
        "#   jupytext:\n"
        "#     text_representation:\n"
        "#       format_name: percent\n"
        "# ---\n"
        "\n"
        '# %% [markdown] tags=["intro"]\n'
        "# Hello\n"
        "\n"
        "# %%\n"
        "x = 1\n"
    )
    notebook = from_percent_python(text)
    assert [cell["cell_type"] for cell in notebook["cells"]] == ["markdown", "code"]
    assert cell_source(notebook["cells"][0]).rstrip() == "Hello"
    assert cell_source(notebook["cells"][1]).rstrip() == "x = 1"


def test_unquote_keeps_uncommented_markdown_lines() -> None:
    notebook = from_percent_python("# %% [markdown]\nHello\n#\n# world\n")
    source = cell_source(notebook["cells"][0])
    assert "Hello" in source
    assert "world" in source


def test_from_percent_python_keeps_unclosed_front_matter() -> None:
    text = "# ---\njupyter: true\nprint(1)\n"
    notebook = from_percent_python(text)
    assert notebook["cells"][0]["cell_type"] == "code"
    assert "print(1)" in cell_source(notebook["cells"][0])


def test_jupytext_front_matter_without_trailing_newline() -> None:
    text = "# ---\n# jupyter: true\n# ---\n# %%\nx = 1"
    notebook = from_percent_python(text)
    assert cell_source(notebook["cells"][0]).rstrip() == "x = 1"


def test_empty_notebook_conversions() -> None:
    empty = {"cells": []}
    assert to_percent_python(empty) == ""
    assert to_script(empty) == ""
    assert to_markdown(empty) == ""


def test_empty_markdown_raw_and_code_cells_roundtrip() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "source": "", "metadata": {}},
            {"cell_type": "raw", "source": "", "metadata": {}},
            {"cell_type": "code", "source": "", "metadata": {}},
        ]
    }
    restored = from_percent_python(to_percent_python(notebook))
    assert [cell["cell_type"] for cell in restored["cells"]] == ["markdown", "raw", "code"]
    markdown = to_markdown(notebook)
    assert "```python" in markdown


def test_convert_skips_non_mapping_cells() -> None:
    notebook = {"cells": ["nope", {"cell_type": "code", "source": "x = 1\n"}]}
    percent = to_percent_python(notebook)
    assert "# %%\nx = 1" in percent
    assert to_script(notebook).strip() == "x = 1"
    markdown = to_markdown(notebook)
    assert "```python" in markdown
