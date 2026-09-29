"""
services/rating_service.py
===========================
CRUD for the ratings table (1:N child of movies).
"""

from database.db import get_db


def _rows_to_list(rows):
    return [dict(r) for r in rows]


def get_ratings_for_movie(movie_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT id, user_name, score, review, created_at
        FROM   ratings
        WHERE  movie_id = ?
        ORDER  BY created_at DESC
        """,
        (movie_id,)
    ).fetchall()
    return _rows_to_list(rows)


def create_rating(data):
    """
    Insert a new rating (1:N child insert — movie_id is the FK).
    Validates score is 1-10 before inserting (schema also has a CHECK constraint).
    """
    if not (1 <= int(data.get("score", 0)) <= 10):
        raise ValueError("Score must be between 1 and 10")

    db = get_db()
    with db:
        cursor = db.execute(
            """
            INSERT INTO ratings (movie_id, user_name, score, review)
            VALUES (:movie_id, :user_name, :score, :review)
            """,
            data
        )
    row = db.execute(
        "SELECT id, movie_id, user_name, score, review, created_at FROM ratings WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()
    return dict(row) if row else None


def delete_rating(rating_id):
    db = get_db()
    with db:
        result = db.execute("DELETE FROM ratings WHERE id = ?", (rating_id,))
    return result.rowcount > 0
