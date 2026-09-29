"""
database/db.py
==============
SQLite connection singleton using Python's built-in sqlite3 module.

Key behaviour:
  - PRAGMA foreign_keys = ON  →  enforces all FK constraints at runtime
  - Row factory set to sqlite3.Row  →  rows are accessible as dict-like objects
  - A single connection is reused across all requests (thread-safe via check_same_thread=False)
"""

import sqlite3
import os
from pathlib import Path

# ── Resolve the database file path from the environment variable ──────────────
# DATABASE_URL can be relative (./database/movie_catalog.db) or absolute.
_BASE_DIR = Path(__file__).resolve().parent.parent
_DB_URL   = os.getenv("DATABASE_URL", "./database/movie_catalog.db")
DB_PATH   = _BASE_DIR / _DB_URL if not os.path.isabs(_DB_URL) else Path(_DB_URL)

# Ensure the database directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# ── Singleton connection ───────────────────────────────────────────────────────
_connection: sqlite3.Connection | None = None


def get_db() -> sqlite3.Connection:
    """
    Return the shared SQLite connection.
    Creates the connection on first call and stores it as a module-level singleton.
    """
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        # Make rows accessible by column name (e.g. row["title"])
        _connection.row_factory = sqlite3.Row
        # CRITICAL: SQLite does NOT enforce foreign keys by default.
        # This pragma turns FK enforcement ON for every statement.
        _connection.execute("PRAGMA foreign_keys = ON")
        _connection.commit()
    return _connection


def close_db():
    """Close the singleton connection (called on app shutdown)."""
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None
