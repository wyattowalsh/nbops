"""Unit tests for notebook conversion."""

from __future__ import annotations

import ast
from typing import Any

import pytest

from nbops.cells import cell_source, is_python_notebook
from nbops.convert import (
    _at_percent_metadata,
    _consume_quoted_string,
    _inline_attachment_references,
    _leading_list_literal,
    _leading_object_literal,
    _leading_scalar_literal,
    _parse_key_equal_values,
    _percent_cell_header,
    _percent_cell_id,
    _percent_cell_metadata,
    _percent_meta_item,
    convert_notebook,
    from_percent_python,
    to_markdown,
    to_percent_python,
    to_script,
)
from nbops.lint import lint_notebook


def test_percent_and_script_and_markdown(sample_notebook: dict[str, Any]) -> None:
    percent = to_percent_python(sample_notebook)
    assert percent.startswith("# ---")
    assert '#   display_name: "Python 3"' in percent
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
        assert right.get("id") == left.get("id")
        assert right.get("metadata", {}).get("tags", []) == left.get("metadata", {}).get("tags", [])
    kernelspec = restored["metadata"]["kernelspec"]
    assert kernelspec["name"] == "python3"
    assert kernelspec["display_name"] == "Python 3"
    assert kernelspec["language"] == "python"


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


def test_from_percent_python_kernelspec_parser_edges() -> None:
    text = (
        "# ---\n"
        "#\n"
        "#kernelspec:\n"
        "#\n"
        "#  name: ir\n"
        "#  argv: []\n"
        "#  bogus\n"
        "#  display_name:\n"
        "orphan-line\n"
        "# ---\n"
        "# %%\n"
        "print(1)\n"
    )
    notebook = from_percent_python(text)
    kernelspec = notebook["metadata"]["kernelspec"]
    assert kernelspec["name"] == "ir"
    assert cell_source(notebook["cells"][0]).rstrip() == "print(1)"


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
    assert all("id" not in cell for cell in restored["cells"])


def test_percent_roundtrip_preserves_attachments() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "See note\n",
                "attachments": {"note.txt": {"text/plain": "hello"}},
            }
        ]
    }
    text = to_percent_python(notebook)
    assert "attachments=" in text
    restored = from_percent_python(text)
    assert restored["cells"][0]["attachments"] == {"note.txt": {"text/plain": "hello"}}
    assert "attachments" not in restored["cells"][0]["metadata"]


def test_percent_omits_empty_attachments() -> None:
    text = to_percent_python(
        {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": "Hi\n",
                    "attachments": {},
                }
            ]
        }
    )
    assert "attachments=" not in text


def test_from_percent_promotes_metadata_attachments() -> None:
    text = '# %% [markdown] attachments={"note.txt": {"text/plain": "hello"}}\n# See note\n'
    notebook = from_percent_python(text)
    assert notebook["cells"][0]["attachments"] == {"note.txt": {"text/plain": "hello"}}
    assert "attachments" not in notebook["cells"][0]["metadata"]


def test_percent_prefers_cell_attachments_over_metadata() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {"attachments": {"meta.txt": {"text/plain": "meta"}}},
                "source": "Hi\n",
                "attachments": {"cell.txt": {"text/plain": "cell"}},
            }
        ]
    }
    text = to_percent_python(notebook)
    assert "cell.txt" in text
    assert "meta.txt" not in text
    restored = from_percent_python(text)
    assert restored["cells"][0]["attachments"] == {"cell.txt": {"text/plain": "cell"}}


def test_to_percent_skips_non_dict_attachments() -> None:
    text = to_percent_python(
        {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": "Hi\n",
                    "attachments": "nope",
                }
            ]
        }
    )
    assert "attachments=" not in text


def test_from_percent_ignores_non_dict_attachments() -> None:
    notebook = from_percent_python('# %% [markdown] attachments="nope"\n# Hi\n')
    assert "attachments" not in notebook["cells"][0]
    assert "attachments" not in notebook["cells"][0]["metadata"]


