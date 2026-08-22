"""Unit tests for notebook I/O."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from nbops.exceptions import InvalidNotebookError, NotebookNotFoundError
from nbops.io import (
    dumps_notebook,
    load_notebook,
    new_notebook,
    parse_notebook,
    save_notebook,
    validate_notebook,
)


def test_new_notebook_has_kernelspec() -> None:
    notebook = new_notebook()
    assert notebook["nbformat"] == 4
    assert notebook["cells"] == []
    assert notebook["metadata"]["kernelspec"]["name"] == "python3"


def test_parse_and_roundtrip(sample_notebook: dict[str, Any]) -> None:
    parsed = parse_notebook(sample_notebook, validate=False)
    dumped = dumps_notebook(parsed)
    again = parse_notebook(dumped, validate=False)
    assert again["nbformat"] == 4
    assert len(again["cells"]) == 4


def test_save_and_load_roundtrip(tmp_path: Path, sample_notebook: dict[str, Any]) -> None:
    path = tmp_path / "nested" / "demo.ipynb"
    save_notebook(sample_notebook, path, validate=False)
    loaded = load_notebook(path, validate=False)
    assert loaded["nbformat"] == 4
    assert len(loaded["cells"]) == 4


def test_load_notebook_missing(tmp_path: Path) -> None:
    with pytest.raises(NotebookNotFoundError):
        load_notebook(tmp_path / "nope.ipynb")


def test_load_notebook_invalid_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.ipynb"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(InvalidNotebookError):
        load_notebook(bad, validate=False)


def test_parse_invalid_document() -> None:
    with pytest.raises(InvalidNotebookError):
        parse_notebook("not-a-notebook", validate=False)


def test_validate_rejects_wrong_shape() -> None:
    with pytest.raises(InvalidNotebookError):
        parse_notebook({"cells": "nope", "nbformat": 4, "nbformat_minor": 5}, validate=True)


def test_validate_rejects_schema_error() -> None:
    with pytest.raises(InvalidNotebookError, match="schema validation"):
        validate_notebook({"nbformat": 4, "nbformat_minor": 5, "cells": [], "metadata": "bad"})


def test_load_notebook_validates_new_notebook(tmp_path: Path) -> None:
    path = tmp_path / "fresh.ipynb"
    save_notebook(new_notebook(), path, validate=True)
    loaded = load_notebook(path, validate=True)
    assert loaded["cells"] == []
    assert loaded["nbformat"] == 4
    validate_notebook(loaded)


def _noid_notebook() -> dict[str, Any]:
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "# Title\n",
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def test_parse_preserves_missing_cell_ids() -> None:
    parsed = parse_notebook(_noid_notebook(), validate=False)
    assert "id" not in parsed["cells"][0]


def test_save_and_load_preserve_missing_cell_ids(tmp_path: Path) -> None:
    path = tmp_path / "noid.ipynb"
    save_notebook(_noid_notebook(), path, validate=False)
    on_disk = path.read_text(encoding="utf-8")
    assert '"id"' not in on_disk
    loaded = load_notebook(path, validate=False)
    assert "id" not in loaded["cells"][0]
    validate_notebook(loaded)


def test_parse_bytes_and_reject_non_mapping() -> None:
    parsed = parse_notebook(b'{"cells": [], "nbformat": 4, "nbformat_minor": 5}', validate=False)
    assert parsed["cells"] == []
    with pytest.raises(InvalidNotebookError, match="mapping"):
        parse_notebook("[]", validate=False)
    with pytest.raises(InvalidNotebookError, match="notebook document"):
        parse_notebook(b"\xff\xfe", validate=False)


def test_load_notebook_rejects_non_mapping_json(tmp_path: Path) -> None:
    path = tmp_path / "list.ipynb"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(InvalidNotebookError, match="JSON notebook"):
        load_notebook(path, validate=False)


def test_load_notebook_invalid_encoding(tmp_path: Path) -> None:
    path = tmp_path / "binary.ipynb"
    path.write_bytes(b"\xff\xfe not utf-8")
    with pytest.raises(InvalidNotebookError, match="JSON notebook"):
        load_notebook(path, validate=False)


def test_load_notebook_unreadable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "blocked.ipynb"
    path.write_text("{}", encoding="utf-8")

    def boom(self: Path, *args: object, **kwargs: object) -> str:
        raise OSError("denied")

    monkeypatch.setattr(Path, "read_text", boom)
    with pytest.raises(InvalidNotebookError, match="JSON notebook"):
        load_notebook(path, validate=False)


def test_dumps_rejects_non_json_values() -> None:
    with pytest.raises(InvalidNotebookError, match="JSON-serializable"):
        dumps_notebook({"cells": [{"bad": object()}]})


def test_parse_upgrades_nbformat_v3() -> None:
    v3 = {
        "nbformat": 3,
        "nbformat_minor": 0,
        "metadata": {"name": "legacy"},
        "worksheets": [
            {
                "cells": [
                    {
                        "cell_type": "code",
                        "input": "x = 1\n",
                        "language": "python",
                        "outputs": [],
                        "collapsed": False,
                    }
                ]
            }
        ],
    }
    loaded = parse_notebook(v3, validate=False)
    assert loaded["nbformat"] == 4
    assert loaded["cells"][0]["cell_type"] == "code"
    assert "x = 1" in "".join(loaded["cells"][0]["source"])


def test_legacy_upgrade_rejects_non_mapping_result(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("nbops.io.nbformat.writes", lambda _node: "[]")
    with pytest.raises(InvalidNotebookError, match="mapping"):
        parse_notebook(
            {
                "nbformat": 3,
                "nbformat_minor": 0,
                "metadata": {"name": "legacy"},
                "worksheets": [
                    {
                        "cells": [
                            {
                                "cell_type": "code",
                                "input": "x = 1\n",
                                "language": "python",
                                "outputs": [],
                                "collapsed": False,
                            }
                        ]
                    }
                ],
            },
            validate=False,
        )


def test_legacy_upgrade_wraps_convert_errors() -> None:
    with pytest.raises(InvalidNotebookError, match="notebook document"):
        parse_notebook({"nbformat": 3, "nbformat_minor": 0, "worksheets": "nope"}, validate=False)


def test_validate_accepts_nbformat_node() -> None:
    import nbformat

    node = nbformat.v4.new_notebook()
    node["metadata"] = new_notebook()["metadata"]
    validate_notebook(node)
