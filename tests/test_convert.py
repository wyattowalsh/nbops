"""Unit tests for notebook conversion."""

from __future__ import annotations

from typing import Any

import pytest

from nbops.convert import convert_notebook, to_markdown, to_percent_python, to_script


def test_percent_and_script_and_markdown(sample_notebook: dict[str, Any]) -> None:
    percent = to_percent_python(sample_notebook)
    assert "# %% [markdown]" in percent
    assert "# %%" in percent
    assert "import os" in percent
    script = to_script(sample_notebook)
    assert "import os" in script
    assert "# Title" not in script
    markdown = to_markdown(sample_notebook)
    assert "# Title" in markdown
    assert "```python" in markdown


def test_convert_notebook_formats(sample_notebook: dict[str, Any]) -> None:
    assert convert_notebook(sample_notebook, "py").format == "py"
    assert convert_notebook(sample_notebook, "script").format == "script"
    assert convert_notebook(sample_notebook, "md").format == "md"
    with pytest.raises(ValueError, match="Unsupported"):
        convert_notebook(sample_notebook, "pdf")