def test_percent_skips_unserializable_attachments() -> None:
    attachments: dict[str, Any] = {}
    attachments["self"] = attachments
    text = to_percent_python(
        {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": "Hi\n",
                    "attachments": attachments,
                }
            ]
        }
    )
    assert "attachments=" not in text


def _markdown_with_attachments(source: str, attachments: dict[str, Any]) -> dict[str, Any]:
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": source,
                "attachments": attachments,
            }
        ]
    }


def test_to_markdown_inlines_attachment_image() -> None:
    notebook = _markdown_with_attachments(
        "![plot](attachment:plot.png)\n",
        {"plot.png": {"image/png": "aaa"}},
    )
    markdown = to_markdown(notebook)
    assert "attachment:plot.png" not in markdown
    assert "data:image/png;base64,aaa" in markdown
    assert convert_notebook(notebook, "md").text == markdown


def test_to_markdown_inlines_attachment_slash_slash_and_title() -> None:
    notebook = _markdown_with_attachments(
        '![plot](attachment://plot.png "Plot")\n',
        {"plot.png": {"image/png": "aaa"}},
    )
    markdown = to_markdown(notebook)
    assert '![plot](data:image/png;base64,aaa "Plot")' in markdown


def test_to_markdown_leaves_unknown_attachment_ref() -> None:
    notebook = _markdown_with_attachments(
        "![missing](attachment:missing.png)\n",
        {"plot.png": {"image/png": "aaa"}},
    )
    assert "attachment:missing.png" in to_markdown(notebook)


def test_to_markdown_prefers_image_mime_over_text() -> None:
    notebook = _markdown_with_attachments(
        "![plot](attachment:plot.png)\n",
        {"plot.png": {"text/plain": "note", "image/png": "aaa"}},
    )
    markdown = to_markdown(notebook)
    assert "data:image/png;base64,aaa" in markdown
    assert "data:text/plain" not in markdown


def test_to_markdown_inlines_html_img_src() -> None:
    notebook = _markdown_with_attachments(
        '<img src="attachment:plot.png" alt="plot">\n',
        {"plot.png": {"image/png": "aaa"}},
    )
    assert '<img src="data:image/png;base64,aaa" alt="plot">' in to_markdown(notebook)


def test_to_markdown_inlines_reference_definition() -> None:
    notebook = _markdown_with_attachments(
        "![plot][fig]\n\n[fig]: attachment:plot.png\n",
        {"plot.png": {"image/png": "aaa"}},
    )
    markdown = to_markdown(notebook)
    assert "[fig]: data:image/png;base64,aaa" in markdown


def test_to_markdown_inlines_raw_cell_attachments() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "raw",
                "metadata": {},
                "source": "![plot](attachment:plot.png)\n",
                "attachments": {"plot.png": {"image/png": "aaa"}},
            }
        ]
    }
    assert "data:image/png;base64,aaa" in to_markdown(notebook)


def test_to_markdown_does_not_rewrite_code_cells() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "metadata": {},
                "source": 'print("attachment:plot.png")\n',
                "attachments": {"plot.png": {"image/png": "aaa"}},
            }
        ]
    }
    markdown = to_markdown(notebook)
    assert "attachment:plot.png" in markdown
    assert "data:image/png" not in markdown


def test_to_markdown_inlines_list_payload_and_url_encoded_name() -> None:
    notebook = _markdown_with_attachments(
        "![plot](attachment:my%20plot.png)\n",
        {"my plot.png": {"image/png": ["aa", "a"]}},
    )
    assert "data:image/png;base64,aaa" in to_markdown(notebook)


def test_to_markdown_inlines_svg_text_payload() -> None:
    svg = "<svg xmlns='http://www.w3.org/2000/svg'></svg>"
    notebook = _markdown_with_attachments(
        "![mark](attachment:mark.svg)\n",
        {"mark.svg": {"image/svg+xml": svg}},
    )
    markdown = to_markdown(notebook)
    assert "data:image/svg+xml;charset=utf-8," in markdown
    assert "attachment:mark.svg" not in markdown


