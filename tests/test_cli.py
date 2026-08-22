"""Tests for the nbops Typer CLI."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
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


def test_inspect_headings_imports_lint(sample_notebook_file: Path) -> None:
    inspect_result = runner.invoke(app, ["inspect", str(sample_notebook_file)])
    assert inspect_result.exit_code == 0
    payload = json.loads(inspect_result.stdout)
    assert payload["stats"]["total_cells"] == 4
    assert payload["outline"][0]["title"] == "Title"

    headings = runner.invoke(app, ["headings", str(sample_notebook_file)])
    assert headings.exit_code == 0
    assert "Title" in headings.stdout

    imports = runner.invoke(app, ["imports", str(sample_notebook_file), "--json"])
    assert imports.exit_code == 0
    assert json.loads(imports.stdout)[0]["module"] == "os"

    lint = runner.invoke(app, ["lint", str(sample_notebook_file)])
    assert lint.exit_code == 0


def test_clean_convert_concat_diff_new(tmp_path: Path, sample_notebook_file: Path) -> None:
    cleaned = tmp_path / "cleaned.ipynb"
    clean = runner.invoke(app, ["clean", str(sample_notebook_file), "-o", str(cleaned)])
    assert clean.exit_code == 0
    assert cleaned.is_file()

    converted = runner.invoke(app, ["convert", str(sample_notebook_file), "--to", "md"])
    assert converted.exit_code == 0
    assert "# Title" in converted.stdout

    out_py = tmp_path / "demo.py"
    to_py = runner.invoke(
        app, ["convert", str(sample_notebook_file), "--to", "py", "-o", str(out_py)]
    )
    assert to_py.exit_code == 0
    assert out_py.read_text(encoding="utf-8").startswith("# %%")

    merged = tmp_path / "merged.ipynb"
    concat = runner.invoke(
        app, ["concat", str(sample_notebook_file), str(cleaned), "-o", str(merged)]
    )
    assert concat.exit_code == 0

    diff = runner.invoke(app, ["diff", str(sample_notebook_file), str(cleaned)])
    assert diff.exit_code == 0

    created = tmp_path / "fresh.ipynb"
    new = runner.invoke(app, ["new", str(created)])
    assert new.exit_code == 0
    assert created.is_file()
    again = runner.invoke(app, ["new", str(created)])
    assert again.exit_code != 0


def test_split_kernel_and_batch(tmp_path: Path, sample_notebook_file: Path) -> None:
    split_dir = tmp_path / "parts"
    split = runner.invoke(app, ["split", str(sample_notebook_file), "-o", str(split_dir)])
    assert split.exit_code == 0
    assert any(split_dir.glob("*.ipynb"))

    kernel = runner.invoke(
        app, ["kernel", str(sample_notebook_file), "--name", "python3", "--language", "python"]
    )
    assert kernel.exit_code == 0

    batch = runner.invoke(app, ["batch", "stats", str(tmp_path), "--json"])
    assert batch.exit_code == 0
    payload = json.loads(batch.stdout)
    assert isinstance(payload, list)
    assert payload


def test_clean_requires_output(sample_notebook_file: Path) -> None:
    result = runner.invoke(app, ["clean", str(sample_notebook_file)])
    assert result.exit_code != 0


def test_lint_strict_errors(tmp_path: Path, error_notebook: dict) -> None:
    path = tmp_path / "err.ipynb"
    path.write_text(json.dumps(error_notebook), encoding="utf-8")
    result = runner.invoke(app, ["lint", str(path)])
    assert result.exit_code != 0


def test_exec_missing_extra(monkeypatch: pytest.MonkeyPatch, sample_notebook_file: Path) -> None:
    from nbops import execute as execute_mod
    from nbops.exceptions import MissingExtraError

    monkeypatch.setattr(
        execute_mod,
        "_notebook_client_class",
        lambda: (_ for _ in ()).throw(MissingExtraError("need extra")),
    )
    result = runner.invoke(app, ["exec", str(sample_notebook_file)])
    assert result.exit_code != 0
    assert "need extra" in result.output


def test_cli_json_and_batch_and_concat_guard(tmp_path: Path, sample_notebook_file: Path) -> None:
    headings = runner.invoke(app, ["headings", str(sample_notebook_file), "--json"])
    assert headings.exit_code == 0
    assert json.loads(headings.stdout)[0]["title"] == "Title"

    imports = runner.invoke(app, ["imports", str(sample_notebook_file)])
    assert imports.exit_code == 0
    assert "os" in imports.stdout

    lint_json = runner.invoke(app, ["lint", str(sample_notebook_file), "--json"])
    assert lint_json.exit_code == 0
    assert "issue_count" in json.loads(lint_json.stdout)

    concat = runner.invoke(
        app, ["concat", str(sample_notebook_file), "-o", str(tmp_path / "x.ipynb")]
    )
    assert concat.exit_code != 0

    kernel = runner.invoke(
        app,
        [
            "kernel",
            str(sample_notebook_file),
            "--name",
            "python3",
            "--output",
            str(tmp_path / "k.ipynb"),
        ],
    )
    assert kernel.exit_code == 0

    table = runner.invoke(app, ["batch", "stats", str(tmp_path)])
    assert table.exit_code == 0

    lint_batch = runner.invoke(app, ["batch", "lint", str(tmp_path)])
    assert lint_batch.exit_code in {0, 1}

    diff_json = runner.invoke(
        app, ["diff", str(sample_notebook_file), str(sample_notebook_file), "--json"]
    )
    assert diff_json.exit_code == 0
    assert json.loads(diff_json.stdout)["identical"] is True
