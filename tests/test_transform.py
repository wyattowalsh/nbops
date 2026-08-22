"""Unit tests for notebook transforms."""

from __future__ import annotations

from typing import Any

import pytest

from nbops.lint import lint_notebook
from nbops.transform import (
    add_tags,
    concat_notebooks,
    ensure_cell_ids,
    filter_cells,
    remove_tags,
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
    assert "id" not in merged["cells"][-1]
    empty = concat_notebooks([])
    assert empty["cells"] == []


def test_concat_assigns_unique_cell_ids(sample_notebook: dict[str, Any]) -> None:
    merged = concat_notebooks([sample_notebook, sample_notebook])
    ids = [cell["id"] for cell in merged["cells"]]
    assert len(ids) == 8
    assert len(set(ids)) == 8


def test_concat_preserves_omitted_cell_ids(
    original_shipped_demo_notebook: dict[str, Any],
) -> None:
    merged = concat_notebooks([original_shipped_demo_notebook, original_shipped_demo_notebook])
    assert all("id" not in cell for cell in merged["cells"])
    codes = {issue.code for issue in lint_notebook(merged).issues}
    assert "NB009" in codes
    assert "NB010" not in codes


def test_concat_skips_non_mapping_cells(sample_notebook: dict[str, Any]) -> None:
    weird = {
        "cells": [
            "skip",
            {
                "cell_type": "markdown",
                "id": "shared",
                "metadata": {},
                "source": "# Shared\n",
            },
        ],
        "metadata": sample_notebook["metadata"],
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    merged = concat_notebooks([weird, weird])
    assert merged["cells"][0] == "skip"
    present_ids = [cell["id"] for cell in merged["cells"] if isinstance(cell, dict)]
    assert len(present_ids) == 2
    assert len(set(present_ids)) == 2
    assert all("id" not in cell for cell in merged["cells"] if not isinstance(cell, dict))


def test_transform_preserves_omitted_cell_ids() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "# Alpha\n"},
            {
                "cell_type": "code",
                "metadata": {},
                "source": "x = 1\n",
                "outputs": [],
                "execution_count": None,
            },
            {"cell_type": "markdown", "metadata": {}, "source": "# Beta\n"},
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    filtered = filter_cells(notebook, cell_types=["code"])
    assert all("id" not in cell for cell in filtered["cells"])
    sections = split_by_headings(notebook, level=1)
    assert all("id" not in cell for _, section in sections for cell in section["cells"])
    kerned = set_kernelspec(notebook, name="python3")
    assert all("id" not in cell for cell in kerned["cells"])
    tagged = add_tags(notebook, 1, ["keep"])
    assert all("id" not in cell for cell in tagged["cells"])


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


def test_split_by_headings_uses_setext_and_ignores_fences() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "```\n# ignored\n```\n"},
            {"cell_type": "markdown", "metadata": {}, "source": "Alpha\n=====\n"},
            {"cell_type": "code", "metadata": {}, "source": "a = 1\n", "outputs": []},
            {"cell_type": "markdown", "metadata": {}, "source": "## Not a split\n"},
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    sections = split_by_headings(notebook, level=1)
    titles = [title for title, _ in sections]
    assert titles == ["preamble", "Alpha"]
    assert len(sections[0][1]["cells"]) == 1
    assert len(sections[1][1]["cells"]) == 2


def test_set_kernelspec_and_tags(sample_notebook: dict[str, Any]) -> None:
    updated = set_kernelspec(sample_notebook, name="ir", display_name="R", language="r")
    assert updated["metadata"]["kernelspec"]["name"] == "ir"
    assert updated["metadata"]["language_info"]["name"] == "r"
    tagged = add_tags(updated, 0, ["intro"])
    assert "intro" in tagged["cells"][0]["metadata"]["tags"]
    with pytest.raises(IndexError):
        add_tags(sample_notebook, 99, ["x"])


def test_filter_predicate_and_kernelspec_without_metadata() -> None:
    notebook = {
        "cells": [
            {"cell_type": "code", "metadata": {}, "source": "a = 1\n", "outputs": []},
            {"cell_type": "markdown", "metadata": {}, "source": "# Keep\n"},
        ]
    }
    filtered = filter_cells(
        notebook,
        predicate=lambda cell: cell.get("cell_type") == "markdown",
    )
    assert len(filtered["cells"]) == 1
    updated = set_kernelspec({"cells": []}, name="python3", display_name="Py", language="python")
    assert updated["metadata"]["kernelspec"]["name"] == "python3"
    assert updated["metadata"]["language_info"]["name"] == "python"
    tagged = add_tags({"cells": [{"cell_type": "code", "source": "x", "metadata": None}]}, 0, ["t"])
    assert tagged["cells"][0]["metadata"]["tags"] == ["t"]
    untagged = remove_tags(tagged, 0, ["t", "missing"])
    assert untagged["cells"][0]["metadata"]["tags"] == []
    with pytest.raises(IndexError):
        remove_tags(tagged, 99, ["x"])


def test_filter_skips_non_mapping_cells() -> None:
    notebook = {
        "cells": [
            "skip",
            {"cell_type": "code", "metadata": {}, "source": "x = 1\n", "outputs": []},
        ]
    }
    filtered = filter_cells(notebook, cell_types=["code"])
    assert len(filtered["cells"]) == 1
    skipped = filter_cells(notebook, cell_types=["markdown"])
    assert skipped["cells"] == []


def test_ensure_cell_ids_fills_missing_and_duplicates() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "# A\n"},
            {"cell_type": "code", "id": "dup", "metadata": {}, "source": "x = 1\n", "outputs": []},
            {"cell_type": "code", "id": "dup", "metadata": {}, "source": "y = 2\n", "outputs": []},
            "skip",
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    updated = ensure_cell_ids(notebook)
    ids = [cell["id"] for cell in updated["cells"] if isinstance(cell, dict)]
    assert all(isinstance(cell_id, str) and cell_id for cell_id in ids)
    assert len(set(ids)) == 3


def test_ensure_cell_ids_retries_uuid_collision(monkeypatch: pytest.MonkeyPatch) -> None:
    generated = iter(["taken1234567", "fresh1234567"])

    class Token:
        def __init__(self) -> None:
            self.hex = next(generated)

    monkeypatch.setattr("nbops.transform.uuid.uuid4", Token)
    notebook = {
        "cells": [
            {"cell_type": "code", "id": "taken1234567", "metadata": {}, "source": "a\n"},
            {"cell_type": "code", "metadata": {}, "source": "b\n"},
        ]
    }
    updated = ensure_cell_ids(notebook)
    ids = [cell["id"] for cell in updated["cells"]]
    assert ids[0] == "taken1234567"
    assert ids[1] == "fresh1234567"
