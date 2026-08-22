"""Optional notebook execution via nbclient."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

from nbformat.validator import MissingIDFieldWarning
from tenacity import retry, stop_after_attempt, wait_exponential

from nbops.cells import as_mapping, nested_mapping
from nbops.exceptions import ExecuteError, MissingExtraError
from nbops.io import dumps_notebook, parse_notebook

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path


def execute_notebook(
    notebook: Mapping[str, Any],
    *,
    timeout: int = 120,
    kernel_name: str | None = None,
    cwd: str | Path | None = None,
    allow_errors: bool = False,
) -> dict[str, Any]:
    """Execute a notebook in-process with nbclient and return the updated document.

    Requires the ``nbops[execute]`` extra. ``nbformat`` may insert cell ids while
    talking to the kernel; omitted ids are restored on the returned document so
    lint ``NB009`` and ``clean --strip-ids`` stay observable.
    """
    original_ids = _original_cell_ids(notebook)
    client_cls = _notebook_client_class()
    resources: dict[str, Any] = {}
    if cwd is not None:
        resources["metadata"] = {"path": str(cwd)}
    metadata = as_mapping(notebook.get("metadata"))
    kernelspec = nested_mapping(metadata, "kernelspec")
    kernel = kernel_name or kernelspec.get("name") or "python3"

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=0.2, min=0.2, max=2),
        reraise=True,
    )
    def _run() -> dict[str, Any]:
        try:
            import nbformat
        except ImportError as exc:  # pragma: no cover - nbformat is a hard dependency
            raise MissingExtraError("nbformat is required to execute notebooks.") from exc
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", MissingIDFieldWarning)
            node = nbformat.reads(dumps_notebook(dict(notebook)), as_version=4)
        client = client_cls(
            node,
            timeout=timeout,
            kernel_name=kernel,
            resources=resources or None,
            allow_errors=allow_errors,
        )
        try:
            executed = client.execute()
        except Exception as exc:
            raise ExecuteError(f"Notebook execution failed: {exc}") from exc
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", MissingIDFieldWarning)
            result = parse_notebook(nbformat.writes(executed), validate=False)
        return _apply_original_cell_ids(result, original_ids)

    return _run()


def _original_cell_ids(notebook: Mapping[str, Any]) -> list[str | None]:
    """Return each cell's id, or ``None`` when the id was omitted or empty."""
    cells = as_mapping(notebook).get("cells")
    if not isinstance(cells, list):
        return []
    ids: list[str | None] = []
    for cell in cells:
        if isinstance(cell, dict) and isinstance(cell.get("id"), str) and cell["id"]:
            ids.append(cell["id"])
        else:
            ids.append(None)
    return ids


def _apply_original_cell_ids(
    notebook: dict[str, Any], original_ids: list[str | None]
) -> dict[str, Any]:
    """Restore omitted vs present cell ids after an nbformat execute roundtrip."""
    cells = notebook.get("cells")
    if not isinstance(cells, list):
        return notebook
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict) or index >= len(original_ids):
            continue
        original_id = original_ids[index]
        if original_id is None:
            cell.pop("id", None)
        else:
            cell["id"] = original_id
    return notebook


def _notebook_client_class() -> Any:
    try:
        from nbclient import NotebookClient
    except ImportError as exc:
        raise MissingExtraError(
            "Notebook execution requires the optional extra 'nbops[execute]' (nbclient)."
        ) from exc
    return NotebookClient
