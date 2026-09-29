"""
services/genre_service.py
==========================
CRUD for genres table. Genres relate to movies via movie_genres (M:N).
"""

from database.db import get_db


def _rows_to_list(rows):
    return [dict(r) for r in rows]


def get_all_genres():
    db = get_db()
    rows = db.execute("SELECT id, name FROM genres ORDER BY name").fetchall()
    return _rows_to_list(rows)


def create_genre(data):
    db = get_db()
    with db:
        cursor = db.execute(
            "INSERT OR IGNORE INTO genres (name) VALUES (:name)", data
        )
    row = db.execute("SELECT id, name FROM genres WHERE name = ?", (data["name"],)).fetchone()
    return dict(row) if row else None


def delete_genre(genre_id):
    db = get_db()
    with db:
        result = db.execute("DELETE FROM genres WHERE id = ?", (genre_id,))
    return result.rowcount > 0
