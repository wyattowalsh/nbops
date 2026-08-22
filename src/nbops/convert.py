"""Convert notebooks to percent-format Python, scripts, and Markdown."""

from __future__ import annotations

import ast
import json
import re
from typing import TYPE_CHECKING, Any

from nbops.cells import cell_source, cell_tags, cells_of
from nbops.io import new_notebook
from nbops.models import ConvertResult
from nbops.transform import set_kernelspec

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
        header = _percent_cell_header(cell)
        if cell_type == "markdown" or cell_type == "raw":
            quoted = "\n".join(f"# {line}" if line else "#" for line in source.splitlines()) or "#"
            chunks.append(f"{header}\n{quoted}")
        else:
            chunks.append(f"{header}\n{source}")
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


_PERCENT_HEADER = re.compile(
    r"^# %%(?:\s+(?P<title>(?:(?!\s*\[)(?!\s*\w+=).)+))?"
    r"(?:\s*\[(?P<kind>[\w-]+)\])?(?P<meta>\s+\w+=.*)?\s*$"
)
_PERCENT_TAGS = re.compile(r"\btags\s*=\s*")
_PERCENT_ID = re.compile(r"\bid\s*=\s*")
_UNQUOTED_ID = re.compile(r"[A-Za-z0-9_-]+")
_JUPYTEXT_FENCE = "# ---"


def from_percent_python(text: str) -> dict[str, Any]:
    """Parse a Jupytext-style percent script into an nbformat v4 notebook.

    Cell ids present in ``# %%`` headers are restored. Omitted ids stay omitted;
    use :func:`nbops.transform.ensure_cell_ids` / ``nbops ids`` to assign them.
    """
    notebook = new_notebook()
    kernelspec = _kernelspec_from_jupytext_front_matter(text)
    if kernelspec is not None:
        notebook = set_kernelspec(
            notebook,
            name=kernelspec["name"],
            display_name=kernelspec.get("display_name"),
            language=kernelspec.get("language"),
        )
    cells: list[dict[str, Any]] = []
    current_kind = "code"
    current_meta: dict[str, Any] = {}
    current_id: str | None = None
    current_title: str | None = None
    current_lines: list[str] = []
    started = False

    def flush() -> None:
        nonlocal current_lines
        if not started and not any(line.strip() for line in current_lines):
            current_lines = []
            return
        source = "\n".join(current_lines).strip("\n")
        metadata = dict(current_meta)
        if current_title:
            metadata["title"] = current_title
        if current_kind in {"markdown", "raw"}:
            source = _unquote_percent_comment(source)
            cell: dict[str, Any] = {
                "cell_type": current_kind,
                "metadata": metadata,
                "source": f"{source}\n" if source else "",
            }
        else:
            cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": metadata,
                "outputs": [],
                "source": f"{source}\n" if source else "",
            }
        if current_id:
            cell["id"] = current_id
        cells.append(cell)
        current_lines = []

    for line in _strip_jupytext_front_matter(text).splitlines():
        match = _PERCENT_HEADER.match(line)
        if match is not None:
            if started or current_lines:
                flush()
            started = True
            current_kind = _percent_kind(match.group("kind"))
            current_meta = _percent_cell_metadata(match.group("meta"))
            current_id = _percent_cell_id(match.group("meta"))
            current_title = _percent_title_text(match.group("title"))
            continue
        current_lines.append(line)
    if started or any(line.strip() for line in current_lines):
        flush()
    notebook["cells"] = cells
    return notebook


def _percent_cell_header(cell: Mapping[str, Any]) -> str:
    cell_type = cell.get("cell_type")
    kind = "" if cell_type == "code" else f" [{cell_type}]"
    title = _percent_title_text(_mapping_title(cell))
    title_part = f" {title}" if title else ""
    parts: list[str] = []
    cell_id = cell.get("id")
    if isinstance(cell_id, str) and cell_id:
        parts.append(f"id={json.dumps(cell_id)}")
    tags = cell_tags(cell)
    if tags:
        parts.append(f"tags={json.dumps(tags)}")
    suffix = f" {' '.join(parts)}" if parts else ""
    return f"# %%{title_part}{kind}{suffix}"


def _mapping_title(cell: Mapping[str, Any]) -> str | None:
    metadata = cell.get("metadata")
    if not isinstance(metadata, dict):
        return None
    raw_title = metadata.get("title")
    return raw_title if isinstance(raw_title, str) else None


