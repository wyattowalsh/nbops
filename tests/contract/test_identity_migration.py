"""TASK-105: canonical nbops identity vs historical provenance."""

from __future__ import annotations

import tomllib
from pathlib import Path

import nbops
from nbops import Observer, ObserverConfig, observe, start_observer

ROOT = Path(__file__).resolve().parents[2]


def test_pyproject_distribution_is_nbops() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["name"] == "nbops"
    assert data["project"]["scripts"]["nbops"] == "nbops.cli:app"


def test_import_and_cli_identity() -> None:
    assert nbops.observe is observe
    assert nbops.start_observer is start_observer
    assert nbops.Observer is Observer
    assert nbops.ObserverConfig is ObserverConfig
    assert Path(nbops.__file__).parent.name == "nbops"


def test_default_artifact_namespace_is_nbops() -> None:
    from nbops.config import default_artifact_root

    root = default_artifact_root()
    assert root.name == "nbops"
    assert "colab-observer" not in str(root)


def test_no_current_colab_observer_package() -> None:
    src = ROOT / "src"
    assert not (src / "colab_observer").exists()
    assert (src / "nbops").is_dir()


def test_identity_allowlist_matches_dump() -> None:
    import json

    allowlist = json.loads((ROOT / "IDENTITY_ALLOWLIST.json").read_text(encoding="utf-8"))
    assert allowlist["canonical_identity"] == "nbops"
    assert "build-colab-observer" in allowlist["stable_openspec_ids"]
    assert "generalize-notebook-runtime-observer" in allowlist["stable_openspec_ids"]
