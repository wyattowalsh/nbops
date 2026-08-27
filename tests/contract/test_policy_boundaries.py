"""TASK-103/security: no keepalive, telemetry, or public backend by default."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "src" / "nbops"

_FORBIDDEN_CALL_SHAPES = (
    "keepalive",
    "anti-idle",
    "anti_idle",
    "keep_alive",
    "timeout_bypass",
    "quota_circumvention",
    "reconnect_forever",
)


def test_observer_modules_do_not_ship_runtime_extension() -> None:
    hits: list[str] = []
    for path in ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in _FORBIDDEN_CALL_SHAPES:
            # Comments that name the boundary are allowed; call shapes are not.
            if (
                needle in text
                and "explain" not in text.lower()
                and "prohibited" not in text.lower()
                and (f"def {needle}" in text or f"{needle}(" in text)
            ):
                hits.append(f"{path.name}:{needle}")
    assert hits == []


def test_default_display_has_no_public_endpoint(tmp_path: Path) -> None:
    from nbops import ObserverConfig, observe

    observer = observe(
        ObserverConfig(project="sec", output_dir=tmp_path, persist=False, interval_s=0.05)
    )
    try:
        result = observer.display()
        assert result.public_url is None
        assert "http://" not in result.text
        assert "https://" not in result.text
    finally:
        observer.stop()
        observer.close()


def test_notebook_snippet_has_three_cells_and_nbops_identity() -> None:
    import json

    notebook = json.loads(
        (Path(__file__).resolve().parents[2] / "notebooks" / "nbops-quickstart.ipynb").read_text(
            encoding="utf-8"
        )
    )
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    assert len(code_cells) == 3
    source = "".join("".join(cell["source"]) for cell in notebook["cells"])
    assert "from nbops import" in source
    assert "colab_observer" not in source
    assert "observe(" in source
    assert "observer.display()" in source
    assert "export_bundle" in source
    assert "keepalive" not in source
    assert "google.colab.drive.mount" not in source
