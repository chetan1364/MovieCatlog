"""
services/actor_service.py
==========================
CRUD for actors table. Actors relate to movies via movie_actors (M:N).
"""

from database.db import get_db


def _row_to_dict(row):
    return dict(row) if row else None

def _rows_to_list(rows):
    return [dict(r) for r in rows]


def get_all_actors():
    db = get_db()
    rows = db.execute(
        "SELECT id, name, bio FROM actors ORDER BY name"
    ).fetchall()
    return _rows_to_list(rows)


def get_actor_by_id(actor_id):
    db = get_db()
    row = db.execute(
        "SELECT id, name, bio FROM actors WHERE id = ?", (actor_id,)
    ).fetchone()
    if not row:
        return None
    actor = _row_to_dict(row)

    # Fetch filmography: movies this actor appeared in (M:N via movie_actors)
    movies = db.execute(
        """
        SELECT m.id, m.title, m.release_year, ma.character_name
        FROM   movies      m
        JOIN   movie_actors ma ON ma.movie_id = m.id
        WHERE  ma.actor_id = ?
        ORDER BY m.release_year DESC
        """,
        (actor_id,)
    ).fetchall()
    actor["filmography"] = _rows_to_list(movies)
    return actor


def create_actor(data):
    db = get_db()
    with db:
        cursor = db.execute(
            "INSERT INTO actors (name, bio) VALUES (:name, :bio)", data
        )
    return get_actor_by_id(cursor.lastrowid)


def update_actor(actor_id, data):
    db = get_db()
    with db:
        db.execute(
            "UPDATE actors SET name = :name, bio = :bio WHERE id = :id",
            {**data, "id": actor_id}
        )
    return get_actor_by_id(actor_id)


def delete_actor(actor_id):
    db = get_db()
    with db:
        result = db.execute("DELETE FROM actors WHERE id = ?", (actor_id,))
    return result.rowcount > 0