def test_to_markdown_uses_metadata_attachments_fallback() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {"attachments": {"plot.png": {"image/png": "aaa"}}},
                "source": "![plot](attachment:plot.png)\n",
            }
        ]
    }
    assert "data:image/png;base64,aaa" in to_markdown(notebook)


def test_to_markdown_skips_non_dict_attachments() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "![plot](attachment:plot.png)\n",
                "attachments": "nope",
            }
        ]
    }
    assert "attachment:plot.png" in to_markdown(notebook)


def test_percent_keeps_attachment_refs_in_source() -> None:
    notebook = _markdown_with_attachments(
        "![plot](attachment:plot.png)\n",
        {"plot.png": {"image/png": "aaa"}},
    )
    text = to_percent_python(notebook)
    assert "attachment:plot.png" in text
    assert "data:image/png" not in text


def test_to_markdown_attachment_payload_and_lookup_edges() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": "nope",
                "source": (
                    "![a](attachment:folder/a.png)\n"
                    "![b](attachment:b.png)\n"
                    "![c](attachment:c.png)\n"
                    "![empty](attachment:empty.png)\n"
                    "![space](attachment:space.png)\n"
                    "![skip](attachment:skip.png)\n"
                    '<img src="attachment:missing.png">\n'
                    "[fig]: attachment:missing.png\n"
                ),
                "attachments": {
                    "folder/a.png": {"image/png": "aaa"},
                    "b.png": {"image/png": 123, "text/plain": "bbb"},
                    "c.png": {"image/png": "data:image/png;base64,ccc"},
                    "empty.png": {"image/png": ""},
                    "space.png": {"image/png": " \n "},
                    "skip.png": {},
                    "": {"image/png": "nope"},
                    1: {"image/png": "nope"},
                    "not-bundle.png": "nope",
                },
            }
        ]
    }
    markdown = to_markdown(notebook)
    assert "data:image/png;base64,aaa" in markdown
    assert "data:text/plain;base64,bbb" in markdown
    assert "data:image/png;base64,ccc" in markdown
    assert "attachment:empty.png" in markdown
    assert "attachment:space.png" in markdown
    assert "attachment:skip.png" in markdown
    assert 'src="attachment:missing.png"' in markdown
    assert "[fig]: attachment:missing.png" in markdown
    assert _inline_attachment_references("", {"plot.png": {"image/png": "aaa"}}) == ""


def test_to_markdown_inlines_code_cell_output_images() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "metadata": {},
                "source": "plot()\n",
                "outputs": [
                    "nope",
                    {"output_type": "stream", "name": "stdout", "text": "hi\n"},
                    {
                        "output_type": "display_data",
                        "data": {"text/plain": "<Figure>", "image/png": "aaa"},
                        "metadata": {},
                    },
                    {
                        "output_type": "execute_result",
                        "data": {"image/svg+xml": "<svg></svg>"},
                        "metadata": {},
                        "execution_count": 1,
                    },
                    {"output_type": "display_data", "data": {"text/plain": "1"}, "metadata": {}},
                    {"output_type": "display_data", "data": "nope", "metadata": {}},
                ],
            }
        ]
    }
    markdown = to_markdown(notebook)
    assert "```python\nplot()\n```" in markdown
    assert "    hi" in markdown
    assert "![output-0](data:image/png;base64,aaa)" in markdown
    assert "![output-1](data:image/svg+xml;charset=utf-8," in markdown
    assert markdown.count("![output-") == 2
    assert "<Figure>" not in markdown
    assert "    1" in markdown


def test_to_markdown_skips_code_cell_without_output_list() -> None:
    notebook = {
        "cells": [{"cell_type": "code", "metadata": {}, "source": "x = 1\n", "outputs": None}]
    }
    markdown = to_markdown(notebook)
    assert "```python" in markdown
    assert "![output-" not in markdown


