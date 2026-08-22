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


def test_demo_notebook_stats_contract() -> None:
    demo = Path(__file__).resolve().parents[1] / "examples" / "demo.ipynb"
    result = runner.invoke(app, ["stats", str(demo), "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["total_cells"] == 4
    assert payload["code_cells"] == 2
    assert payload["code_lines"] == 4
    assert payload["kernel"] == "Python 3"
    assert payload["language"] == "python"


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
    assert payload["outputs"][0]["output_type"] == "stream"

    headings = runner.invoke(app, ["headings", str(sample_notebook_file)])
    assert headings.exit_code == 0
    assert "Title" in headings.stdout

    imports = runner.invoke(app, ["imports", str(sample_notebook_file), "--json"])
    assert imports.exit_code == 0
    assert json.loads(imports.stdout)[0]["module"] == "os"

    lint = runner.invoke(app, ["lint", str(sample_notebook_file)])
    assert lint.exit_code == 0

    listed = runner.invoke(app, ["outputs", str(sample_notebook_file)])
    assert listed.exit_code == 0
    assert "stdout" in listed.stdout

    listed_json = runner.invoke(app, ["outputs", str(sample_notebook_file), "--json"])
    assert listed_json.exit_code == 0
    assert json.loads(listed_json.stdout)[0]["output_type"] == "stream"

    valid = runner.invoke(app, ["validate", str(sample_notebook_file)])
    assert valid.exit_code == 0
    assert "ok" in valid.stdout


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

    restored = tmp_path / "from-py.ipynb"
    from_py = runner.invoke(app, ["from-py", str(out_py), "-o", str(restored)])
    assert from_py.exit_code == 0
    assert json.loads(restored.read_text(encoding="utf-8"))["cells"]

    merged = tmp_path / "merged.ipynb"
    concat = runner.invoke(
        app, ["concat", str(sample_notebook_file), str(cleaned), "-o", str(merged)]
    )
    assert concat.exit_code == 0

    diff = runner.invoke(app, ["diff", str(sample_notebook_file), str(cleaned)])
    assert diff.exit_code == 0

    changed = tmp_path / "changed.ipynb"
    payload = json.loads(sample_notebook_file.read_text(encoding="utf-8"))
    payload["cells"][0]["source"] = "# Different\n"
    changed.write_text(json.dumps(payload), encoding="utf-8")
    diff_changed = runner.invoke(app, ["diff", str(sample_notebook_file), str(changed)])
    assert diff_changed.exit_code == 0
    assert "changed" in diff_changed.stdout

    created = tmp_path / "fresh.ipynb"
    new = runner.invoke(app, ["new", str(created)])
    assert new.exit_code == 0
    assert created.is_file()
    empty_outputs = runner.invoke(app, ["outputs", str(created)])
    assert empty_outputs.exit_code == 0
    assert "no outputs" in empty_outputs.stdout
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


def test_lint_ok_when_no_issues(tmp_path: Path) -> None:
    path = tmp_path / "ok.ipynb"
    path.write_text(
        json.dumps(
            {
                "cells": [
                    {
                        "cell_type": "markdown",
                        "id": "title",
                        "metadata": {},
                        "source": "# Title\n",
                    },
                    {
                        "cell_type": "code",
                        "id": "code",
                        "execution_count": 1,
                        "metadata": {},
                        "outputs": [{"output_type": "stream", "name": "stdout", "text": "1\n"}],
                        "source": "print(1)\n",
                    },
                ],
                "metadata": {"kernelspec": {"name": "python3"}},
                "nbformat": 4,
                "nbformat_minor": 5,
            }
        ),
        encoding="utf-8",
    )
    result = runner.invoke(app, ["lint", str(path)])
    assert result.exit_code == 0
    assert "ok" in result.stdout


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


def test_ops_filter_tag_ids_and_batch_clean(tmp_path: Path, sample_notebook_file: Path) -> None:
    ops = runner.invoke(app, ["ops", "--json"])
    assert ops.exit_code == 0
    names = {item["name"] for item in json.loads(ops.stdout)}
    assert "stats" in names
    assert "filter" in names

    filtered = tmp_path / "code-only.ipynb"
    filt = runner.invoke(
        app,
        ["filter", str(sample_notebook_file), "--type", "code", "-o", str(filtered)],
    )
    assert filt.exit_code == 0
    assert json.loads(filtered.read_text(encoding="utf-8"))["cells"]

    tagged = tmp_path / "tagged.ipynb"
    tag = runner.invoke(
        app,
        [
            "tag",
            str(sample_notebook_file),
            "--cell",
            "0",
            "--add",
            "intro",
            "-o",
            str(tagged),
        ],
    )
    assert tag.exit_code == 0

    missing_ids = tmp_path / "noid.ipynb"
    missing_ids.write_text(
        json.dumps(
            {
                "cells": [
                    {"cell_type": "markdown", "metadata": {}, "source": "# T\n"},
                ],
                "metadata": {"kernelspec": {"name": "python3"}},
                "nbformat": 4,
                "nbformat_minor": 5,
            }
        ),
        encoding="utf-8",
    )
    with_ids = tmp_path / "with-ids.ipynb"
    ids = runner.invoke(app, ["ids", str(missing_ids), "-o", str(with_ids)])
    assert ids.exit_code == 0
    assert json.loads(with_ids.read_text(encoding="utf-8"))["cells"][0]["id"]

    batch_dir = tmp_path / "batch"
    batch_dir.mkdir()
    target = batch_dir / "demo.ipynb"
    target.write_text(sample_notebook_file.read_text(encoding="utf-8"), encoding="utf-8")
    cleaned = runner.invoke(app, ["batch", "clean", str(batch_dir), "--json"])
    assert cleaned.exit_code == 0
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["cells"][1]["outputs"] == []

    ok_dir = tmp_path / "ok-batch"
    ok_dir.mkdir()
    created = ok_dir / "fresh.ipynb"
    new = runner.invoke(app, ["new", str(created)])
    assert new.exit_code == 0
    validated = runner.invoke(app, ["batch", "validate", str(ok_dir), "--json"])
    assert validated.exit_code == 0
    assert json.loads(validated.stdout)[0]["ok"] is True


def test_filter_and_tag_require_output(sample_notebook_file: Path) -> None:
    filt = runner.invoke(app, ["filter", str(sample_notebook_file), "--type", "code"])
    assert filt.exit_code != 0
    tag = runner.invoke(app, ["tag", str(sample_notebook_file), "--cell", "0"])
    assert tag.exit_code != 0
    ids = runner.invoke(app, ["ids", str(sample_notebook_file)])
    assert ids.exit_code != 0
    ops = runner.invoke(app, ["ops"])
    assert ops.exit_code == 0
    assert "stats" in ops.stdout
    assert "validate" in ops.stdout
    assert "outputs" in ops.stdout


def test_cli_error_paths(tmp_path: Path, sample_notebook_file: Path) -> None:
    inspect = runner.invoke(app, ["inspect", str(tmp_path / "missing.ipynb")])
    assert inspect.exit_code != 0

    bad = tmp_path / "bad.ipynb"
    bad.write_text("{not json", encoding="utf-8")
    headings = runner.invoke(app, ["headings", str(bad)])
    assert headings.exit_code != 0
    valid_bad = runner.invoke(app, ["validate", str(bad)])
    assert valid_bad.exit_code != 0

    warn_only = tmp_path / "warn.ipynb"
    warn_only.write_text(
        json.dumps(
            {
                "cells": [
                    {
                        "cell_type": "code",
                        "id": "c1",
                        "metadata": {},
                        "source": "x = 1\n",
                        "outputs": [],
                        "execution_count": 1,
                    }
                ],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 5,
            }
        ),
        encoding="utf-8",
    )
    strict = runner.invoke(app, ["lint", str(warn_only), "--strict"])
    assert strict.exit_code != 0

    kernel = runner.invoke(
        app, ["kernel", str(sample_notebook_file), "--name", "python3", "--no-in-place"]
    )
    assert kernel.exit_code != 0

    tag_bad = runner.invoke(
        app, ["tag", str(sample_notebook_file), "--cell", "99", "--add", "x", "--in-place"]
    )
    assert tag_bad.exit_code != 0

    batch_dir = tmp_path / "empty-batch"
    batch_dir.mkdir()
    (batch_dir / "bad.ipynb").write_text("{not json", encoding="utf-8")
    batch_lint = runner.invoke(app, ["batch", "lint", str(batch_dir)])
    assert batch_lint.exit_code != 0
    batch_clean = runner.invoke(app, ["batch", "clean", str(batch_dir)])
    assert batch_clean.exit_code != 0
    batch_stats = runner.invoke(app, ["batch", "stats", str(batch_dir)])
    assert batch_stats.exit_code != 0
    batch_validate = runner.invoke(app, ["batch", "validate", str(batch_dir)])
    assert batch_validate.exit_code != 0
