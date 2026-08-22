"""Typer CLI for general notebook operations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import typer
from loguru import logger

from nbops import __version__
from nbops.batch import map_notebooks
from nbops.clean import clean_notebook
from nbops.convert import convert_notebook
from nbops.diff import diff_notebooks
from nbops.exceptions import ExecuteError, InvalidNotebookError, MissingExtraError, NbopsError
from nbops.inspect import compute_stats, extract_imports, outline, stats_for_file
from nbops.io import load_notebook, new_notebook, save_notebook
from nbops.lint import lint_notebook
from nbops.models import CleanOptions
from nbops.transform import concat_notebooks, set_kernelspec, split_by_headings

app = typer.Typer(
    name="nbops",
    help="General operations toolkit for Jupyter notebooks.",
    no_args_is_help=True,
    add_completion=False,
)

batch_app = typer.Typer(help="Run an operation across a directory of notebooks.")
app.add_typer(batch_app, name="batch")


def _fail(message: str, code: int = 1) -> None:
    typer.secho(message, err=True, fg=typer.colors.RED)
    raise typer.Exit(code)


def _emit_json(payload: Any) -> None:
    if hasattr(payload, "model_dump"):
        typer.echo(payload.model_dump_json(indent=2))
        return
    typer.echo(json.dumps(payload, indent=2, default=str))


def _load(path: Path, *, validate: bool = False) -> dict[str, Any]:
    try:
        return load_notebook(path, validate=validate)
    except (OSError, NbopsError, ValueError) as exc:
        _fail(str(exc))
        raise  # pragma: no cover


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
    result = stats_for_file(notebook, validate=False)
    if as_json:
        _emit_json(result)
        return
    logger.debug("Computed stats for {}", notebook)
    typer.echo(f"Notebook: {notebook}")
    typer.echo(f"  Total cells   : {result.total_cells}")
    typer.echo(f"  Code cells    : {result.code_cells}")
    typer.echo(f"  Markdown cells: {result.markdown_cells}")
    typer.echo(f"  Raw cells     : {result.raw_cells}")
    typer.echo(f"  Code lines    : {result.code_lines}")
    typer.echo(f"  Markdown lines: {result.markdown_lines}")
    typer.echo(f"  Empty cells   : {result.empty_cells}")
    typer.echo(f"  Executed code : {result.executed_code_cells}")
    typer.echo(f"  Error outputs : {result.error_outputs}")
    typer.echo(f"  Kernel        : {result.kernel or '-'}")
    typer.echo(f"  Language      : {result.language or '-'}")


@app.command("inspect")
def inspect_cmd(
    notebook: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
) -> None:
    """Emit the full inspect payload (stats, outline, imports) as JSON."""
    document = _load(notebook, validate=False)
    payload = {
        "stats": compute_stats(document).model_dump(),
        "outline": [item.model_dump() for item in outline(document)],
        "imports": [item.model_dump() for item in extract_imports(document)],
    }
    _emit_json(payload)


@app.command()
def headings(
    notebook: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    as_json: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Print markdown headings in document order."""
    items = outline(_load(notebook, validate=False))
    if as_json:
        _emit_json([item.model_dump() for item in items])
        return
    for item in items:
        typer.echo(f"{'#' * item.level} {item.title}  (cell {item.cell_index})")


