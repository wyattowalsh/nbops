"""Tests for the operations catalog and lint issue codes."""

from __future__ import annotations

from nbops.lint import ISSUE_CATALOG, lint_notebook
from nbops.operations import OPERATIONS, operation_names


def test_issue_catalog_covers_nb000_through_nb011() -> None:
    assert list(ISSUE_CATALOG) == [f"NB{index:03d}" for index in range(12)]


def test_lint_emits_missing_cell_id() -> None:
    report = lint_notebook(
        {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": "# Title\n",
                }
            ],
            "metadata": {"kernelspec": {"name": "python3"}},
            "nbformat": 4,
            "nbformat_minor": 5,
        }
    )
    assert any(issue.code == "NB009" for issue in report.issues)


def test_operation_catalog_names_are_unique() -> None:
    names = operation_names()
    assert len(names) == len(set(names))
    assert "stats" in names
    assert "ops" in names
    assert all(item.library for item in OPERATIONS)
