"""Unit tests for notebook diffs."""

from __future__ import annotations

from typing import Any

from nbops.diff import diff_notebooks


def test_identical_notebooks(sample_notebook: dict[str, Any]) -> None:
    report = diff_notebooks(sample_notebook, sample_notebook)
    assert report.identical is True
    assert report.changed == 0
    assert report.equal == 4


def test_changed_added_removed(sample_notebook: dict[str, Any]) -> None:
    right = {
        "cells": [
            sample_notebook["cells"][0],
            {
                "cell_type": "code",
                "metadata": {},
                "source": "x = 99\n",
                "outputs": [],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "# Extra\n",
            },
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    report = diff_notebooks(sample_notebook, right)
    assert report.identical is False
    assert report.changed + report.added + report.removed > 0
    assert report.right_cells == 3


def test_diff_replace_with_unequal_span() -> None:
    left = {"cells": [{"cell_type": "code", "metadata": {}, "source": "a = 1\n"}]}
    right = {
        "cells": [
            {"cell_type": "code", "metadata": {}, "source": "b = 2\n"},
            {"cell_type": "markdown", "metadata": {}, "source": "# Extra\n"},
        ]
    }
    report = diff_notebooks(left, right)
    assert report.identical is False
    assert report.left_cells == 1
    assert report.right_cells == 2
    assert report.changed + report.added >= 1
    assert any(cell.change in {"changed", "added"} for cell in report.cells)
