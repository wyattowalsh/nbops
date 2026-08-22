"""Canonical catalog of notebook operations shared by library, CLI, and API."""

from __future__ import annotations

from pydantic import BaseModel


class Operation(BaseModel):
    """One notebook operation and the surfaces that expose it."""

    name: str
    summary: str
    library: str
    cli: str | None = None
    api: str | None = None
    batch: str | None = None


OPERATIONS: tuple[Operation, ...] = (
    Operation(
        name="stats",
        summary="Cell, line, output, and kernel statistics.",
        library="nbops.inspect.compute_stats",
        cli="nbops stats",
        api="POST /notebooks/stats",
        batch="nbops batch stats",
    ),
    Operation(
        name="inspect",
        summary="Stats plus markdown outline and top-level imports.",
        library="nbops.inspect",
        cli="nbops inspect",
        api="POST /notebooks/inspect",
    ),
    Operation(
        name="headings",
        summary="Markdown heading outline.",
        library="nbops.inspect.outline",
        cli="nbops headings",
        api="POST /notebooks/headings",
    ),
    Operation(
        name="imports",
        summary="Top-level imports from code cells.",
        library="nbops.inspect.extract_imports",
        cli="nbops imports",
        api="POST /notebooks/imports",
    ),
    Operation(
        name="lint",
        summary="Structural quality report (NB000–NB011).",
        library="nbops.lint.lint_notebook",
        cli="nbops lint",
        api="POST /notebooks/lint",
        batch="nbops batch lint",
    ),
    Operation(
        name="clean",
        summary="Strip outputs, execution counts, optional ids and empty cells.",
        library="nbops.clean.clean_notebook",
        cli="nbops clean",
        api="POST /notebooks/clean",
        batch="nbops batch clean",
    ),
    Operation(
        name="convert",
        summary="Convert to percent Python, code-only script, or Markdown.",
        library="nbops.convert.convert_notebook",
        cli="nbops convert",
        api="POST /notebooks/convert",
    ),
    Operation(
        name="concat",
        summary="Concatenate notebooks cell-wise.",
        library="nbops.transform.concat_notebooks",
        cli="nbops concat",
        api="POST /notebooks/concat",
    ),
    Operation(
        name="split",
        summary="Split a notebook on markdown headings.",
        library="nbops.transform.split_by_headings",
        cli="nbops split",
        api="POST /notebooks/split",
    ),
    Operation(
        name="diff",
        summary="Cell-level structural diff.",
        library="nbops.diff.diff_notebooks",
        cli="nbops diff",
        api="POST /notebooks/diff",
    ),
    Operation(
        name="new",
        summary="Create an empty nbformat v4 notebook.",
        library="nbops.io.new_notebook",
        cli="nbops new",
        api="POST /notebooks/new",
    ),
    Operation(
        name="kernel",
        summary="Set kernelspec and language_info.",
        library="nbops.transform.set_kernelspec",
        cli="nbops kernel",
        api="POST /notebooks/kernel",
    ),
    Operation(
        name="exec",
        summary="Execute with nbclient (requires nbops[execute]).",
        library="nbops.execute.execute_notebook",
        cli="nbops exec",
        api="POST /notebooks/execute",
    ),
    Operation(
        name="filter",
        summary="Keep cells by type and/or tags.",
        library="nbops.transform.filter_cells",
        cli="nbops filter",
        api="POST /notebooks/filter",
    ),
    Operation(
        name="tag",
        summary="Add tags to a cell.",
        library="nbops.transform.add_tags",
        cli="nbops tag",
        api="POST /notebooks/tag",
    ),
    Operation(
        name="ids",
        summary="Assign missing or duplicate cell ids.",
        library="nbops.transform.ensure_cell_ids",
        cli="nbops ids",
        api="POST /notebooks/ids",
    ),
    Operation(
        name="from-py",
        summary="Parse a Jupytext-style percent Python script into a notebook.",
        library="nbops.convert.from_percent_python",
        cli="nbops from-py",
        api="POST /notebooks/from-py",
    ),
    Operation(
        name="ops",
        summary="List the operations catalog.",
        library="nbops.operations.OPERATIONS",
        cli="nbops ops",
        api="GET /operations",
    ),
)


def operation_names() -> list[str]:
    """Return catalog names in declaration order."""
    return [item.name for item in OPERATIONS]


def catalog_cli_argv(item: Operation) -> list[str] | None:
    """Return Typer argv tokens for a catalog CLI entry (after ``nbops``)."""
    if item.cli is None:
        return None
    parts = item.cli.split()
    if not parts or parts[0] != "nbops":
        raise ValueError(f"Catalog CLI must start with 'nbops': {item.cli}")
    return parts[1:]


def catalog_http_route(item: Operation) -> tuple[str, str] | None:
    """Return ``(METHOD, path)`` for a catalog HTTP entry."""
    if item.api is None:
        return None
    method, _, path = item.api.partition(" ")
    if not method or not path.startswith("/"):
        raise ValueError(f"Catalog API must look like 'METHOD /path': {item.api}")
    return method.upper(), path
