"""Typer-based command line interface for nbops."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from loguru import logger

from nbops import __version__
from nbops.core import stats_for_file

app = typer.Typer(
    name="nbops",
    help="Lightweight operations toolkit for Jupyter notebooks.",
    no_args_is_help=True,
    add_completion=False,
)


@app.command()
def version() -> None:
    """Print the installed nbops version."""
    typer.echo(__version__)


@app.command()
def stats(
    notebook: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, readable=True, help="Path to a .ipynb file."),
    ],
    as_json: Annotated[
        bool, typer.Option("--json", help="Emit machine-readable JSON instead of a table.")
    ] = False,
) -> None:
    """Compute and display statistics for a Jupyter notebook."""
    result = stats_for_file(notebook)

    if as_json:
        typer.echo(result.model_dump_json(indent=2))
        return

    logger.debug("Computed stats for {}", notebook)
    typer.echo(f"Notebook: {notebook}")
    typer.echo(f"  Total cells   : {result.total_cells}")
    typer.echo(f"  Code cells    : {result.code_cells}")
    typer.echo(f"  Markdown cells: {result.markdown_cells}")
    typer.echo(f"  Raw cells     : {result.raw_cells}")
    typer.echo(f"  Code lines    : {result.code_lines}")
    typer.echo(f"  Kernel        : {result.kernel or '-'}")
    typer.echo(f"  Language      : {result.language or '-'}")


if __name__ == "__main__":  # pragma: no cover
    app()
