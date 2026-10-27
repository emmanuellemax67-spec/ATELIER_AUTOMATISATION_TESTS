import json
import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(**file**).resolve().parent
DB_PATH = os.environ.get(
"DATABASE_PATH",
str(BASE_DIR / "runs.db")
)

def get_connection():
"""Ouvre une connexion SQLite."""
connection = sqlite3.connect(DB_PATH, timeout=10)
connection.row_factory = sqlite3.Row
return connection

def init_db():
"""Crée la table des exécutions si elle n'existe pas."""
with get_connection() as connection:
connection.execute("""
CREATE TABLE IF NOT EXISTS runs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
timestamp TEXT NOT NULL,
api TEXT NOT NULL,
total INTEGER NOT NULL,
passed INTEGER NOT NULL,
failed INTEGER NOT NULL,
errors INTEGER NOT NULL,
error_rate REAL NOT NULL,
latency_avg REAL NOT NULL,
latency_p95 REAL NOT NULL,
results_json TEXT NOT NULL
)
""")

def save_run(run):
"""Enregistre une exécution et renvoie son identifiant."""
summary = run["summary"]

```
with get_connection() as connection:
    cursor = connection.execute("""
        INSERT INTO runs (
            timestamp, api, total, passed, failed, errors,
            error_rate, latency_avg, latency_p95, results_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run["timestamp"],
        run["api"],
        summary["total"],
        summary["passed"],
        summary["failed"],
        summary["errors"],
        summary["error_rate"],
        summary["latency_ms_avg"],
        summary["latency_ms_p95"],
        json.dumps(run["tests"], ensure_ascii=False),
    ))

    return cursor.lastrowid
```

def list_runs(limit=20):
"""Renvoie les dernières exécutions."""
limit = max(1, min(int(limit), 100))

```
with get_connection() as connection:
    rows = connection.execute("""
        SELECT *
        FROM runs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    return [dict(row) for row in rows]
```

def get_latest_run():
"""Renvoie la dernière exécution ou None."""
runs = list_runs(limit=1)
return runs[0] if runs else None
