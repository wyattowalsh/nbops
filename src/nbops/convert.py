"""Convert notebooks to percent-format Python, scripts, and Markdown."""

from __future__ import annotations

import ast
import json
import re
from typing import TYPE_CHECKING, Any

from nbops.cells import (
    as_mapping,
    cell_source,
    cell_tags,
    cells_of,
    is_python_notebook,
    notebook_code_language,
    strip_ipython_magics,
)
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
    body = ("\n\n".join(chunks).rstrip() + "\n") if chunks else ""
    front_matter = _jupytext_kernelspec_front_matter(notebook)
    if not front_matter:
        return body
    if not body:
        return front_matter
    return f"{front_matter}{body}"


def to_script(notebook: Mapping[str, Any]) -> str:
    """Render code cells as a plain Python script.

    IPython line magics, shell bangs, and help suffixes are stripped so the
    result is parseable Python. Non-Python cell magics such as ``%%bash`` are
    omitted. Non-Python notebooks are emitted unchanged.
    """
    python = is_python_notebook(notebook)
    chunks: list[str] = []
    for cell in cells_of(notebook):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = cell_source(cell)
        if python:
            cleaned = strip_ipython_magics(source)
            if cleaned is None:
                continue
            source = cleaned
        source = source.rstrip()
        if source:
            chunks.append(source)
    return ("\n\n".join(chunks).rstrip() + "\n") if chunks else ""


def to_markdown(notebook: Mapping[str, Any]) -> str:
    """Render a notebook as Markdown with fenced code cells."""
    language = notebook_code_language(notebook)
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
            chunks.append(f"```{language}\n{source}\n```" if source else f"```{language}\n```")
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


_PERCENT_KIND = re.compile(r"\[(?P<kind>[\w-]+)\]")
_META_KEY = re.compile(r"[A-Za-z0-9_\.@/-]+")
_VALID_META_KEY = re.compile(r"^[A-Za-z0-9_\.@/-]+$")
_UNQUOTED_VALUE = re.compile(r"[A-Za-z0-9_.+-]+")
_UNQUOTED_ID = re.compile(r"[A-Za-z0-9_-]+")
_JSONISH_ERROR = object()
_JUPYTEXT_FENCE = "# ---"


def from_percent_python(text: str) -> dict[str, Any]:
    """Parse a Jupytext-style percent script into an nbformat v4 notebook.

    Cell ids present in ``# %%`` headers are restored. Omitted ids stay omitted;
    use :func:`nbops.transform.ensure_cell_ids` / ``nbops ids`` to assign them.
    Jupytext optional titles, ``key=value`` cell metadata, and JSON metadata
    objects are restored onto the cell.
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
        parsed = _parse_percent_header(line)
        if parsed is not None:
            if started or current_lines:
                flush()
            started = True
            title, kind, meta = parsed
            current_kind = _percent_kind(kind)
            current_meta = _percent_cell_metadata(meta)
            current_id = _percent_cell_id(meta)
            current_title = _percent_title_text(title)
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
    metadata = cell.get("metadata")
    if isinstance(metadata, dict):
        skipped = {"id", "tags"}
        if title is not None:
            skipped.add("title")
        for key in sorted(metadata):
            if key in skipped:
                continue
            encoded = _percent_meta_item(key, metadata[key])
            if encoded is not None:
                parts.append(encoded)
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


def _percent_meta_item(key: str, value: Any) -> str | None:
    if not _VALID_META_KEY.match(key):
        return None
    try:
        return f"{key}={json.dumps(value)}"
    except (TypeError, ValueError):
        return None


def _parse_percent_header(line: str) -> tuple[str | None, str | None, str | None] | None:
    """Split a ``# %%`` line into optional title, cell kind, and metadata text."""
    if not line.startswith("# %%"):
        return None
    rest = line[4:]
    if rest and rest[0] not in " \t" and not rest.startswith("["):
        return None
    text = rest.rstrip()
    index = 0
    length = len(text)
    while index < length and text[index] in " \t":
        index += 1
    if index >= length:
        return None, None, None

    title: str | None = None
    kind, kind_end = _try_percent_kind(text, index)
    if kind is not None:
        index = kind_end
    elif _at_percent_metadata(text, index):
        title = None
    else:
        title_start = index
        title_end = length
        found_tail = False
        scan = index
        while scan < length:
            kind_token, kind_end = _try_percent_kind(text, scan)
            if kind_token is not None:
                title_end = scan
                kind = kind_token
                index = kind_end
                found_tail = True
                break
            if text[scan] in " \t":
                skip = scan
                while skip < length and text[skip] in " \t":
                    skip += 1
                if _at_percent_metadata(text, skip):
                    title_end = scan
                    index = skip
                    found_tail = True
                    break
                scan = skip
                continue
            scan += 1
        if not found_tail:
            stripped_title = text[title_start:].strip() or None
            if stripped_title and _percent_title_text(stripped_title) is None:
                return None
            return stripped_title, None, None
        title = text[title_start:title_end].strip() or None

    while index < length and text[index] in " \t":
        index += 1
    meta = text[index:] if index < length else None
    if not meta:
        return title, kind, None
    if meta.startswith("{") or _at_percent_metadata(meta, 0):
        return title, kind, meta
    return None


def _try_percent_kind(text: str, index: int) -> tuple[str | None, int]:
    match = _PERCENT_KIND.match(text, index)
    if match is None:
        return None, index
    return match.group("kind"), match.end()


