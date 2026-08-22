"""Tests for the operations catalog and lint issue codes."""

from __future__ import annotations

import pytest
from fastapi.routing import APIRoute
from typer.main import get_command

from nbops.api import app as api_app
from nbops.cli import app as cli_app
from nbops.lint import ISSUE_CATALOG, lint_notebook
from nbops.operations import (
    OPERATIONS,
    Operation,
    catalog_cli_argv,
    catalog_http_route,
    operation_names,
)


def test_issue_catalog_covers_nb000_through_nb011() -> None:
    assert list(ISSUE_CATALOG) == [f"NB{index:03d}" for index in range(12)]


def test_lint_emits_missing_cell_id() -> None:
    report = lint_notebook(
        {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": "# Title\n",
                }
            ],
            "metadata": {"kernelspec": {"name": "python3"}},
            "nbformat": 4,
            "nbformat_minor": 5,
        }
    )
    assert any(issue.code == "NB009" for issue in report.issues)


def test_operation_catalog_names_are_unique() -> None:
    names = operation_names()
    assert len(names) == len(set(names))
    assert "stats" in names
    assert "ops" in names
    assert "from-py" in names
    assert "outputs" in names
    assert "validate" in names
    assert all(item.library for item in OPERATIONS)


def test_catalog_cli_and_api_surfaces_exist() -> None:
    click_group = get_command(cli_app)
    implemented_http = {
        (method, route.path)
        for route in api_app.routes
        if isinstance(route, APIRoute)
        for method in route.methods
        if method not in {"HEAD", "OPTIONS"}
    }
    catalog_http: set[tuple[str, str]] = set()
    for item in OPERATIONS:
        argv = catalog_cli_argv(item)
        if argv is not None:
            current = click_group
            for token in argv:
                commands = getattr(current, "commands", None)
                assert commands is not None, f"missing CLI group for {item.cli}"
                assert token in commands, f"missing CLI command {item.cli}"
                current = commands[token]
        route = catalog_http_route(item)
        if route is not None:
            assert route in implemented_http, f"missing API route {item.api}"
            catalog_http.add(route)

    notebook_routes = {
        pair
        for pair in implemented_http
        if pair[1] == "/operations" or pair[1].startswith("/notebooks/")
    }
    assert notebook_routes == catalog_http


def test_catalog_parsers_reject_malformed_entries() -> None:
    with pytest.raises(ValueError, match="nbops"):
        catalog_cli_argv(Operation(name="x", summary="x", library="x", cli="wrong stats"))
    with pytest.raises(ValueError, match="METHOD"):
        catalog_http_route(Operation(name="x", summary="x", library="x", api="not-a-route"))
    assert catalog_cli_argv(Operation(name="x", summary="x", library="x")) is None
    assert catalog_http_route(Operation(name="x", summary="x", library="x")) is None
