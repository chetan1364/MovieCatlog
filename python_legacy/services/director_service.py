"""
services/director_service.py
=============================
CRUD queries for the directors table.
Directors are the 1:N parent of movies (one director → many movies).
"""

from database.db import get_db


def _row_to_dict(row):
    return dict(row) if row else None

def _rows_to_list(rows):
    return [dict(r) for r in rows]


def get_all_directors():
    db = get_db()
    rows = db.execute(
        "SELECT id, name, bio, birth_year FROM directors ORDER BY name"
    ).fetchall()
    return _rows_to_list(rows)


def get_director_by_id(director_id):
    db = get_db()
    row = db.execute(
        "SELECT id, name, bio, birth_year FROM directors WHERE id = ?",
        (director_id,)
    ).fetchone()
    if not row:
        return None
    director = _row_to_dict(row)

    # Fetch all movies by this director (1:N child query)
    movies = db.execute(
        """
        SELECT m.id, m.title, m.release_year,
               ROUND(AVG(r.score), 1) AS avg_rating
        FROM   movies  m
        LEFT JOIN ratings r ON r.movie_id = m.id
        WHERE  m.director_id = ?
        GROUP BY m.id
        ORDER BY m.release_year DESC
        """,
        (director_id,)
    ).fetchall()
    director["movies"] = _rows_to_list(movies)
    return director


def create_director(data):
    db = get_db()
    with db:
        cursor = db.execute(
            "INSERT INTO directors (name, bio, birth_year) VALUES (:name, :bio, :birth_year)",
            data
        )
    return get_director_by_id(cursor.lastrowid)


def update_director(director_id, data):
    db = get_db()
    with db:
        db.execute(
            """
            UPDATE directors SET name = :name, bio = :bio, birth_year = :birth_year
            WHERE id = :id
            """,
            {**data, "id": director_id}
        )
    return get_director_by_id(director_id)


def delete_director(director_id):
    db = get_db()
    with db:
        result = db.execute("DELETE FROM directors WHERE id = ?", (director_id,))
    return result.rowcount > 0
