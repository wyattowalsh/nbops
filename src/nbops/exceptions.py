"""Shared exceptions for nbops."""

from __future__ import annotations


class NbopsError(Exception):
    """Base error for all nbops failures."""


class NotebookNotFoundError(NbopsError, FileNotFoundError):
    """Raised when a notebook path does not exist."""


class InvalidNotebookError(NbopsError, ValueError):
    """Raised when a document is not a usable Jupyter notebook."""


class ExecuteError(NbopsError):
    """Raised when notebook execution fails."""


class MissingExtraError(NbopsError):
    """Raised when an optional extra is required but not installed."""


class ObserverError(NbopsError):
    """Raised when a notebook runtime observer operation fails."""


class InvalidObserverConfigError(ObserverError, ValueError):
    """Raised when observer configuration or control arguments are invalid."""


class OutputPathError(ObserverError, ValueError):
    """Raised when an observer output path fails preflight."""


class TerminalObserverError(ObserverError):
    """Raised when a terminal observer rejects a new control event."""
