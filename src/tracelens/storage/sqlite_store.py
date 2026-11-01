"""SQLite persistence for observations."""
import sqlite3
from pathlib import Path
from tracelens.models import Observation

class SQLiteStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _initialize(self):
        with self._connect() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL, record_type TEXT NOT NULL, value TEXT NOT NULL,
                observed_at TEXT NOT NULL, source TEXT NOT NULL, method TEXT NOT NULL,
                confidence TEXT NOT NULL, note TEXT NOT NULL)""")
            con.execute("CREATE INDEX IF NOT EXISTS idx_observations_domain ON observations(domain)")

    def add_many(self, observations: list[Observation]) -> int:
        if not observations:
            return 0
        with self._connect() as con:
            con.executemany("""INSERT INTO observations
                (domain, record_type, value, observed_at, source, method, confidence, note)
                VALUES (:domain, :record_type, :value, :observed_at, :source, :method, :confidence, :note)""",
                [item.to_dict() for item in observations])
        return len(observations)

    def history(self, domain: str) -> list[Observation]:
        with self._connect() as con:
            rows = con.execute("""SELECT domain, record_type, value, observed_at, source, method, confidence, note
                FROM observations WHERE domain=? ORDER BY observed_at DESC, id DESC""", (domain,)).fetchall()
        return [Observation(*row) for row in rows]
