"""Shared pytest fixtures for the nbops test suite."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def sample_notebook() -> dict[str, Any]:
    """A minimal, valid nbformat v4 notebook with mixed cell types."""
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
def sample_notebook_file(tmp_path: Path, sample_notebook: dict[str, Any]) -> Path:
    """Write ``sample_notebook`` to a temporary ``.ipynb`` file and return its path."""
    path = tmp_path / "sample.ipynb"
    path.write_text(json.dumps(sample_notebook), encoding="utf-8")
    return path
