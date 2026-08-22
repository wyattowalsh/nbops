"""nbops - lightweight operations toolkit for Jupyter notebooks."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("nbops")
except PackageNotFoundError:  # pragma: no cover - only during local, uninstalled use
    __version__ = "0.0.0.dev0"

from nbops.core import NotebookStats, compute_stats

__all__ = ["NotebookStats", "__version__", "compute_stats"]
