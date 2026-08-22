"""nbops — general operations toolkit for Jupyter notebooks."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("nbops")
except PackageNotFoundError:  # pragma: no cover - only during local, uninstalled use
    __version__ = "0.0.0.dev0"

from nbops.clean import clean_notebook
from nbops.convert import convert_notebook, from_percent_python, to_percent_python
from nbops.diff import diff_notebooks
from nbops.execute import execute_notebook
from nbops.inspect import (
    NotebookStats,
    compute_stats,
    extract_imports,
    list_outputs,
    outline,
    stats_for_file,
)
from nbops.io import load_notebook, new_notebook, save_notebook, validate_notebook
from nbops.lint import ISSUE_CATALOG, lint_notebook
from nbops.operations import OPERATIONS
from nbops.transform import (
    add_tags,
    concat_notebooks,
    ensure_cell_ids,
    filter_cells,
    remove_tags,
    set_kernelspec,
    split_by_headings,
)

__all__ = [
    "ISSUE_CATALOG",
    "OPERATIONS",
    "NotebookStats",
    "__version__",
    "add_tags",
    "clean_notebook",
    "compute_stats",
    "concat_notebooks",
    "convert_notebook",
    "diff_notebooks",
    "ensure_cell_ids",
    "execute_notebook",
    "extract_imports",
    "filter_cells",
    "from_percent_python",
    "lint_notebook",
    "list_outputs",
    "load_notebook",
    "new_notebook",
    "outline",
    "remove_tags",
    "save_notebook",
    "set_kernelspec",
    "split_by_headings",
    "stats_for_file",
    "to_percent_python",
    "validate_notebook",
]
