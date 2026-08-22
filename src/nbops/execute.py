"""Optional notebook execution via nbclient."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential

from nbops.cells import as_mapping, nested_mapping
from nbops.exceptions import ExecuteError, MissingExtraError
from nbops.io import dumps_notebook, parse_notebook


def execute_notebook(
    notebook: Mapping[str, Any],
    *,
    timeout: int = 120,
    kernel_name: str | None = None,
    cwd: str | Path | None = None,
    allow_errors: bool = False,
) -> dict[str, Any]:
    """Execute a notebook in-process with nbclient and return the updated document.

    Requires the ``nbops[execute]`` extra.
    """
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
        return parse_notebook(nbformat.writes(executed), validate=False)

    return _run()


def _notebook_client_class() -> Any:
    try:
        from nbclient import NotebookClient
    except ImportError as exc:
        raise MissingExtraError(
            "Notebook execution requires the optional extra 'nbops[execute]' (nbclient)."
        ) from exc
    return NotebookClient
