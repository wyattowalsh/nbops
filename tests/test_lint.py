"""Unit tests for notebook linting."""

from __future__ import annotations

from typing import Any

from nbops.lint import lint_notebook


def test_lint_clean_sample_has_unexecuted_info(sample_notebook: dict[str, Any]) -> None:
    report = lint_notebook(sample_notebook)
    codes = {issue.code for issue in report.issues}
    assert "NB005" in codes
    assert report.passed is True


def test_lint_detects_errors_and_missing_title(error_notebook: dict[str, Any]) -> None:
    report = lint_notebook(error_notebook)
    codes = {issue.code for issue in report.issues}
    assert "NB004" in codes
    assert "NB002" in codes
    assert "NB008" in codes
    assert report.passed is False
    assert report.error_count >= 1


def test_lint_syntax_duplicate_id_and_empty() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "dup",
                "metadata": {},
                "source": "# Title\n",
            },
            {
                "cell_type": "code",
                "id": "dup",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "def (\n",
            },
            {
                "cell_type": "code",
                "id": "empty",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "",
            },
        ],
        "metadata": {"kernelspec": {"name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    report = lint_notebook(notebook)
    codes = {issue.code for issue in report.issues}
    assert "NB007" in codes
    assert "NB010" in codes
    assert "NB003" in codes
    assert "NB001" not in codes


def test_lint_empty_notebook() -> None:
    report = lint_notebook({"cells": []})
    assert any(issue.code == "NB001" for issue in report.issues)
    assert report.passed is False


def test_lint_title_accepts_setext_and_ignores_fenced_hashes() -> None:
    titled = {
        "cells": [
            {"cell_type": "markdown", "id": "title", "metadata": {}, "source": "Demo\n====\n"},
            {
                "cell_type": "code",
                "id": "ok",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": "x = 1\n",
            },
        ],
        "metadata": {"kernelspec": {"name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    assert "NB002" not in {issue.code for issue in lint_notebook(titled).issues}

    fenced = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "fenced",
                "metadata": {},
                "source": "```\n# Title\n```\n",
            }
        ],
        "metadata": {"kernelspec": {"name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    assert "NB002" in {issue.code for issue in lint_notebook(fenced).issues}


def test_lint_skips_writefile_cell_magic() -> None:
    notebook = {
        "cells": [
            {"cell_type": "markdown", "id": "title", "metadata": {}, "source": "# Title\n"},
            {
                "cell_type": "code",
                "id": "write",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": "%%writefile notes.txt\nhello world\n",
            },
        ],
        "metadata": {"kernelspec": {"name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    assert "NB007" not in {issue.code for issue in lint_notebook(notebook).issues}


def test_lint_output_size_and_non_mapping_outputs() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "title",
                "metadata": {},
                "source": "# Title\n",
            },
            {
                "cell_type": "code",
                "id": "sized",
                "execution_count": 1,
                "metadata": {},
                "source": "print(1)\n",
                "outputs": [
                    "skip",
                    {"output_type": "stream", "name": "stdout", "text": "x" * 20},
                    {"output_type": "error"},
                    {"output_type": "display_data", "metadata": {}},
                ],
            },
        ],
        "metadata": {"kernelspec": {"name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    report = lint_notebook(notebook, max_output_chars=10)
    codes = {issue.code for issue in report.issues}
    assert "NB006" in codes
    assert "NB004" in codes
    nameless = [issue for issue in report.issues if issue.code == "NB004"]
    assert nameless[0].message.endswith("(error).")


def test_lint_accepts_ipython_magics_and_toplevel_await() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "title",
                "metadata": {},
                "source": "# Title\n",
            },
            {
                "cell_type": "code",
                "id": "magics",
                "execution_count": 1,
                "metadata": {},
                "outputs": [{"output_type": "stream", "name": "stdout", "text": "ok\n"}],
                "source": "%matplotlib inline\nimport os\nawait fetch()\n",
            },
            {
                "cell_type": "code",
                "id": "bash",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": "%%bash\necho hi\n",
            },
        ],
        "metadata": {"kernelspec": {"name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    report = lint_notebook(notebook)
    codes = {issue.code for issue in report.issues}
    assert "NB007" not in codes
    assert report.passed is True


def test_lint_skips_python_syntax_for_non_python_kernels() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "id": "title",
                "metadata": {},
                "source": "# Title\n",
            },
            {
                "cell_type": "code",
                "id": "r-code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": "library(ggplot2)\n",
            },
        ],
        "metadata": {
            "kernelspec": {"name": "ir", "display_name": "R", "language": "r"},
            "language_info": {"name": "r"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    report = lint_notebook(notebook)
    assert "NB007" not in {issue.code for issue in report.issues}
    assert report.passed is True


def test_lint_infers_r_from_kernelspec_name_without_language() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "id": "r-code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": "library(ggplot2)\n",
            }
        ],
        "metadata": {"kernelspec": {"name": "ir", "display_name": "R"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    report = lint_notebook(notebook)
    assert "NB007" not in {issue.code for issue in report.issues}