def test_to_markdown_includes_stream_error_and_markdown_outputs() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "metadata": {},
                "source": "print(1)\n",
                "outputs": [
                    {"output_type": "stream", "name": "stdout", "text": ["hello\n", "world\n"]},
                    {"output_type": "stream", "name": "stderr", "text": ""},
                    {"output_type": "stream", "name": "stdout", "text": 123},
                    {"output_type": "update_display_data"},
                    {
                        "output_type": "display_data",
                        "data": {"text/markdown": "  ", "text/plain": "\n"},
                        "metadata": {},
                    },
                    {"output_type": "error", "ename": "", "evalue": "", "traceback": ["\n"]},
                    {
                        "output_type": "error",
                        "ename": "ValueError",
                        "evalue": "bad",
                        "traceback": ["\x1b[31mValueError\x1b[0m: bad"],
                    },
                    {
                        "output_type": "execute_result",
                        "data": {"text/markdown": "**ok**\n"},
                        "metadata": {},
                        "execution_count": 1,
                    },
                ],
            }
        ]
    }
    markdown = to_markdown(notebook)
    assert "    hello" in markdown
    assert "    world" in markdown
    assert "    ValueError: bad" in markdown
    assert "\x1b" not in markdown
    assert "**ok**" in markdown
    assert "123" not in markdown


def test_to_markdown_error_without_traceback_uses_ename() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "metadata": {},
                "source": "raise\n",
                "outputs": [
                    {
                        "output_type": "error",
                        "ename": "RuntimeError",
                        "evalue": "boom",
                        "traceback": [],
                    },
                    {"output_type": "error"},
                ],
            }
        ]
    }
    markdown = to_markdown(notebook)
    assert "    RuntimeError: boom" in markdown
    assert "    Error" in markdown


def test_to_markdown_ignores_empty_metadata_attachments() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {"attachments": {}},
                "source": "![p](attachment:plot.png)\n",
            },
            {
                "cell_type": "markdown",
                "metadata": "nope",
                "source": "![q](attachment:plot.png)\n",
            },
        ]
    }
    markdown = to_markdown(notebook)
    assert markdown.count("attachment:plot.png") == 2


def test_percent_roundtrip_preserves_omitted_cell_ids() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "# Hello\n"},
            {"cell_type": "code", "metadata": {}, "source": "x = 1\n"},
        ]
    }
    text = to_percent_python(notebook)
    assert "id=" not in text
    restored = from_percent_python(text)
    assert all("id" not in cell for cell in restored["cells"])
    codes = {issue.code for issue in lint_notebook(restored).issues}
    assert "NB009" in codes


def test_from_percent_python_parses_header_ids() -> None:
    notebook = from_percent_python(
        '# %% [markdown] id="title" tags=["intro"]\n# Hello\n\n# %% id=area\nprint(1)\n'
    )
    assert notebook["cells"][0]["id"] == "title"
    assert notebook["cells"][0]["metadata"]["tags"] == ["intro"]
    assert notebook["cells"][1]["id"] == "area"
    quoted = from_percent_python("# %% id='cell-1'\nprint(1)\n")
    assert quoted["cells"][0]["id"] == "cell-1"


def test_from_percent_python_ignores_malformed_ids() -> None:
    unclosed = from_percent_python('# %% id="nope\nprint(1)\n')
    assert "id" not in unclosed["cells"][0]
    invalid_escape = from_percent_python('# %% id="\\xzz"\nprint(1)\n')
    assert "id" not in invalid_escape["cells"][0]
    empty = from_percent_python('# %% id=""\nprint(1)\n')
    assert "id" not in empty["cells"][0]
    mapping = from_percent_python("# %% id={not: scalar}\nprint(1)\n")
    assert "id" not in mapping["cells"][0]


def test_from_percent_python_parses_jupytext_cell_titles() -> None:
    notebook = from_percent_python(
        '# %% My Title [markdown] tags=["intro"]\n# Hello\n\n# %% Plot\nprint(1)\n'
    )
    assert notebook["cells"][0]["cell_type"] == "markdown"
    assert notebook["cells"][0]["metadata"]["title"] == "My Title"
    assert notebook["cells"][0]["metadata"]["tags"] == ["intro"]
    assert notebook["cells"][1]["cell_type"] == "code"
    assert notebook["cells"][1]["metadata"]["title"] == "Plot"


