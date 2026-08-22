"""nbops — general operations toolkit for Jupyter notebooks."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("nbops")
except PackageNotFoundError:  # pragma: no cover - only during local, uninstalled use
    __version__ = "0.0.0.dev0"

from nbops.clean import clean_notebook
from nbops.convert import convert_notebook
from nbops.diff import diff_notebooks
from nbops.inspect import NotebookStats, compute_stats, extract_imports, outline, stats_for_file
from nbops.io import load_notebook, new_notebook, save_notebook
from nbops.lint import lint_notebook

__all__ = [
    "NotebookStats",
    "__version__",
    "clean_notebook",
    "compute_stats",
    "convert_notebook",
    "diff_notebooks",
    "extract_imports",
    "lint_notebook",
    "load_notebook",
    "new_notebook",
    "outline",
    "save_notebook",
    "stats_for_file",
]
