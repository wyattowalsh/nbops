"""Unit tests for nbops exception types."""

from __future__ import annotations

from nbops.exceptions import (
    ExecuteError,
    InvalidNotebookError,
    InvalidObserverConfigError,
    MissingExtraError,
    NbopsError,
    NotebookNotFoundError,
    ObserverError,
    OutputPathError,
    TerminalObserverError,
)


def test_exception_hierarchy() -> None:
    assert issubclass(NotebookNotFoundError, NbopsError)
    assert issubclass(NotebookNotFoundError, FileNotFoundError)
    assert issubclass(InvalidNotebookError, NbopsError)
    assert issubclass(InvalidNotebookError, ValueError)
    assert issubclass(ExecuteError, NbopsError)
    assert issubclass(MissingExtraError, NbopsError)
    assert issubclass(ObserverError, NbopsError)
    assert issubclass(InvalidObserverConfigError, ObserverError)
    assert issubclass(InvalidObserverConfigError, ValueError)
    assert issubclass(OutputPathError, ObserverError)
    assert issubclass(TerminalObserverError, ObserverError)


def test_exception_messages() -> None:
    assert str(InvalidNotebookError("not a notebook")) == "not a notebook"
    assert str(MissingExtraError("need extra")) == "need extra"
