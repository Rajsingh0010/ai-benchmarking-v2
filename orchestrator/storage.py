import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class RunStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY, app_id TEXT NOT NULL, app_type TEXT NOT NULL,
                dataset_version TEXT NOT NULL, git_commit TEXT NOT NULL, created_at TEXT NOT NULL,
                result_json TEXT NOT NULL)"""
            )
            db.commit()

    def save(self, run: dict[str, Any]) -> None:
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?)",
                (run["run_id"], run["app_id"], run["app_type"], run["dataset_version"],
                 run["git_commit"], run["created_at"], json.dumps(run)))
            db.commit()

    def get(self, run_id: str) -> dict[str, Any] | None:
        with sqlite3.connect(self.path) as db:
            row = db.execute("SELECT result_json FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def list(self, limit: int = 50) -> list[dict[str, Any]]:
        with sqlite3.connect(self.path) as db:
            rows = db.execute("SELECT result_json FROM runs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [json.loads(row[0]) for row in rows]

    def list_filtered(self, app_id: str | None = None, app_type: str | None = None,
                      limit: int = 50) -> list[dict[str, Any]]:
        query = "SELECT result_json FROM runs WHERE 1=1"
        values: list[Any] = []
        if app_id:
            query += " AND app_id = ?"
            values.append(app_id)
        if app_type:
            query += " AND app_type = ?"
            values.append(app_type)
        query += " ORDER BY created_at DESC LIMIT ?"
        values.append(limit)
        with sqlite3.connect(self.path) as db:
            rows = db.execute(query, values).fetchall()
        return [json.loads(row[0]) for row in rows]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