def _percent_title_text(raw: str | None) -> str | None:
    if not raw or not raw.strip():
        return None
    title = raw.strip()
    if "[" in title or "=" in title:
        return None
    return title


def _percent_kind(kind: str | None) -> str:
    token = (kind or "code").lower()
    if token in {"markdown", "md"}:
        return "markdown"
    if token == "raw":
        return "raw"
    return "code"


def _percent_cell_metadata(meta: str | None) -> dict[str, Any]:
    if not meta or not meta.strip():
        return {}
    match = _PERCENT_TAGS.search(meta)
    if match is None:
        return {}
    raw = _leading_list_literal(meta[match.end() :])
    if raw is None:
        return {}
    try:
        tags = json.loads(raw)
    except json.JSONDecodeError:
        try:
            tags = ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            return {}
    if not isinstance(tags, list):
        return {}
    return {"tags": [str(tag) for tag in tags]}


def _percent_cell_id(meta: str | None) -> str | None:
    if not meta or not meta.strip():
        return None
    match = _PERCENT_ID.search(meta)
    if match is None:
        return None
    value = _leading_scalar_literal(meta[match.end() :])
    if not isinstance(value, str) or not value:
        return None
    return value


def _leading_scalar_literal(text: str) -> str | None:
    stripped = text.lstrip()
    if not stripped:
        return None
    if stripped[0] in {'"', "'"}:
        quote = stripped[0]
        escape = False
        for index, char in enumerate(stripped[1:], start=1):
            if escape:
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            if char == quote:
                raw = stripped[: index + 1]
                try:
                    value = json.loads(raw) if quote == '"' else ast.literal_eval(raw)
                except (json.JSONDecodeError, SyntaxError, ValueError):
                    return None
                return value if isinstance(value, str) else None
        return None
    match = _UNQUOTED_ID.match(stripped)
    return match.group(0) if match else None


def _leading_list_literal(text: str) -> str | None:
    stripped = text.lstrip()
    if not stripped.startswith("["):
        return None
    quote: str | None = None
    escape = False
    depth = 0
    for index, char in enumerate(stripped):
        if quote is not None:
            if escape:
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            if char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
            continue
        if char == "[":
            depth += 1
            continue
        if char == "]":
            depth -= 1
            if depth == 0:
                return stripped[: index + 1]
    return None


def _jupytext_front_matter_span(lines: list[str]) -> tuple[int, int] | None:
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines) or lines[index].strip() != _JUPYTEXT_FENCE:
        return None
    closer = index + 1
    while closer < len(lines) and lines[closer].strip() != _JUPYTEXT_FENCE:
        closer += 1
    if closer >= len(lines):
        return None
    return index, closer


def _strip_jupytext_front_matter(text: str) -> str:
    """Drop a leading ``# ---`` YAML header used by Jupytext percent scripts."""
    lines = text.splitlines()
    span = _jupytext_front_matter_span(lines)
    if span is None:
        return text
    _start, closer = span
    body = "\n".join(lines[closer + 1 :])
    if text.endswith("\n") and body:
        return f"{body}\n"
    return body


def _uncomment_jupytext_yaml_line(line: str) -> str:
    if line.startswith("# "):
        return line[2:]
    if line.startswith("#"):
        return line[1:]
    return line


def _yaml_scalar(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {'"', "'"}:
        return stripped[1:-1]
    return stripped


def _kernelspec_from_jupytext_front_matter(text: str) -> dict[str, str] | None:
    """Read ``kernelspec`` name/display_name/language from a Jupytext YAML header."""
    lines = text.splitlines()
    span = _jupytext_front_matter_span(lines)
    if span is None:
        return None
    start, closer = span
    kernel_indent: int | None = None
    fields: dict[str, str] = {}
    for raw in lines[start + 1 : closer]:
        yaml_line = _uncomment_jupytext_yaml_line(raw)
        if not yaml_line.strip():
            continue
        indent = len(yaml_line) - len(yaml_line.lstrip(" "))
        stripped = yaml_line.strip()
        if kernel_indent is None:
            if stripped.startswith("kernelspec:"):
                kernel_indent = indent
                inline = stripped.partition(":")[2].strip()
                if inline:
                    return None
            continue
        if indent <= kernel_indent:
            break
        key, sep, raw_value = stripped.partition(":")
        if not sep:
            continue
        value = _yaml_scalar(raw_value)
        if key in {"name", "display_name", "language"} and value:
            fields[key] = value
    if "name" not in fields:
        return None
    return fields


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
