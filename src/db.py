"""SQLite database with sample daily production data (fictional)."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "reports.db"


def get_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY,
            field_id TEXT,
            field_name TEXT,
            report_date TEXT,
            oil_bbl INTEGER,
            water_cut REAL
        );
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT
        );
        """
    )
    if db.execute("SELECT COUNT(*) FROM reports").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO reports (field_id, field_name, report_date, oil_bbl, water_cut) VALUES (?, ?, ?, ?, ?)",
            [
                ("F-101", "Demo Field A", "2026-11-01", 125000, 0.18),
                ("F-101", "Demo Field A", "2026-11-02", 124300, 0.19),
                ("F-202", "Demo Field B", "2026-11-01", 87000, 0.27),
                ("F-303", "Demo Field C", "2026-11-01", 43500, 0.35),
            ],
        )
    db.commit()
    db.close()
