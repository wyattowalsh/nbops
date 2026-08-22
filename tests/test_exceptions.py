"""Unit tests for nbops exception types."""

from __future__ import annotations

from nbops.exceptions import (
    ExecuteError,
    InvalidNotebookError,
    MissingExtraError,
    NbopsError,
    NotebookNotFoundError,
)


def test_exception_hierarchy() -> None:
    assert issubclass(NotebookNotFoundError, NbopsError)
    assert issubclass(NotebookNotFoundError, FileNotFoundError)
    assert issubclass(InvalidNotebookError, NbopsError)
    assert issubclass(InvalidNotebookError, ValueError)
    assert issubclass(ExecuteError, NbopsError)
    assert issubclass(MissingExtraError, NbopsError)


def test_exception_messages() -> None:
    assert str(InvalidNotebookError("not a notebook")) == "not a notebook"
    assert str(MissingExtraError("need extra")) == "need extra"