def test_percent_roundtrip_preserves_cell_titles() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "t",
                "metadata": {"title": "Intro", "tags": ["intro"]},
                "source": "# Hello\n",
            },
            {
                "cell_type": "code",
                "metadata": {"title": "Plot"},
                "source": "print(1)\n",
            },
        ]
    }
    text = to_percent_python(notebook)
    assert "# %% Intro [markdown]" in text
    assert "# %% Plot" in text
    restored = from_percent_python(text)
    assert restored["cells"][0]["cell_type"] == "markdown"
    assert restored["cells"][0]["metadata"]["title"] == "Intro"
    assert restored["cells"][0]["id"] == "t"
    assert restored["cells"][1]["metadata"]["title"] == "Plot"


def test_percent_title_helpers_reject_unsafe_and_non_string_titles() -> None:
    from nbops.convert import _percent_title_text

    assert _percent_title_text(None) is None
    assert _percent_title_text("  ") is None
    assert _percent_title_text("bad[title]") is None
    assert _percent_title_text("a=b") is None
    unsafe = _percent_cell_header(
        {"cell_type": "code", "metadata": {"title": "bad=title"}, "source": "x"}
    )
    assert unsafe == '# %% title="bad=title"'
    numbered = _percent_cell_header({"cell_type": "code", "metadata": {"title": 12}, "source": "x"})
    assert numbered == "# %% title=12"
    missing = _percent_cell_header({"cell_type": "code", "metadata": None, "source": "x"})
    assert missing == "# %%"


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


def test_to_script_strips_ipython_magics_and_skips_cell_magics() -> None:
    notebook = {
        "metadata": {"language_info": {"name": "python"}},
        "cells": [
            {"cell_type": "code", "source": "%matplotlib inline\nimport os\n"},
            {"cell_type": "code", "source": "%%bash\necho hi\n"},
            {"cell_type": "code", "source": "%pwd\n"},
            {"cell_type": "code", "source": "x = %time 1 + 1\n"},
        ],
    }
    script = to_script(notebook)
    assert script == "import os\n\nx = 1 + 1\n"
    assert "%matplotlib" not in script
    assert "echo hi" not in script
    ast.parse(script)


def test_percent_convert_keeps_ipython_magics() -> None:
    notebook = {
        "metadata": {"language_info": {"name": "python"}},
        "cells": [{"cell_type": "code", "source": "%matplotlib inline\nimport os\n"}],
    }
    percent = to_percent_python(notebook)
    assert "%matplotlib inline" in percent
    assert "import os" in percent


def test_to_script_leaves_non_python_notebooks_unchanged() -> None:
    notebook = {
        "metadata": {"kernelspec": {"name": "ir", "language": "r"}},
        "cells": [{"cell_type": "code", "source": "library(ggplot2)\n"}],
    }
    assert to_script(notebook) == "library(ggplot2)\n"


def test_to_script_infers_r_from_kernelspec_name() -> None:
    notebook = {
        "metadata": {"kernelspec": {"name": "ir"}},
        "cells": [{"cell_type": "code", "source": "library(ggplot2)\n"}],
    }
    assert to_script(notebook) == "library(ggplot2)\n"


def test_to_markdown_uses_declared_code_language() -> None:
    notebook = {
        "metadata": {"kernelspec": {"name": "ir"}},
        "cells": [{"cell_type": "code", "source": "library(ggplot2)\n"}],
    }
    markdown = to_markdown(notebook)
    assert "```r\n" in markdown
    assert "library(ggplot2)" in markdown
    assert "```python" not in markdown


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


def test_percent_front_matter_without_cells() -> None:
    text = to_percent_python(
        {"metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3"}}, "cells": []}
    )
    assert text.startswith("# ---")
    assert "# kernelspec:" in text
    assert "# %%" not in text


