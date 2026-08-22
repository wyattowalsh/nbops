"""Tests for the nbops Typer CLI."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from nbops import __version__
from nbops.cli import app

runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_stats_command_table(sample_notebook_file: Path) -> None:
    result = runner.invoke(app, ["stats", str(sample_notebook_file)])
    assert result.exit_code == 0
    assert "Total cells   : 4" in result.stdout
    assert "Code lines    : 4" in result.stdout


def test_stats_command_json(sample_notebook_file: Path) -> None:
    result = runner.invoke(app, ["stats", str(sample_notebook_file), "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["total_cells"] == 4
    assert payload["language"] == "python"


def test_stats_command_missing_file() -> None:
    result = runner.invoke(app, ["stats", "does-not-exist.ipynb"])
    assert result.exit_code != 0
