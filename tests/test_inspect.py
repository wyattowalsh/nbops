"""Unit tests for nbops.inspect and core compatibility exports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from nbops.core import NotebookStats, compute_stats, load_notebook, stats_for_file
from nbops.inspect import extract_imports, list_outputs, outline


def test_compute_stats_counts_cells(sample_notebook: dict[str, Any]) -> None:
    result = compute_stats(sample_notebook)
    assert isinstance(result, NotebookStats)
    assert result.total_cells == 4
    assert result.code_cells == 2
    assert result.markdown_cells == 1
    assert result.raw_cells == 1


def test_compute_stats_counts_non_empty_code_lines(sample_notebook: dict[str, Any]) -> None:
    result = compute_stats(sample_notebook)
    assert result.code_lines == 4
    assert result.markdown_lines == 2
    assert result.executed_code_cells == 1
    assert result.stream_outputs == 1
    assert result.tags == ["setup"]
    assert result.kernel_name == "python3"
    assert result.nbformat_major == 4


def test_compute_stats_reads_metadata(sample_notebook: dict[str, Any]) -> None:
    result = compute_stats(sample_notebook)
    assert result.kernel == "Python 3"
    assert result.language == "python"


def test_compute_stats_empty_cells_and_widgets(sample_notebook: dict[str, Any]) -> None:
    sample_notebook["cells"].append(
        {"cell_type": "code", "id": "empty", "metadata": {}, "source": "", "outputs": []}
    )
    sample_notebook["metadata"]["widgets"] = {"state": {"x": {}}}
    result = compute_stats(sample_notebook)
    assert result.empty_cells == 1
    assert result.has_widgets is True


def test_compute_stats_empty_notebook() -> None:
    result = compute_stats({"cells": []})
    assert result.total_cells == 0
    assert result.code_lines == 0
    assert result.kernel is None
    assert result.language is None


def test_compute_stats_infers_language_from_kernelspec_name() -> None:
    result = compute_stats({"cells": [], "metadata": {"kernelspec": {"name": "ir"}}})
    assert result.kernel_name == "ir"
    assert result.language == "r"


def test_compute_stats_does_not_let_python_language_info_hide_ir() -> None:
    result = compute_stats(
        {
            "cells": [],
            "metadata": {
                "kernelspec": {"name": "ir"},
                "language_info": {"name": "python"},
            },
        }
    )
    assert result.language == "r"


@pytest.mark.parametrize("bad", [None, {}, {"cells": "nope"}, [], 42])
def test_compute_stats_rejects_invalid(bad: Any) -> None:
    with pytest.raises(ValueError, match="Invalid notebook"):
        compute_stats(bad)


def test_load_and_stats_for_file(sample_notebook_file: Path) -> None:
    loaded = load_notebook(sample_notebook_file, validate=False)
    assert loaded["nbformat"] == 4
    result = stats_for_file(sample_notebook_file)
    assert result.total_cells == 4


def test_outline_and_imports(sample_notebook: dict[str, Any]) -> None:
    headings = outline(sample_notebook)
    assert headings[0].level == 1
    assert headings[0].title == "Title"
    imports = extract_imports(sample_notebook)
    assert imports[0].module == "os"
    assert imports[0].cell_index == 1


def test_extract_imports_from_import(sample_notebook: dict[str, Any]) -> None:
    sample_notebook["cells"][2]["source"] = "from pathlib import Path, PurePath\n"
    imports = extract_imports(sample_notebook)
    modules = {item.module for item in imports}
    assert "os" in modules
    assert "pathlib" in modules


def test_extract_imports_skips_magics_and_non_python_cells() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "metadata": {},
                "source": (
                    "%matplotlib inline\n"
                    "import pandas as pd\n"
                    "from os import path as p\n"
                    "from . import util\n"
                ),
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": "import os\nawait fetch()\n",
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": "%%bash\necho hi\nimport should_ignore\n",
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": "def (\n",
            },
        ]
    }
    imports = extract_imports(notebook)
    assert [item.module for item in imports] == ["pandas", "os", "", "os"]
    assert imports[0].raw == "import pandas as pd"
    assert imports[1].names == ["p"]
    assert imports[2].names == ["util"]
    assert imports[3].raw == "import os"


def test_extract_imports_skips_non_python_notebooks() -> None:
    notebook = {
        "metadata": {"kernelspec": {"name": "ir", "language": "r"}},
        "cells": [
            {
                "cell_type": "code",
                "metadata": {},
                "source": "import should_ignore\n",
            }
        ],
    }
    assert extract_imports(notebook) == []


def test_extract_imports_skips_ir_kernelspec_name_without_language() -> None:
    notebook = {
        "metadata": {"kernelspec": {"name": "ir"}},
        "cells": [{"cell_type": "code", "metadata": {}, "source": "import should_ignore\n"}],
    }
    assert extract_imports(notebook) == []


def test_extract_imports_skips_when_parse_returns_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("nbops.inspect.parse_code_cell", lambda _source: None)
    notebook = {"cells": [{"cell_type": "code", "metadata": {}, "source": "import os\n"}]}
    assert extract_imports(notebook) == []


def test_list_outputs_stream_and_error(
    sample_notebook: dict[str, Any], error_notebook: dict[str, Any]
) -> None:
    outputs = list_outputs(sample_notebook)
    assert len(outputs) == 1
    assert outputs[0].output_type == "stream"
    assert outputs[0].name == "stdout"
    assert outputs[0].cell_index == 1
    assert outputs[0].size > 0

    errors = list_outputs(error_notebook)
    assert errors[0].output_type == "error"
    assert errors[0].name == "ValueError"
    assert errors[0].preview is not None

    display_notebook = {
        "cells": [
            {
                "cell_type": "code",
                "metadata": {},
                "source": "x",
                "outputs": [
                    {
                        "output_type": "execute_result",
                        "data": {"text/plain": "42"},
                        "metadata": {},
                    },
                    "skip-me",
                ],
            }
        ]
    }
    display = list_outputs(display_notebook)
    assert display[0].output_type == "execute_result"
    assert display[0].preview == "42"
    empty_output = list_outputs(
        {"cells": [{"cell_type": "code", "metadata": {}, "source": "x", "outputs": [{}]}]}
    )
    assert empty_output[0].preview is None
    stats = compute_stats(error_notebook)
    assert stats.error_outputs == 1
    assert compute_stats(display_notebook).display_outputs == 1


def test_compute_stats_unknown_cell_and_output_types() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "# T\n"},
            {"cell_type": "raw", "metadata": {}, "source": "raw\n"},
            {"cell_type": "unknown", "metadata": {}, "source": "skip\n"},
            {
                "cell_type": "code",
                "metadata": {},
                "source": "x\n",
                "outputs": [
                    {"output_type": "error", "ename": "E", "evalue": "x"},
                    {"output_type": "stream", "name": "stdout", "text": "hi"},
                    {"output_type": "display_data", "data": {"text/plain": "1"}},
                    {"output_type": "update_display_data", "data": {"text/plain": "2"}},
                ],
            },
        ]
    }
    stats = compute_stats(notebook)
    assert stats.markdown_cells == 1
    assert stats.raw_cells == 1
    assert stats.code_cells == 1
    assert stats.error_outputs == 1
    assert stats.stream_outputs == 1
    assert stats.display_outputs == 1


def test_list_outputs_fallbacks_and_non_list() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "# T\n"},
            {"cell_type": "code", "metadata": {}, "source": "x\n", "outputs": "nope"},
            {
                "cell_type": "code",
                "metadata": {},
                "source": "y\n",
                "outputs": [
                    {"output_type": "stream", "text": "hi"},
                    {"output_type": "error"},
                    {
                        "output_type": "display_data",
                        "data": {"text/html": ["<b>x</b>"]},
                    },
                    {"output_type": "display_data", "data": {"image/png": "abc"}},
                    {"text": ["z"]},
                ],
            },
        ]
    }
    records = list_outputs(notebook)
    assert records[0].name == "stdout"
    assert records[1].name == "error"
    assert records[2].preview == "<b>x</b>"
    assert "abc" in (records[3].preview or "")
    assert records[4].output_type == "unknown"
