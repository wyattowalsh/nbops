"""Backward-compatible core exports (inspect + io)."""

from __future__ import annotations

from nbops.inspect import NotebookStats, compute_stats, stats_for_file
from nbops.io import load_notebook

__all__ = ["NotebookStats", "compute_stats", "load_notebook", "stats_for_file"]