def test_percent_roundtrip_preserves_non_python_kernelspec() -> None:
    notebook = {
        "metadata": {
            "kernelspec": {
                "name": "ir",
                "display_name": "R",
                "language": "r",
            }
        },
        "cells": [{"cell_type": "code", "metadata": {}, "source": "x <- 1\n"}],
    }
    text = to_percent_python(notebook)
    assert text.startswith("# ---")
    assert "# kernelspec:" in text
    assert "#   name: ir" in text
    assert '#   display_name: "R"' in text or "#   display_name: R" in text
    assert "#   language: r" in text
    restored = from_percent_python(text)
    kernelspec = restored["metadata"]["kernelspec"]
    assert kernelspec["name"] == "ir"
    assert kernelspec["display_name"] == "R"
    assert kernelspec["language"] == "r"
    assert restored["metadata"]["language_info"]["name"] == "r"
    assert cell_source(restored["cells"][0]).rstrip() == "x <- 1"


def test_percent_roundtrip_infers_language_from_kernelspec_name() -> None:
    notebook = {
        "metadata": {"kernelspec": {"name": "ir"}},
        "cells": [{"cell_type": "code", "metadata": {}, "source": "library(ggplot2)\n"}],
    }
    text = to_percent_python(notebook)
    assert "#   name: ir" in text
    assert "#   language: r" in text
    restored = from_percent_python(text)
    assert restored["metadata"]["kernelspec"]["name"] == "ir"
    assert restored["metadata"]["kernelspec"]["language"] == "r"
    assert restored["metadata"]["language_info"]["name"] == "r"
    assert is_python_notebook(restored) is False
    assert to_script(restored) == "library(ggplot2)\n"


def test_percent_roundtrip_language_info_without_kernelspec_name() -> None:
    notebook = {
        "metadata": {"language_info": {"name": "r"}},
        "cells": [{"cell_type": "code", "metadata": {}, "source": "library(ggplot2)\n"}],
    }
    text = to_percent_python(notebook)
    assert "language_info:" in text
    assert "#   name: r" in text
    assert "kernelspec:" not in text
    restored = from_percent_python(text)
    assert restored["metadata"]["language_info"]["name"] == "r"
    assert is_python_notebook(restored) is False
    assert to_script(restored) == "library(ggplot2)\n"


def test_from_percent_python_applies_nested_language_info() -> None:
    text = "# ---\n# jupyter:\n#   language_info:\n#     name: r\n# ---\n# %%\nlibrary(ggplot2)\n"
    notebook = from_percent_python(text)
    assert notebook["metadata"]["language_info"]["name"] == "r"
    assert to_script(notebook) == "library(ggplot2)\n"


def test_from_percent_python_ignores_inline_language_info() -> None:
    text = "# ---\n# language_info: {name: r}\n# ---\n# %%\nprint(1)\n"
    notebook = from_percent_python(text)
    assert notebook["metadata"]["language_info"]["name"] == "python"


def test_from_percent_uses_language_info_when_kernelspec_language_omitted() -> None:
    text = (
        "# ---\n"
        "# kernelspec:\n"
        "#   name: mystery\n"
        "# language_info:\n"
        "#   name: r\n"
        "# ---\n"
        "# %%\n"
        "library(ggplot2)\n"
    )
    notebook = from_percent_python(text)
    assert notebook["metadata"]["kernelspec"]["name"] == "mystery"
    assert notebook["metadata"]["kernelspec"]["language"] == "r"
    assert notebook["metadata"]["language_info"]["name"] == "r"


def test_percent_omits_kernelspec_yaml_without_name() -> None:
    text = to_percent_python(
        {
            "metadata": {"kernelspec": {"display_name": "Python 3"}},
            "cells": [{"cell_type": "code", "metadata": {}, "source": "x = 1\n"}],
        }
    )
    assert "kernelspec:" not in text
    assert text.startswith("# %%")


