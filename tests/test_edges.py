"""Additional edge-case tests to cover remaining operation branches."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from nbops.cells import as_mapping, cells_of, nested_mapping
from nbops.clean import clean_notebook
from nbops.convert import to_percent_python, to_script
from nbops.diff import diff_notebooks
from nbops.exceptions import InvalidNotebookError, MissingExtraError
from nbops.execute import _notebook_client_class
from nbops.inspect import compute_stats, extract_imports
from nbops.io import dumps_notebook, new_notebook, parse_notebook
from nbops.lint import lint_notebook
from nbops.models import CleanOptions
from nbops.transform import add_tags, split_by_headings


def test_lint_invalid_and_non_mapping_cell() -> None:
    report = lint_notebook({"nope": True})  # type: ignore[arg-type]
    assert any(issue.code == "NB000" for issue in report.issues)
    report = lint_notebook({"cells": ["bad"]})
    assert any(issue.code == "NB011" for issue in report.issues)


def test_lint_large_output_and_display_data() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "# Title\n",
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [
                    {
                        "output_type": "display_data",
                        "data": {"text/plain": "x" * 50},
                        "metadata": {},
                    }
                ],
                "source": "x = 1\n",
            },
        ],
        "metadata": {"kernelspec": {"name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    report = lint_notebook(notebook, max_output_chars=10)
    assert any(issue.code == "NB006" for issue in report.issues)


def test_clean_invalid_and_metadata_keys(sample_notebook: dict[str, Any]) -> None:
    with pytest.raises(ValueError, match="Invalid notebook"):
        clean_notebook({"cells": "nope"})
    sample_notebook["cells"][1]["metadata"]["collapsed"] = True
    sample_notebook["cells"][1]["metadata"]["custom"] = 1
    cleaned = clean_notebook(sample_notebook, CleanOptions(metadata_keys=["custom"]))
    assert "collapsed" not in cleaned["cells"][1]["metadata"]
    assert "custom" not in cleaned["cells"][1]["metadata"]


def test_split_level_and_add_tags_type() -> None:
    with pytest.raises(ValueError, match="Heading level"):
        split_by_headings({"cells": []}, level=0)
    notebook = {"cells": ["nope"], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    with pytest.raises(TypeError):
        add_tags(notebook, 0, ["x"])


def test_diff_insert_and_delete() -> None:
    left = {"cells": []}
    right = {"cells": [{"cell_type": "markdown", "metadata": {}, "source": "# Extra\n"}]}
    inserted = diff_notebooks(left, right)
    assert inserted.added == 1
    deleted = diff_notebooks(right, left)
    assert deleted.removed == 1


def test_parse_bytes_and_dumps_validate() -> None:
    notebook = new_notebook()
    parsed = parse_notebook(dumps_notebook(notebook).encode("utf-8"), validate=True)
    assert parsed["cells"] == []
    dumps_notebook(notebook, validate=True)


def test_execute_extra_missing() -> None:
    with pytest.raises(MissingExtraError):
        _notebook_client_class()


def test_extract_imports_skips_syntax_and_non_dict() -> None:
    notebook = {
        "cells": [
            "nope",
            {"cell_type": "code", "metadata": {}, "source": "def (\n", "outputs": []},
        ]
    }
    assert extract_imports(notebook) == []
    stats = compute_stats({"cells": ["nope"]})
    assert stats.total_cells == 1


def test_convert_empty_and_percent_blank_markdown() -> None:
    assert to_script({"cells": []}) == ""
    text = to_percent_python({"cells": [{"cell_type": "markdown", "metadata": {}, "source": ""}]})
    assert "# %% [markdown]" in text


def test_mapping_helpers() -> None:
    assert as_mapping(None) == {}
    assert (
        nested_mapping({"metadata": {"kernelspec": {"name": "py"}}}, "metadata")["kernelspec"][
            "name"
        ]
        == "py"
    )
    assert cells_of({"cells": "nope"}) == []


def test_validate_schema_failure_path() -> None:
    with pytest.raises(InvalidNotebookError):
        parse_notebook({"nbformat": 4, "nbformat_minor": 5, "cells": 1}, validate=True)


def test_iter_missing_root(tmp_path: Path) -> None:
    from nbops.batch import iter_notebooks

    assert iter_notebooks(tmp_path / "missing") == []
    lone = tmp_path / "one.ipynb"
    lone.write_text("{}", encoding="utf-8")
    assert iter_notebooks(lone) == [lone]
