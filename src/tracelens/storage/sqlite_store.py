"""SQLite persistence for TraceLens observations."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from tracelens.models import Observation


class SQLiteStore:
    """Small local evidence store with context-manager support."""

    def __init__(self, path: str | Path = "data/tracelens.sqlite3") -> None:
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.path)
        self._connection.row_factory = sqlite3.Row
        self._initialize()

    def __enter__(self) -> "SQLiteStore":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def _db(self) -> sqlite3.Connection:
        if self._connection is None:
            raise RuntimeError("This SQLiteStore is closed.")
        return self._connection

    def _initialize(self) -> None:
        db = self._db()
        db.execute(
            """CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                category TEXT NOT NULL,
                value TEXT NOT NULL,
                source TEXT NOT NULL,
                method TEXT NOT NULL,
                confidence TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                note TEXT NOT NULL DEFAULT ''
            )"""
        )
        db.execute("CREATE INDEX IF NOT EXISTS idx_observations_target ON observations(target)")
        db.commit()

    def add_many(self, observations: list[Observation]) -> int:
        if not observations:
            return 0
        db = self._db()
        db.executemany(
            """INSERT INTO observations
               (target, category, value, source, method, confidence, observed_at, note)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    item.target, item.category, item.value, item.source, item.method,
                    item.confidence, item.observed_at, item.note,
                )
                for item in observations
            ],
        )
        db.commit()
        return len(observations)

    def count(self, target: str | None = None) -> int:
        db = self._db()
        if target is None:
            row = db.execute("SELECT COUNT(*) AS n FROM observations").fetchone()
        else:
            row = db.execute(
                "SELECT COUNT(*) AS n FROM observations WHERE target = ?", (target,)
            ).fetchone()
        return int(row["n"])

    def list_observations(self, target: str | None = None) -> list[Observation]:
        db = self._db()
        if target is None:
            rows = db.execute(
                "SELECT * FROM observations ORDER BY observed_at DESC, id DESC"
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM observations WHERE target = ? ORDER BY observed_at DESC, id DESC",
                (target,),
            ).fetchall()
        return [
            Observation(
                target=row["target"],
                category=row["category"],
                value=row["value"],
                source=row["source"],
                method=row["method"],
                confidence=row["confidence"],
                observed_at=row["observed_at"],
                note=row["note"],
                id=row["id"],
            )
            for row in rows
        ]

    def history(self, domain: str) -> list[Observation]:
        """Backward-compatible alias for listing one target's observations."""
        return self.list_observations(domain)