def test_percent_kernelspec_yaml_skips_blank_and_non_string_fields() -> None:
    text = to_percent_python(
        {
            "metadata": {
                "kernelspec": {"name": "python3", "display_name": "", "language": 3},
            },
            "cells": [{"cell_type": "code", "metadata": {}, "source": "x = 1\n"}],
        }
    )
    assert "#   name: python3" in text
    assert "display_name:" not in text
    assert "language:" not in text


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
    assert _percent_cell_metadata(" key=1") == {"key": 1}
    assert _percent_cell_id(None) is None
    assert _percent_cell_id("   ") is None
    assert _percent_cell_id(" key=1") is None
    assert _percent_cell_id(" id=12") == "12"
    assert _percent_cell_id(" id=true") is None
    assert _percent_cell_id(' {"id": "cell-1"}') == "cell-1"
    assert _leading_list_literal("[[]") is None
    assert _leading_object_literal("{") is None
    assert _leading_object_literal("x") is None
    assert _leading_scalar_literal("") is None
    assert _leading_scalar_literal("   ") is None
    assert _leading_scalar_literal("'unterminated") is None
    assert _leading_scalar_literal('"hello"') == "hello"
    assert _leading_scalar_literal("area") == "area"
    assert _leading_scalar_literal("!!!") is None
    assert _at_percent_metadata("", 0) is False
    assert _parse_key_equal_values("collapsed=true  ") == {"collapsed": True}
    notebook = from_percent_python("# %% tags=[[]\nprint(1)\n")
    assert notebook["cells"][0]["metadata"] == {}


def test_percent_metadata_rejects_non_list_decoded_tags(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("nbops.convert.json.loads", lambda _raw: {"hide": True})
    assert _percent_cell_metadata(' tags=["x"]') == {}


def test_percent_id_rejects_non_string_decoded_scalar(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("nbops.convert.json.loads", lambda _raw: 12)
    assert _leading_scalar_literal('"x"') is None


def test_from_percent_python_parses_generic_key_value_metadata() -> None:
    notebook = from_percent_python(
        '# %% [markdown] collapsed=true slideshow={"slide_type": "slide"} '
        'foo.bar=1 tags=["intro"]\n# Hello\n'
    )
    metadata = notebook["cells"][0]["metadata"]
    assert notebook["cells"][0]["cell_type"] == "markdown"
    assert metadata["collapsed"] is True
    assert metadata["slideshow"] == {"slide_type": "slide"}
    assert metadata["foo.bar"] == 1
    assert metadata["tags"] == ["intro"]
    assert "id" not in notebook["cells"][0]


def test_from_percent_python_parses_json_cell_metadata() -> None:
    notebook = from_percent_python(
        '# %% [markdown] {"tags": ["intro"], "collapsed": true, "id": "title"}\n# Hello\n'
    )
    cell = notebook["cells"][0]
    assert cell["cell_type"] == "markdown"
    assert cell["id"] == "title"
    assert cell["metadata"]["tags"] == ["intro"]
    assert cell["metadata"]["collapsed"] is True
    assert "id" not in cell["metadata"]
    listed = from_percent_python("# %% [markdown] [1, 2]\n# Hello\n")
    assert listed["cells"][0]["cell_type"] == "code"
    assert "# %% [markdown] [1, 2]" in cell_source(listed["cells"][0])
    not_dict = from_percent_python("# %% {1, 2}\nprint(1)\n")
    assert not_dict["cells"][0]["metadata"] == {}
    unclosed = from_percent_python('# %% {"tags": ["intro"]\nprint(1)\n')
    assert unclosed["cells"][0]["metadata"] == {}


def test_from_percent_python_parses_title_then_key_value_metadata() -> None:
    notebook = from_percent_python("# %% Plot collapsed=true\nprint(1)\n")
    assert notebook["cells"][0]["cell_type"] == "code"
    assert notebook["cells"][0]["metadata"]["title"] == "Plot"
    assert notebook["cells"][0]["metadata"]["collapsed"] is True
    attached = from_percent_python("# %% Plot[markdown]\n# Hello\n")
    assert attached["cells"][0]["cell_type"] == "markdown"
    assert attached["cells"][0]["metadata"]["title"] == "Plot"


def test_from_percent_python_ignores_trailing_non_metadata_tokens() -> None:
    notebook = from_percent_python("# %% collapsed=true oops\nprint(1)\n")
    assert notebook["cells"][0]["metadata"] == {"collapsed": True}
    leftover = from_percent_python("# %% collapsed=true $foo\nprint(1)\n")
    assert leftover["cells"][0]["metadata"] == {"collapsed": True}
    unclosed = from_percent_python("# %% slideshow={\nprint(1)\n")
    assert unclosed["cells"][0]["metadata"] == {}
    unsafe_title = from_percent_python("# %% foo [has space]\nprint(1)\n")
    assert "# %% foo [has space]" in cell_source(unsafe_title["cells"][0])


def test_from_percent_python_parses_title_key_value() -> None:
    notebook = from_percent_python('# %% title="Intro" collapsed=false\nprint(1)\n')
    assert notebook["cells"][0]["cell_type"] == "code"
    assert notebook["cells"][0]["metadata"]["title"] == "Intro"
    assert notebook["cells"][0]["metadata"]["collapsed"] is False


def test_percent_roundtrip_preserves_generic_cell_metadata() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "t",
                "metadata": {
                    "title": "Intro",
                    "tags": ["intro"],
                    "collapsed": True,
                    "slideshow": {"slide_type": "slide"},
                },
                "source": "# Hello\n",
            },
            {
                "cell_type": "code",
                "metadata": {"title": "a=b", "name": "plot"},
                "source": "print(1)\n",
            },
        ]
    }
    text = to_percent_python(notebook)
    assert "# %% Intro [markdown]" in text
    assert "collapsed=true" in text
    assert "slideshow=" in text
    assert 'title="a=b"' in text
    assert 'name="plot"' in text
    restored = from_percent_python(text)
    right = restored["cells"][0]["metadata"]
    assert right["title"] == "Intro"
    assert right["tags"] == ["intro"]
    assert right["collapsed"] is True
    assert right["slideshow"] == {"slide_type": "slide"}
    assert restored["cells"][0]["id"] == "t"
    assert restored["cells"][1]["metadata"]["title"] == "a=b"
    assert restored["cells"][1]["metadata"]["name"] == "plot"
    assert "id" not in restored["cells"][1]


