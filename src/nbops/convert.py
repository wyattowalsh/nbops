"""Convert notebooks to percent-format Python, scripts, and Markdown."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from nbops.cells import cell_source, cells_of
from nbops.io import new_notebook
from nbops.models import ConvertResult
from nbops.transform import ensure_cell_ids

if TYPE_CHECKING:
    from collections.abc import Mapping


def to_percent_python(notebook: Mapping[str, Any]) -> str:
    """Render a notebook as a Jupytext-style percent script."""
    chunks: list[str] = []
    for cell in cells_of(notebook):
        if not isinstance(cell, dict):
            continue
        cell_type = cell.get("cell_type")
        source = cell_source(cell).rstrip()
        if cell_type == "markdown":
            quoted = "\n".join(f"# {line}" if line else "#" for line in source.splitlines()) or "#"
            chunks.append(f"# %% [markdown]\n{quoted}")
        elif cell_type == "raw":
            quoted = "\n".join(f"# {line}" if line else "#" for line in source.splitlines()) or "#"
            chunks.append(f"# %% [raw]\n{quoted}")
        else:
            chunks.append(f"# %%\n{source}")
    text = "\n\n".join(chunks).rstrip() + "\n"
    return text if chunks else ""


def to_script(notebook: Mapping[str, Any]) -> str:
    """Render only code cells as a plain Python script."""
    chunks: list[str] = []
    for cell in cells_of(notebook):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = cell_source(cell).rstrip()
        if source:
            chunks.append(source)
    return ("\n\n".join(chunks).rstrip() + "\n") if chunks else ""


def to_markdown(notebook: Mapping[str, Any]) -> str:
    """Render a notebook as Markdown with fenced Python code cells."""
    chunks: list[str] = []
    for cell in cells_of(notebook):
        if not isinstance(cell, dict):
            continue
        cell_type = cell.get("cell_type")
        source = cell_source(cell).rstrip()
        if cell_type == "markdown" or cell_type == "raw":
            if source:
                chunks.append(source)
        else:
            chunks.append(f"```python\n{source}\n```" if source else "```python\n```")
    return ("\n\n".join(chunks).rstrip() + "\n") if chunks else ""


def convert_notebook(notebook: Mapping[str, Any], fmt: str) -> ConvertResult:
    """Convert a notebook to ``py``, ``script``, or ``md``."""
    normalized = fmt.lower().strip()
    if normalized in {"py", "percent"}:
        return ConvertResult(format="py", text=to_percent_python(notebook))
    if normalized in {"script", "python"}:
        return ConvertResult(format="script", text=to_script(notebook))
    if normalized in {"md", "markdown"}:
        return ConvertResult(format="md", text=to_markdown(notebook))
    raise ValueError(f"Unsupported conversion format: {fmt}")


_PERCENT_HEADER = re.compile(r"^# %%(?:\s*\[(?P<kind>[\w-]+)\])?(?:\s+.*)?$")
_JUPYTEXT_FENCE = "# ---"


def from_percent_python(text: str) -> dict[str, Any]:
    """Parse a Jupytext-style percent script into an nbformat v4 notebook."""
    notebook = new_notebook()
    cells: list[dict[str, Any]] = []
    current_kind = "code"
    current_lines: list[str] = []
    started = False

    def flush() -> None:
        nonlocal current_lines
        if not started and not any(line.strip() for line in current_lines):
            current_lines = []
            return
        source = "\n".join(current_lines).strip("\n")
        if current_kind in {"markdown", "raw"}:
            source = _unquote_percent_comment(source)
            cells.append(
                {
                    "cell_type": current_kind,
                    "metadata": {},
                    "source": f"{source}\n" if source else "",
                }
            )
        else:
            cells.append(
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": f"{source}\n" if source else "",
                }
            )
        current_lines = []

    for line in _strip_jupytext_front_matter(text).splitlines():
        match = _PERCENT_HEADER.match(line)
        if match is not None:
            if started or current_lines:
                flush()
            started = True
            kind = (match.group("kind") or "code").lower()
            current_kind = kind if kind in {"markdown", "raw"} else "code"
            continue
        current_lines.append(line)
    if started or any(line.strip() for line in current_lines):
        flush()
    notebook["cells"] = cells
    return ensure_cell_ids(notebook)


def _strip_jupytext_front_matter(text: str) -> str:
    """Drop a leading ``# ---`` YAML header used by Jupytext percent scripts."""
    lines = text.splitlines()
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines) or lines[index].strip() != _JUPYTEXT_FENCE:
        return text
    closer = index + 1
    while closer < len(lines) and lines[closer].strip() != _JUPYTEXT_FENCE:
        closer += 1
    if closer >= len(lines):
        return text
    body = "\n".join(lines[closer + 1 :])
    if text.endswith("\n") and body:
        return f"{body}\n"
    return body


def _unquote_percent_comment(source: str) -> str:
    lines: list[str] = []
    for line in source.splitlines():
        if line.startswith("# "):
            lines.append(line[2:])
        elif line == "#":
            lines.append("")
        else:
            lines.append(line)
    return "\n".join(lines)
