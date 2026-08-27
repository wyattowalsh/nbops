"""SQLite and in-memory observation stores."""

from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING, Any

from nbops.observations import ObservationQuality

if TYPE_CHECKING:
    from pathlib import Path

    from nbops.observations import Observation


_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    project TEXT NOT NULL,
    product TEXT NOT NULL,
    started_at TEXT NOT NULL,
    state TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS observations (
    run_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    observed_at_utc TEXT NOT NULL,
    monotonic_ns INTEGER NOT NULL,
    metric TEXT NOT NULL,
    value_number REAL,
    value_text TEXT,
    unit TEXT,
    source TEXT NOT NULL,
    quality TEXT NOT NULL,
    PRIMARY KEY (run_id, sequence, metric)
);
"""


class SqliteStore:
    """One-writer SQLite store for run metadata and observations."""

    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(path), check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def create_run(self, run_id: str, project: str, started_at: str, state: str) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO runs"
            "(run_id, project, product, started_at, state) VALUES (?,?,?,?,?)",
            (run_id, project, "nbops", started_at, state),
        )
        self._conn.commit()

    def set_state(self, run_id: str, state: str) -> None:
        self._conn.execute("UPDATE runs SET state=? WHERE run_id=?", (state, run_id))
        self._conn.commit()

    def append(self, observation: Observation) -> None:
        self._conn.execute(
            """INSERT OR REPLACE INTO observations (
                   run_id, sequence, observed_at_utc, monotonic_ns, metric,
                   value_number, value_text, unit, source, quality
               ) VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                observation.run_id,
                observation.sequence,
                observation.observed_at_utc.isoformat(),
                observation.monotonic_ns,
                observation.metric,
                observation.value_number,
                observation.value_text,
                observation.unit,
                observation.source,
                observation.quality.value,
            ),
        )
        self._conn.commit()

    def list_observations(self, run_id: str) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            "SELECT metric, value_number, value_text, quality, unit, source, "
            "sequence FROM observations WHERE run_id=? ORDER BY sequence",
            (run_id,),
        ).fetchall()
        return [
            {
                "metric": metric,
                "value_number": value_number,
                "value_text": value_text,
                "quality": quality,
                "unit": unit,
                "source": source,
                "sequence": sequence,
            }
            for metric, value_number, value_text, quality, unit, source, sequence in rows
        ]

    def close(self) -> None:
        self._conn.close()


def quality_never_zero(observation: Observation) -> bool:
    """Unavailable observations must not carry a numeric zero stand-in."""
    if observation.quality is ObservationQuality.UNAVAILABLE:
        return observation.value_number is None and observation.value_text is None
    return True