def _at_percent_metadata(text: str, index: int) -> bool:
    if index >= len(text):
        return False
    if text[index] == "{":
        return True
    match = _META_KEY.match(text, index)
    if match is None:
        return False
    position = match.end()
    while position < len(text) and text[position] in " \t":
        position += 1
    return position < len(text) and text[position] == "="


def _percent_header_pairs(meta: str | None) -> dict[str, Any]:
    if not meta or not meta.strip():
        return {}
    stripped = meta.strip()
    if stripped.startswith("{"):
        raw = _leading_object_literal(stripped)
        if raw is None:
            return {}
        decoded = _decode_jsonish(raw)
        return dict(decoded) if isinstance(decoded, dict) else {}
    return _parse_key_equal_values(stripped)


def _percent_cell_metadata(meta: str | None) -> dict[str, Any]:
    pairs = dict(_percent_header_pairs(meta))
    pairs.pop("id", None)
    if "tags" in pairs:
        tags = pairs["tags"]
        if not isinstance(tags, list):
            del pairs["tags"]
        else:
            pairs["tags"] = [str(tag) for tag in tags]
    return pairs


def _percent_cell_id(meta: str | None) -> str | None:
    value = _percent_header_pairs(meta).get("id")
    if isinstance(value, str) and value:
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return None


def _parse_key_equal_values(text: str) -> dict[str, Any]:
    index = 0
    length = len(text)
    pairs: dict[str, Any] = {}
    while index < length:
        while index < length and text[index] in " \t":
            index += 1
        if index >= length:
            break
        key_match = _META_KEY.match(text, index)
        if key_match is None:
            break
        position = key_match.end()
        while position < length and text[position] in " \t":
            position += 1
        if position >= length or text[position] != "=":
            break
        index = position + 1
        while index < length and text[index] in " \t":
            index += 1
        consumed = _consume_meta_value(text, index)
        if consumed is None:
            break
        pairs[key_match.group(0)] = consumed[0]
        index = consumed[1]
    return pairs


def _consume_meta_value(text: str, index: int) -> tuple[Any, int] | None:
    if index >= len(text):
        return None
    char = text[index]
    if char == "{":
        raw = _leading_object_literal(text[index:])
        if raw is None:
            return None
        decoded = _decode_jsonish(raw)
        if decoded is _JSONISH_ERROR:
            return None
        return decoded, index + len(raw)
    if char == "[":
        raw = _leading_list_literal(text[index:])
        if raw is None:
            return None
        decoded = _decode_jsonish(raw)
        if decoded is _JSONISH_ERROR:
            return None
        return decoded, index + len(raw)
    if char in {'"', "'"}:
        quoted = _consume_quoted_string(text, index)
        if quoted is None:
            return None
        return quoted
    match = _UNQUOTED_VALUE.match(text, index)
    if match is None:
        return None
    token = match.group(0)
    decoded = _decode_jsonish(token)
    if decoded is _JSONISH_ERROR:
        return token, match.end()
    return decoded, match.end()


def _decode_jsonish(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            return _JSONISH_ERROR


def _consume_quoted_string(text: str, index: int) -> tuple[str, int] | None:
    if index >= len(text) or text[index] not in {'"', "'"}:
        return None
    quote = text[index]
    escape = False
    for offset, char in enumerate(text[index + 1 :], start=index + 1):
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if char == quote:
            raw = text[index : offset + 1]
            try:
                value = json.loads(raw) if quote == '"' else ast.literal_eval(raw)
            except (json.JSONDecodeError, SyntaxError, ValueError):
                return None
            if not isinstance(value, str):
                return None
            return value, offset + 1
    return None


def _leading_scalar_literal(text: str) -> str | None:
    stripped = text.lstrip()
    if not stripped:
        return None
    if stripped[0] in {'"', "'"}:
        quoted = _consume_quoted_string(stripped, 0)
        return quoted[0] if quoted is not None else None
    match = _UNQUOTED_ID.match(stripped)
    return match.group(0) if match else None


def _leading_bracket_literal(text: str, opener: str, closer: str) -> str | None:
    stripped = text.lstrip()
    if not stripped.startswith(opener):
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
        if char == opener:
            depth += 1
            continue
        if char == closer:
            depth -= 1
            if depth == 0:
                return stripped[: index + 1]
    return None


def _leading_list_literal(text: str) -> str | None:
    return _leading_bracket_literal(text, "[", "]")


def _leading_object_literal(text: str) -> str | None:
    return _leading_bracket_literal(text, "{", "}")


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


_YAML_BARE_SCALAR = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")


def _yaml_emit_scalar(value: str) -> str:
    if _YAML_BARE_SCALAR.match(value):
        return value
    return json.dumps(value)


def _jupytext_kernelspec_front_matter(notebook: Mapping[str, Any]) -> str:
    """Emit a Jupytext ``# ---`` header for a kernelspec that has a name."""
    kernelspec = as_mapping(as_mapping(notebook.get("metadata")).get("kernelspec"))
    name = kernelspec.get("name")
    if not isinstance(name, str) or not name:
        return ""
    lines = ["# ---", "# kernelspec:"]
    for key in ("name", "display_name", "language"):
        value = kernelspec.get(key)
        if isinstance(value, str) and value:
            lines.append(f"#   {key}: {_yaml_emit_scalar(value)}")
    lines.append("# ---")
    return "\n".join(lines) + "\n"


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
