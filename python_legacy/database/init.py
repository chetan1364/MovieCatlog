"""
database/init.py
================
Database initialiser — run this once before starting the server.

Steps:
  1. Reads schema.sql and executes all CREATE TABLE statements
  2. Runs seed.py to populate realistic data

Usage:
  python database/init.py
  (or)  npm run init-db  (see package.json scripts)
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add project root to sys.path so relative imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Load .env before importing db module
from dotenv import load_dotenv
load_dotenv()

from database.db import get_db, DB_PATH
from database.seed import seed_database


def init_schema():
    """Execute schema.sql to create all tables."""
    schema_path = Path(__file__).parent / "schema.sql"
    sql = schema_path.read_text(encoding="utf-8")

    db = get_db()
    # executescript runs multiple semicolon-separated statements
    db.executescript(sql)
    db.commit()
    print(f"  [OK] Schema applied  -> {DB_PATH}")


if __name__ == "__main__":
    print("\nInitialising Movie Catalog database...\n")
    print(f"  Database path: {DB_PATH}")

    init_schema()
    seed_database()

    # ── Verification: count rows in each table ────────────────────────────────
    db = get_db()
    tables = ["directors", "movies", "actors", "genres",
              "movie_actors", "movie_genres", "ratings"]
    print("\n  Row counts after seed:")
    for t in tables:
        count = db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"    {t:20s}  →  {count} rows")

    print("\n[DONE] Database ready. Run:  python server.py\n")
