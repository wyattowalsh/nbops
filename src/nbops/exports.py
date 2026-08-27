"""Local reports and portable evidence bundles. Never upload."""

from __future__ import annotations

import json
import zipfile
from typing import TYPE_CHECKING, Any, Literal

from nbops.observations import RunState

if TYPE_CHECKING:
    from pathlib import Path

    from nbops.observations import ObserverStatus

ReportFormat = Literal["html", "markdown"]


def export_report(
    *,
    output_dir: Path,
    status: ObserverStatus,
    observations: list[dict[str, Any]],
    report_format: ReportFormat,
    profile: dict[str, Any] | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    if report_format == "html":
        path = output_dir / "report.html"
        path.write_text(_html_report(status, observations, profile), encoding="utf-8")
        return path
    path = output_dir / "report.md"
    path.write_text(_markdown_report(status, observations, profile), encoding="utf-8")
    return path


def export_bundle(
    *,
    output_dir: Path,
    status: ObserverStatus,
    sqlite_path: Path | None,
    reports: list[Path],
    profile: dict[str, Any] | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    bundle = output_dir / "nbops-bundle.zip"
    manifest = {
        "product": "nbops",
        "schema": "urn:nbops:bundle:v1",
        "run_id": status.run_id,
        "project": status.project,
        "state": status.state.value if isinstance(status.state, RunState) else str(status.state),
        "profile": profile or {},
    }
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
        if sqlite_path is not None and sqlite_path.is_file():
            archive.write(sqlite_path, arcname="observations.sqlite")
        for report in reports:
            if report.is_file():
                archive.write(report, arcname=report.name)
    return bundle


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def _markdown_report(
    status: ObserverStatus, observations: list[dict[str, Any]], profile: dict[str, Any] | None
) -> str:
    lines = [
        f"# nbops report: {status.project}",
        "",
        f"- run_id: `{status.run_id}`",
        f"- state: `{status.state}`",
        f"- running: `{status.is_running}`",
        "",
        "## Capabilities",
        "",
    ]
    for capability in status.capabilities:
        reason = f" — {capability.reason}" if capability.reason else ""
        lines.append(f"- `{capability.name}`: {capability.state.value}{reason}")
    lines.extend(
        ["", "## Observations", "", "| metric | value | quality | unit |", "|---|---|---|---|"]
    )
    for item in observations:
        value = item.get("value_number")
        if value is None:
            value = item.get("value_text") or "unavailable"
        lines.append(
            f"| {item.get('metric')} | {value} | {item.get('quality')} | {item.get('unit') or ''} |"
        )
    if profile:
        lines.extend(
            ["", "## Runtime profile", "", "```json", json.dumps(profile, indent=2), "```"]
        )
    lines.append("")
    return "\n".join(lines)


def _html_report(
    status: ObserverStatus, observations: list[dict[str, Any]], profile: dict[str, Any] | None
) -> str:
    rows = []
    for item in observations:
        value = item.get("value_number")
        if value is None:
            value = item.get("value_text") or "unavailable"
        rows.append(
            "<tr>"
            f"<td>{_escape(str(item.get('metric')))}</td>"
            f"<td>{_escape(str(value))}</td>"
            f"<td>{_escape(str(item.get('quality')))}</td>"
            f"<td>{_escape(str(item.get('unit') or ''))}</td>"
            "</tr>"
        )
    capabilities = "".join(
        f"<li><code>{_escape(item.name)}</code>: {_escape(item.state.value)}"
        f"{' — ' + _escape(item.reason) if item.reason else ''}</li>"
        for item in status.capabilities
    )
    profile_html = ""
    if profile:
        profile_html = f"<pre>{_escape(json.dumps(profile, indent=2))}</pre>"
    return (
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
        "<title>nbops report</title></head><body>"
        f"<h1>nbops report: {_escape(status.project)}</h1>"
        f"<p>run_id: {_escape(str(status.run_id))} state: {_escape(str(status.state))}</p>"
        f"<h2>Capabilities</h2><ul>{capabilities}</ul>"
        "<h2>Observations</h2><table><thead><tr><th>metric</th><th>value</th>"
        "<th>quality</th><th>unit</th></tr></thead><tbody>"
        f"{''.join(rows)}</tbody></table>{profile_html}</body></html>\n"
    )