@app.command("imports")
def imports_cmd(
    notebook: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    as_json: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """List top-level imports from code cells."""
    items = extract_imports(_load(notebook, validate=False))
    if as_json:
        _emit_json([item.model_dump() for item in items])
        return
    for item in items:
        names = ", ".join(item.names)
        typer.echo(f"{item.module} ({names})  cell {item.cell_index}")


@app.command()
def lint(
    notebook: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    as_json: Annotated[bool, typer.Option("--json")] = False,
    strict: Annotated[
        bool, typer.Option("--strict", help="Exit non-zero on warnings as well as errors.")
    ] = False,
) -> None:
    """Lint a notebook for structural quality issues."""
    report = lint_notebook(_load(notebook, validate=False))
    if as_json:
        _emit_json(report)
    else:
        if not report.issues:
            typer.echo("ok")
        for issue in report.issues:
            loc = f"cell {issue.cell_index}" if issue.cell_index is not None else "notebook"
            typer.echo(f"{issue.severity}: {issue.code} {loc}: {issue.message}")
        typer.echo(
            f"{report.issue_count} issue(s), {report.error_count} error(s), "
            f"{report.warning_count} warning(s)"
        )
    if report.error_count > 0 or (strict and report.warning_count > 0):
        raise typer.Exit(1)


@app.command()
def clean(
    notebook: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    output: Annotated[
        Path | None, typer.Option("--output", "-o", help="Write the cleaned notebook here.")
    ] = None,
    in_place: Annotated[bool, typer.Option("--in-place", help="Overwrite the input file.")] = False,
    keep_outputs: Annotated[bool, typer.Option("--keep-outputs")] = False,
    keep_counts: Annotated[bool, typer.Option("--keep-counts")] = False,
    strip_ids: Annotated[bool, typer.Option("--strip-ids")] = False,
    drop_empty: Annotated[bool, typer.Option("--drop-empty")] = False,
) -> None:
    """Strip outputs, execution counts, and optional cell residue."""
    if output is None and not in_place:
        _fail("Specify --output PATH or --in-place.")
    document = _load(notebook, validate=False)
    cleaned = clean_notebook(
        document,
        CleanOptions(
            outputs=not keep_outputs,
            execution_counts=not keep_counts,
            cell_ids=strip_ids,
            empty_cells=drop_empty,
        ),
    )
    dest = notebook if in_place else output
    assert dest is not None
    save_notebook(cleaned, dest, validate=False)
    typer.echo(str(dest))


@app.command()
def convert(
    notebook: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    fmt: Annotated[str, typer.Option("--to", help="py, script, or md.")] = "py",
    output: Annotated[Path | None, typer.Option("--output", "-o")] = None,
) -> None:
    """Convert a notebook to percent Python, a code-only script, or Markdown."""
    result = convert_notebook(_load(notebook, validate=False), fmt)
    if output is None:
        typer.echo(result.text, nl=False)
        return
    output.write_text(result.text, encoding="utf-8")
    typer.echo(str(output))


@app.command()
def concat(
    notebooks: Annotated[list[Path], typer.Argument(exists=True, dir_okay=False, readable=True)],
    output: Annotated[Path, typer.Option("--output", "-o")],
) -> None:
    """Concatenate two or more notebooks into one."""
    if len(notebooks) < 2:
        _fail("concat requires at least two notebooks.")
    merged = concat_notebooks(_load(path, validate=False) for path in notebooks)
    save_notebook(merged, output, validate=False)
    typer.echo(str(output))


@app.command("split")
def split_cmd(
    notebook: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    output_dir: Annotated[Path, typer.Option("--output-dir", "-o")],
    level: Annotated[int, typer.Option("--level", min=1, max=6)] = 1,
) -> None:
    """Split a notebook on markdown headings into a directory of notebooks."""
    sections = split_by_headings(_load(notebook, validate=False), level=level)
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for index, (title, section) in enumerate(sections):
        slug = _slug(title) or f"section-{index}"
        path = output_dir / f"{index:02d}-{slug}.ipynb"
        save_notebook(section, path, validate=False)
        written.append(str(path))
    typer.echo("\n".join(written) if written else "(no sections)")


@app.command("diff")
def diff_cmd(
    left: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    right: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    as_json: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Diff two notebooks at cell granularity."""
    report = diff_notebooks(_load(left, validate=False), _load(right, validate=False))
    if as_json:
        _emit_json(report)
        return
    typer.echo(
        f"left={report.left_cells} right={report.right_cells} "
        f"equal={report.equal} changed={report.changed} "
        f"added={report.added} removed={report.removed} identical={report.identical}"
    )
    for cell in report.cells:
        if cell.change == "equal":
            continue
        typer.echo(
            f"  [{cell.index}] {cell.change} {cell.left_type or '-'} -> {cell.right_type or '-'}"
        )


@app.command("new")
def new_cmd(
    path: Annotated[Path, typer.Argument(help="Path to write the new notebook.")],
    kernel: Annotated[str, typer.Option("--kernel")] = "python3",
    language: Annotated[str, typer.Option("--language")] = "python",
) -> None:
    """Create an empty nbformat v4 notebook."""
    if path.exists():
        _fail(f"Refusing to overwrite existing file: {path}")
    save_notebook(
        new_notebook(kernel_name=kernel, display_name=kernel, language=language),
        path,
        validate=True,
    )
    typer.echo(str(path))


@app.command()
def kernel(
    notebook: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    name: Annotated[str, typer.Option("--name")],
    display_name: Annotated[str | None, typer.Option("--display-name")] = None,
    language: Annotated[str | None, typer.Option("--language")] = None,
    in_place: Annotated[bool, typer.Option("--in-place")] = True,
    output: Annotated[Path | None, typer.Option("--output", "-o")] = None,
) -> None:
    """Set the notebook kernelspec."""
    updated = set_kernelspec(
        _load(notebook, validate=False),
        name=name,
        display_name=display_name,
        language=language,
    )
    dest = output or notebook
    if output is None and not in_place:
        _fail("Specify --output PATH or --in-place.")
    save_notebook(updated, dest, validate=False)
    typer.echo(str(dest))


@app.command("exec")
def exec_cmd(
    notebook: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    output: Annotated[Path | None, typer.Option("--output", "-o")] = None,
    timeout: Annotated[int, typer.Option("--timeout", min=1)] = 120,
    kernel_name: Annotated[str | None, typer.Option("--kernel")] = None,
    allow_errors: Annotated[bool, typer.Option("--allow-errors")] = False,
) -> None:
    """Execute a notebook (requires the optional extra nbops[execute])."""
    from nbops.execute import execute_notebook

    dest = output or notebook
    try:
        executed = execute_notebook(
            _load(notebook, validate=False),
            timeout=timeout,
            kernel_name=kernel_name,
            cwd=notebook.parent,
            allow_errors=allow_errors,
        )
    except (MissingExtraError, ExecuteError, InvalidNotebookError) as exc:
        _fail(str(exc))
        return
    save_notebook(executed, dest, validate=False)
    typer.echo(str(dest))


@batch_app.command("stats")
def batch_stats(
    root: Annotated[Path, typer.Argument(exists=True, readable=True)],
    as_json: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Compute stats for every notebook under a directory."""
    items = map_notebooks(root, lambda path: stats_for_file(path, validate=False).model_dump())
    if as_json:
        _emit_json([item.model_dump() for item in items])
        return
    for item in items:
        if item.ok and item.result is not None:
            typer.echo(f"{item.path}: {item.result['total_cells']} cells")
        else:
            typer.echo(f"{item.path}: ERROR {item.error}")


@batch_app.command("lint")
def batch_lint(
    root: Annotated[Path, typer.Argument(exists=True, readable=True)],
    as_json: Annotated[bool, typer.Option("--json")] = False,
    strict: Annotated[bool, typer.Option("--strict")] = False,
) -> None:
    """Lint every notebook under a directory."""
    items = map_notebooks(
        root, lambda path: lint_notebook(load_notebook(path, validate=False)).model_dump()
    )
    failed = False
    if as_json:
        _emit_json([item.model_dump() for item in items])
    for item in items:
        if not item.ok or item.result is None:
            failed = True
            if not as_json:
                typer.echo(f"{item.path}: ERROR {item.error}")
            continue
        errors = int(item.result["error_count"])
        warnings = int(item.result["warning_count"])
        if errors or (strict and warnings):
            failed = True
        if not as_json:
            typer.echo(f"{item.path}: {item.result['issue_count']} issue(s)")
    if failed:
        raise typer.Exit(1)


def _slug(title: str) -> str:
    chars = [ch.lower() if ch.isalnum() else "-" for ch in title.strip()]
    slug = "".join(chars)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


if __name__ == "__main__":  # pragma: no cover
    app()
