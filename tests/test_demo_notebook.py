"""Contract tests for the shipped demo notebook (examples/demo.ipynb)."""

from __future__ import annotations

from pathlib import Path

from nbops.cells import cell_source, cell_tags
from nbops.convert import from_percent_python, to_percent_python
from nbops.inspect import compute_stats, extract_imports, outline
from nbops.io import load_notebook, validate_notebook
from nbops.lint import lint_notebook

DEMO = Path(__file__).resolve().parents[1] / "examples" / "demo.ipynb"


def test_demo_notebook_exists() -> None:
    assert DEMO.is_file()


def test_demo_notebook_schema_layout_and_ids() -> None:
    notebook = load_notebook(DEMO, validate=True)
    validate_notebook(notebook)
    cells = notebook["cells"]
    assert [cell["cell_type"] for cell in cells] == ["markdown", "code", "code", "markdown"]
    assert [cell["id"] for cell in cells] == ["title", "area", "print-area", "done"]
    assert len({cell["id"] for cell in cells}) == 4
    assert cell_tags(cells[1]) == ["demo"]
    kernelspec = notebook["metadata"]["kernelspec"]
    assert kernelspec["name"] == "python3"
    assert kernelspec["display_name"] == "Python 3"
    assert notebook["metadata"]["language_info"]["name"] == "python"
    assert notebook["nbformat"] == 4
    assert notebook["nbformat_minor"] == 5


def test_demo_notebook_sources_and_imports() -> None:
    notebook = load_notebook(DEMO, validate=False)
    cells = notebook["cells"]
    assert cell_source(cells[0]).startswith("# nbops demo notebook")
    assert "import math" in cell_source(cells[1])
    assert "def area(" in cell_source(cells[1])
    assert "print(area(2.0))" in cell_source(cells[2])
    headings = outline(notebook)
    assert headings[0].level == 1
    assert headings[0].title == "nbops demo notebook"
    modules = {item.module for item in extract_imports(notebook)}
    assert "math" in modules


def test_demo_notebook_stats_lint_and_percent_roundtrip() -> None:
    notebook = load_notebook(DEMO, validate=False)
    stats = compute_stats(notebook)
    assert stats.total_cells == 4
    assert stats.code_cells == 2
    assert stats.code_lines == 4
    assert stats.kernel == "Python 3"
    assert stats.language == "python"
    assert stats.tags == ["demo"]
    report = lint_notebook(notebook)
    assert report.error_count == 0
    restored = from_percent_python(to_percent_python(notebook))
    assert [cell["cell_type"] for cell in restored["cells"]] == [
        "markdown",
        "code",
        "code",
        "markdown",
    ]
    assert restored["cells"][1]["metadata"]["tags"] == ["demo"]
