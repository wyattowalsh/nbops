"""Unit tests for notebook conversion."""

from __future__ import annotations

from typing import Any

import pytest

from nbops.cells import cell_source
from nbops.convert import (
    _leading_list_literal,
    _percent_cell_metadata,
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
        assert right.get("metadata", {}).get("tags", []) == left.get("metadata", {}).get("tags", [])


def test_from_percent_python_empty_and_preamble() -> None:
    empty = from_percent_python("")
    assert empty["cells"] == []
    preamble = from_percent_python("print(1)\n")
    assert len(preamble["cells"]) == 1
    assert preamble["cells"][0]["cell_type"] == "code"
    assert "print(1)" in cell_source(preamble["cells"][0])


def test_from_percent_python_applies_jupytext_kernelspec() -> None:
    text = (
        "# ---\n"
        "# jupyter:\n"
        "#   jupytext:\n"
        "#     text_representation:\n"
        "#       format_name: percent\n"
        "#   kernelspec:\n"
        '#     display_name: "R"\n'
        "#     language: r\n"
        "#     name: ir\n"
        "#   extra:\n"
        "#     ignored: true\n"
        "# ---\n"
        "# %%\n"
        "x = 1\n"
    )
    notebook = from_percent_python(text)
    kernelspec = notebook["metadata"]["kernelspec"]
    assert kernelspec["name"] == "ir"
    assert kernelspec["display_name"] == "R"
    assert kernelspec["language"] == "r"
    assert notebook["metadata"]["language_info"]["name"] == "r"
    assert cell_source(notebook["cells"][0]).rstrip() == "x = 1"


def test_from_percent_python_ignores_inline_kernelspec_mapping() -> None:
    text = "# ---\n# kernelspec: {name: ir}\n# ---\n# %%\nprint(1)\n"
    notebook = from_percent_python(text)
    assert notebook["metadata"]["kernelspec"]["name"] == "python3"


def test_from_percent_python_ignores_kernelspec_without_name() -> None:
    text = "# ---\n# kernelspec:\n#   display_name: R\n# ---\n# %%\nprint(1)\n"
    notebook = from_percent_python(text)
    assert notebook["metadata"]["kernelspec"]["name"] == "python3"


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
    assert notebook["cells"][0]["metadata"]["tags"] == ["intro"]
    assert cell_source(notebook["cells"][1]).rstrip() == "x = 1"


def test_percent_roundtrip_preserves_tags() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {"tags": ["intro"]},
                "source": "# Hello\n",
            },
            {
                "cell_type": "code",
                "metadata": {"tags": ["setup", "hide"]},
                "source": "x = 1\n",
            },
        ]
    }
    text = to_percent_python(notebook)
    assert 'tags=["intro"]' in text
    assert 'tags=["setup", "hide"]' in text
    restored = from_percent_python(text)
    assert restored["cells"][0]["metadata"]["tags"] == ["intro"]
    assert restored["cells"][1]["metadata"]["tags"] == ["setup", "hide"]


def test_from_percent_python_parses_single_quoted_tags() -> None:
    notebook = from_percent_python("# %% tags=['active']\nprint(1)\n")
    assert notebook["cells"][0]["metadata"]["tags"] == ["active"]


def test_from_percent_python_ignores_malformed_tags() -> None:
    notebook = from_percent_python("# %% tags=[not-json\nprint(1)\n")
    assert notebook["cells"][0]["metadata"] == {}


def test_from_percent_python_ignores_non_list_tags() -> None:
    notebook = from_percent_python('# %% tags={"hide": true}\nprint(1)\n')
    assert notebook["cells"][0]["metadata"] == {}


def test_from_percent_python_parses_tags_containing_brackets() -> None:
    notebook = from_percent_python('# %% tags=["keep]me"]\nprint(1)\n')
    assert notebook["cells"][0]["metadata"]["tags"] == ["keep]me"]
    quoted = from_percent_python("# %% tags=['keep]me']\nprint(1)\n")
    assert quoted["cells"][0]["metadata"]["tags"] == ["keep]me"]


def test_from_percent_python_stringifies_non_string_tags() -> None:
    notebook = from_percent_python("# %% tags=[1, 2]\nprint(1)\n")
    assert notebook["cells"][0]["metadata"]["tags"] == ["1", "2"]


def test_from_percent_python_ignores_identifier_tags() -> None:
    notebook = from_percent_python("# %% tags=[foo]\nprint(1)\n")
    assert notebook["cells"][0]["metadata"] == {}


def test_from_percent_python_parses_escaped_quotes_in_tags() -> None:
    notebook = from_percent_python('# %% tags=["say \\"hi\\""]\nprint(1)\n')
    assert notebook["cells"][0]["metadata"]["tags"] == ['say "hi"']


def test_from_percent_python_whitespace_only_header_meta() -> None:
    notebook = from_percent_python("# %%   \nprint(1)\n")
    assert notebook["cells"][0]["cell_type"] == "code"
    assert "print(1)" in cell_source(notebook["cells"][0])


def test_to_script_skips_empty_code_cells() -> None:
    assert to_script({"cells": [{"cell_type": "code", "source": "  \n"}]}) == ""


def test_from_percent_python_treats_md_as_markdown() -> None:
    notebook = from_percent_python("# %% [md]\n# Hello\n")
    assert notebook["cells"][0]["cell_type"] == "markdown"
    assert cell_source(notebook["cells"][0]).rstrip() == "Hello"


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


def test_percent_metadata_helpers_reject_empty_and_unbalanced_lists() -> None:
    assert _percent_cell_metadata(None) == {}
    assert _percent_cell_metadata("   ") == {}
    assert _percent_cell_metadata(" key=1") == {}
    assert _leading_list_literal("[[]") is None
    notebook = from_percent_python("# %% tags=[[]\nprint(1)\n")
    assert notebook["cells"][0]["metadata"] == {}


def test_percent_metadata_rejects_non_list_decoded_tags(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("nbops.convert.json.loads", lambda _raw: {"hide": True})
    assert _percent_cell_metadata(' tags=["x"]') == {}
