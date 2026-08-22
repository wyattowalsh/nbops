"""Unit tests for cleaning notebooks."""

from __future__ import annotations

from typing import Any

from nbops.clean import clean_notebook
from nbops.models import CleanOptions


def test_clean_strips_outputs_and_counts(sample_notebook: dict[str, Any]) -> None:
    original_outputs = sample_notebook["cells"][1]["outputs"]
    cleaned = clean_notebook(sample_notebook)
    assert sample_notebook["cells"][1]["outputs"] == original_outputs
    code = cleaned["cells"][1]
    assert code["outputs"] == []
    assert code["execution_count"] is None
    assert cleaned["cells"][2]["execution_count"] is None


def test_clean_drop_empty_and_ids(sample_notebook: dict[str, Any]) -> None:
    sample_notebook["cells"].append(
        {"cell_type": "code", "id": "empty", "metadata": {}, "source": "", "outputs": []}
    )
    cleaned = clean_notebook(
        sample_notebook,
        CleanOptions(empty_cells=True, cell_ids=True, outputs=True, execution_counts=True),
    )
    assert all("id" not in cell for cell in cleaned["cells"] if isinstance(cell, dict))
    assert all(
        not (isinstance(cell, dict) and cell.get("source") == "") for cell in cleaned["cells"]
    )
    assert len(cleaned["cells"]) == 4
