"""Unit tests for notebook diffs."""

from __future__ import annotations

from typing import Any

import pytest

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


def test_diff_skips_unknown_opcode(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeMatcher:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def get_opcodes(self) -> list[tuple[str, int, int, int, int]]:
            return [("equal", 0, 0, 0, 0), ("noop", 0, 0, 0, 0)]

    monkeypatch.setattr("nbops.diff.SequenceMatcher", FakeMatcher)
    report = diff_notebooks({"cells": []}, {"cells": []})
    assert report.cells == []
    assert report.identical is True


def test_diff_insert_then_equal_continues_opcode_loop() -> None:
    left = {"cells": [{"cell_type": "markdown", "metadata": {}, "source": "# End\n"}]}
    right = {
        "cells": [
            {"cell_type": "code", "metadata": {}, "source": "x = 1\n"},
            {"cell_type": "markdown", "metadata": {}, "source": "# End\n"},
        ]
    }
    inserted = diff_notebooks(left, right)
    assert inserted.added == 1
    assert inserted.equal == 1
    deleted = diff_notebooks(right, left)
    assert deleted.removed == 1
    assert deleted.equal == 1


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


def test_diff_detects_attachment_only_changes() -> None:
    left = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "See plot\n",
                "attachments": {"plot.png": {"image/png": "aaa"}},
            }
        ]
    }
    same = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "See plot\n",
                "attachments": {"plot.png": {"image/png": "aaa"}},
            }
        ]
    }
    nested = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {"attachments": {"plot.png": {"image/png": "aaa"}}},
                "source": "See plot\n",
            }
        ]
    }
    right = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "See plot\n",
                "attachments": {"plot.png": {"image/png": "bbb"}},
            }
        ]
    }
    empty = {"cells": [{"cell_type": "markdown", "metadata": {}, "source": "See plot\n"}]}
    assert diff_notebooks(left, same).identical is True
    assert diff_notebooks(left, nested).identical is True
    changed = diff_notebooks(left, right)
    assert changed.identical is False
    assert changed.changed == 1
    assert diff_notebooks(left, empty).changed == 1

    cycle: dict[str, Any] = {}
    cycle["self"] = cycle
    cycled = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "See plot\n",
                "attachments": cycle,
            }
        ]
    }
    assert diff_notebooks(cycled, empty).identical is False
