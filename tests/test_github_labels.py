"""Repo-hygiene checks for GitHub label names referenced by automation."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABEL_CATALOG = ROOT / ".github" / "labels.yml"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"
RELEASE = ROOT / ".github" / "release.yml"

REFERENCED_LABELS = (
    "bug",
    "enhancement",
    "documentation",
    "dependencies",
    "python",
    "github-actions",
    "ci",
    "skip-changelog",
)


def test_label_catalog_covers_dependabot_and_release_names() -> None:
    catalog = LABEL_CATALOG.read_text(encoding="utf-8")
    for name in REFERENCED_LABELS:
        assert f'name: "{name}"' in catalog
    dependabot = DEPENDABOT.read_text(encoding="utf-8")
    release = RELEASE.read_text(encoding="utf-8")
    assert '"dependencies"' in dependabot
    assert '"python"' in dependabot
    assert '"github-actions"' in dependabot
    assert 'package-ecosystem: "uv"' in dependabot
    assert 'package-ecosystem: "pip"' not in dependabot
    assert "skip-changelog" in release
    assert "github-actions" in release
    assert "- ci\n" in release
