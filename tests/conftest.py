"""Shared pytest fixtures for the nbops test suite."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def sample_notebook() -> dict[str, Any]:
    """A minimal, valid-enough nbformat v4 notebook with mixed cell types."""
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "md-title",
                "metadata": {},
                "source": ["# Title\n", "Intro text"],
            },
            {
                "cell_type": "code",
                "id": "code-os",
                "execution_count": 1,
                "metadata": {"tags": ["setup"]},
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": ["ok\n"],
                    }
                ],
                "source": ["import os\n", "\n", "print(os.getcwd())\n"],
            },
            {
                "cell_type": "code",
                "id": "code-vars",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "x = 1\ny = 2\n",
            },
            {
                "cell_type": "raw",
                "id": "raw-1",
                "metadata": {},
                "source": ["raw content"],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


@pytest.fixture
def sample_notebook_file(tmp_path: Path, sample_notebook: dict[str, Any]) -> Path:
    """Write ``sample_notebook`` to a temporary ``.ipynb`` file and return its path."""
    path = tmp_path / "sample.ipynb"
    path.write_text(json.dumps(sample_notebook), encoding="utf-8")
    return path


@pytest.fixture
def original_scaffold_notebook() -> dict[str, Any]:
    """Exact stats-scaffold fixture from ``cursor/setup-dev-environment-a5a8``.

    Incomplete kernelspec (no ``name``), no cell ids, mixed source shapes.
    """
    return {
        "cells": [
            {"cell_type": "markdown", "source": ["# Title\n", "Intro text"]},
            {"cell_type": "code", "source": ["import os\n", "\n", "print(os.getcwd())\n"]},
            {"cell_type": "code", "source": "x = 1\ny = 2\n"},
            {"cell_type": "raw", "source": ["raw content"]},
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


@pytest.fixture
def original_scaffold_notebook_file(
    tmp_path: Path, original_scaffold_notebook: dict[str, Any]
) -> Path:
    """Write the original stats-scaffold fixture to a temporary ``.ipynb`` file."""
    path = tmp_path / "original-scaffold.ipynb"
    path.write_text(json.dumps(original_scaffold_notebook), encoding="utf-8")
    return path


@pytest.fixture
def error_notebook() -> dict[str, Any]:
    return {
        "cells": [
            {
                "cell_type": "code",
                "id": "err-raise",
                "execution_count": 1,
                "metadata": {},
                "outputs": [
                    {
                        "ename": "ValueError",
                        "evalue": "boom",
                        "output_type": "error",
                        "traceback": ["ValueError: boom"],
                    }
                ],
                "source": "raise ValueError('boom')\n",
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