def test_percent_header_skips_unserializable_and_invalid_metadata_keys() -> None:
    header = _percent_cell_header(
        {
            "cell_type": "code",
            "metadata": {"ok": 1, "bad": {1, 2}, "not a key": True},
            "source": "x",
        }
    )
    assert "ok=1" in header
    assert "bad=" not in header
    assert "not a key" not in header


def test_from_percent_python_ignores_non_header_percent_lookalikes() -> None:
    glued = from_percent_python("# %%foo\nprint(1)\n")
    assert glued["cells"][0]["cell_type"] == "code"
    assert "# %%foo" in cell_source(glued["cells"][0])
    junk = from_percent_python("# %% [markdown] Hello\nprint(1)\n")
    source = cell_source(junk["cells"][0])
    assert "# %% [markdown] Hello" in source
    assert "print(1)" in source
    assert junk["cells"][0]["cell_type"] == "code"


def test_from_percent_python_parses_spaces_around_metadata_equals() -> None:
    notebook = from_percent_python("# %% collapsed = true\nprint(1)\n")
    assert notebook["cells"][0]["metadata"]["collapsed"] is True
    empty_value = from_percent_python("# %% key=\nprint(1)\n")
    assert empty_value["cells"][0]["metadata"] == {}
    odd_value = from_percent_python("# %% key=$\nprint(1)\n")
    assert odd_value["cells"][0]["metadata"] == {}


def test_percent_header_skips_circular_metadata_values() -> None:
    cyclic: dict[str, Any] = {}
    cyclic["self"] = cyclic
    header = _percent_cell_header(
        {"cell_type": "code", "metadata": {"loop": cyclic, "ok": False}, "source": "x"}
    )
    assert "ok=false" in header
    assert "loop=" not in header
    assert _percent_meta_item("ok", True) == "ok=true"
    assert _consume_quoted_string("", 0) is None
    assert _consume_quoted_string("x", 0) is None
