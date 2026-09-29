"""
services/movie_service.py
==========================
Business logic layer for movies.

All SQL is written as raw strings so the JOINs, foreign key traversal,
and aggregation are fully visible and readable for learning purposes.

Key patterns demonstrated:
  1. 1:N JOIN  — movies → directors (director_id FK)
  2. M:N JOIN  — movies ↔ actors via movie_actors junction
  3. M:N JOIN  — movies ↔ genres  via movie_genres  junction
  4. SQL Aggregation — AVG(r.score), COUNT(r.id) with GROUP BY
  5. Transactions   — atomically create movie + genres + actors
  6. Dynamic WHERE  — search / filter / sort without SQL injection
"""

from database.db import get_db


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER: convert sqlite3.Row objects to plain dicts
# ══════════════════════════════════════════════════════════════════════════════
def _row_to_dict(row):
    return dict(row) if row else None

def _rows_to_list(rows):
    return [dict(r) for r in rows]


# ══════════════════════════════════════════════════════════════════════════════
#  GET ALL MOVIES  (with search, filter, sort)
# ══════════════════════════════════════════════════════════════════════════════
def get_all_movies(search=None, genre=None, year_from=None, year_to=None,
                   sort_by="title", sort_order="ASC"):
    """
    Returns a list of movies with director name, genre list,
    average rating, and rating count.

    Uses LEFT JOINs so movies with no ratings still appear (AVG returns NULL).

    SQL pattern (search + filter + sort):
      ─ The WHERE clause is built dynamically from query parameters.
      ─ LIKE '%?%' is used for keyword search across title, director, actor name.
      ─ Parameters are passed as a tuple to prevent SQL injection.
    """
    db = get_db()

    # ── Build dynamic WHERE clause ─────────────────────────────────────────────
    conditions = []
    params = []

    if search:
        # Search across movie title, director name, and actor name
        # This requires joining actors which may produce duplicate movie rows,
        # so we wrap in GROUP BY m.id to deduplicate.
        keyword = f"%{search}%"
        conditions.append(
            "(m.title LIKE ? OR d.name LIKE ? OR a.name LIKE ?)"
        )
        params.extend([keyword, keyword, keyword])

    if genre:
        conditions.append("g.name = ?")
        params.append(genre)

    if year_from:
        conditions.append("m.release_year >= ?")
        params.append(int(year_from))

    if year_to:
        conditions.append("m.release_year <= ?")
        params.append(int(year_to))

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    # ── Validate sort_by to prevent SQL injection in ORDER BY ──────────────────
    allowed_sort = {
        "title":      "m.title",
        "release_year": "m.release_year",
        "avg_rating": "avg_rating",
    }
    order_col  = allowed_sort.get(sort_by, "m.title")
    order_dir  = "DESC" if sort_order.upper() == "DESC" else "ASC"

    # ── Main query: 1:N join (director), M:N joins (actor, genre), aggregation ─
    query = f"""
        SELECT
            m.id,
            m.title,
            m.release_year,
            m.duration_minutes,
            m.poster_url,
            m.synopsis,

            -- 1:N JOIN: director details via director_id FK
            d.name AS director_name,

            -- Aggregation: AVG and COUNT over ratings (1:N child of movie)
            ROUND(AVG(r.score), 1)  AS avg_rating,
            COUNT(DISTINCT r.id)    AS rating_count

        FROM movies m

        -- 1:N join: director (LEFT so movies without director still show)
        LEFT JOIN directors   d  ON d.id       = m.director_id

        -- M:N joins via junction tables (needed for search/filter only)
        LEFT JOIN movie_genres mg ON mg.movie_id = m.id
        LEFT JOIN genres       g  ON g.id        = mg.genre_id
        LEFT JOIN movie_actors ma ON ma.movie_id = m.id
        LEFT JOIN actors       a  ON a.id        = ma.actor_id

        -- 1:N join: ratings for aggregation
        LEFT JOIN ratings      r  ON r.movie_id  = m.id

        {where_clause}

        -- GROUP BY prevents duplicate rows from the M:N joins
        GROUP BY m.id

        ORDER BY {order_col} {order_dir}
    """

    rows = db.execute(query, params).fetchall()
    movies = _rows_to_list(rows)

    # ── Attach genre tags to each movie (separate query — cleaner than GROUP_CONCAT) ──
    for movie in movies:
        movie["genres"] = _get_movie_genres(movie["id"])

    return movies


# ══════════════════════════════════════════════════════════════════════════════
#  GET SINGLE MOVIE (full detail with director, cast, genres, avg rating)
# ══════════════════════════════════════════════════════════════════════════════
def get_movie_by_id(movie_id):
    """
    Returns full movie detail including:
      - Director info (1:N join via director_id FK)
      - Cast list with character names (M:N join via movie_actors)
      - Genre tags (M:N join via movie_genres)
      - Average rating + review count (SQL aggregation: AVG, COUNT)
    """
    db = get_db()

    # ── Query 1: Movie + Director (1:N) + Aggregated Rating ───────────────────
    movie = db.execute(
        """
        SELECT
            m.id,
            m.title,
            m.release_year,
            m.duration_minutes,
            m.synopsis,
            m.poster_url,

            -- 1:N FK join: director info embedded in movie row
            d.id         AS director_id,
            d.name       AS director_name,
            d.bio        AS director_bio,
            d.birth_year AS director_birth_year,

            -- Aggregation: AVG(score) and COUNT(*) from ratings table
            -- GROUP BY ensures one row per movie
            ROUND(AVG(r.score), 1)  AS avg_rating,
            COUNT(r.id)             AS rating_count

        FROM   movies    m
        LEFT JOIN directors d ON d.id      = m.director_id   -- 1:N join
        LEFT JOIN ratings   r ON r.movie_id = m.id           -- 1:N for aggregation
        WHERE  m.id = ?
        GROUP BY m.id
        """,
        (movie_id,)
    ).fetchone()

    if not movie:
        return None

    result = _row_to_dict(movie)

    # ── Query 2: Cast list (M:N via movie_actors junction) ────────────────────
    # movie_actors joins actors to movies with an extra column: character_name
    result["cast"] = _get_movie_cast(movie_id)

    # ── Query 3: Genre tags (M:N via movie_genres junction) ───────────────────
    result["genres"] = _get_movie_genres(movie_id)

    # ── Query 4: Individual reviews (1:N child) ───────────────────────────────
    result["ratings"] = _get_movie_ratings(movie_id)

    return result


# ══════════════════════════════════════════════════════════════════════════════
#  PRIVATE HELPERS — Fetch related data for a movie
# ══════════════════════════════════════════════════════════════════════════════

def _get_movie_cast(movie_id):
    """
    Fetch actors for a movie via the movie_actors junction table.

    M:N Pattern:
      actors ──(movie_actors)──▶ movies
      The junction table adds: character_name (role-specific attribute)
    """
    db = get_db()
    rows = db.execute(
        """
        SELECT
            a.id,
            a.name,
            a.bio,
            ma.character_name          -- role-specific attribute from junction
        FROM   actors      a
        JOIN   movie_actors ma
            ON ma.actor_id  = a.id     -- join through junction table
        WHERE  ma.movie_id = ?         -- filter to this movie
        ORDER BY a.name
        """,
        (movie_id,)
    ).fetchall()
    return _rows_to_list(rows)


def _get_movie_genres(movie_id):
    """
    Fetch genres for a movie via the movie_genres junction table.

    M:N Pattern:
      genres ──(movie_genres)──▶ movies
    """
    db = get_db()
    rows = db.execute(
        """
        SELECT
            g.id,
            g.name
        FROM   genres      g
        JOIN   movie_genres mg
            ON mg.genre_id = g.id      -- join through junction table
        WHERE  mg.movie_id = ?         -- filter to this movie
        ORDER BY g.name
        """,
        (movie_id,)
    ).fetchall()
    return _rows_to_list(rows)


def _get_movie_ratings(movie_id):
    """Fetch all ratings/reviews for a movie (1:N child of movies)."""
    db = get_db()
    rows = db.execute(
        """
        SELECT id, user_name, score, review, created_at
        FROM   ratings
        WHERE  movie_id = ?
        ORDER BY created_at DESC
        """,
        (movie_id,)
    ).fetchall()
    return _rows_to_list(rows)


# ══════════════════════════════════════════════════════════════════════════════
#  CREATE MOVIE  (transactional — movie + genres + actors atomically)
# ══════════════════════════════════════════════════════════════════════════════
def create_movie(data):
    """
    Create a movie along with its genre associations and cast in a single
    database transaction.

    TRANSACTION PATTERN:
      All three steps (insert movie, insert genre rows, insert actor rows)
      are wrapped in a BEGIN/COMMIT block via Python's context manager.
      If any step raises an exception, the entire transaction is rolled back,
      ensuring the database is never left in a partial state.

    Expected data dict:
      {
        "title": str,
        "release_year": int,
        "duration_minutes": int,
        "synopsis": str,
        "poster_url": str,
        "director_id": int,
        "genre_ids": [int, ...],        # IDs from genres table
        "actors": [                     # cast list
          {"actor_id": int, "character_name": str},
          ...
        ]
      }
    """
    db = get_db()

    # Python's sqlite3 connection is a context manager:
    # __enter__ calls BEGIN, __exit__ calls COMMIT on success or ROLLBACK on error
    with db:
        # ── Step 1: Insert the movie row ──────────────────────────────────────
        cursor = db.execute(
            """
            INSERT INTO movies (title, release_year, duration_minutes, synopsis, poster_url, director_id)
            VALUES (:title, :release_year, :duration_minutes, :synopsis, :poster_url, :director_id)
            """,
            data
        )
        movie_id = cursor.lastrowid

        # ── Step 2: Insert genre associations (M:N via movie_genres) ──────────
        for genre_id in data.get("genre_ids", []):
            db.execute(
                "INSERT OR IGNORE INTO movie_genres (movie_id, genre_id) VALUES (?, ?)",
                (movie_id, genre_id)
            )

        # ── Step 3: Insert cast associations (M:N via movie_actors) ───────────
        for actor in data.get("actors", []):
            db.execute(
                """
                INSERT OR IGNORE INTO movie_actors (movie_id, actor_id, character_name)
                VALUES (?, ?, ?)
                """,
                (movie_id, actor["actor_id"], actor.get("character_name", ""))
            )

    return get_movie_by_id(movie_id)


# ══════════════════════════════════════════════════════════════════════════════
#  UPDATE MOVIE  (transactional — replace metadata + genres + actors)
# ══════════════════════════════════════════════════════════════════════════════
def update_movie(movie_id, data):
    """
    Update movie metadata and replace its genre/actor associations atomically.
    The junction table rows are deleted and re-inserted (replace strategy).
    """
    db = get_db()

    with db:
        # ── Step 1: Update core movie row ─────────────────────────────────────
        db.execute(
            """
            UPDATE movies
               SET title            = :title,
                   release_year     = :release_year,
                   duration_minutes = :duration_minutes,
                   synopsis         = :synopsis,
                   poster_url       = :poster_url,
                   director_id      = :director_id
             WHERE id               = :id
            """,
            {**data, "id": movie_id}
        )

        # ── Step 2: Replace genre associations ────────────────────────────────
        db.execute("DELETE FROM movie_genres WHERE movie_id = ?", (movie_id,))
        for genre_id in data.get("genre_ids", []):
            db.execute(
                "INSERT OR IGNORE INTO movie_genres (movie_id, genre_id) VALUES (?, ?)",
                (movie_id, genre_id)
            )

        # ── Step 3: Replace actor associations ────────────────────────────────
        db.execute("DELETE FROM movie_actors WHERE movie_id = ?", (movie_id,))
        for actor in data.get("actors", []):
            db.execute(
                "INSERT OR IGNORE INTO movie_actors (movie_id, actor_id, character_name) VALUES (?, ?, ?)",
                (movie_id, actor["actor_id"], actor.get("character_name", ""))
            )

    return get_movie_by_id(movie_id)


# ══════════════════════════════════════════════════════════════════════════════
#  DELETE MOVIE
# ══════════════════════════════════════════════════════════════════════════════
def delete_movie(movie_id):
    """
    Delete a movie by ID.
    ON DELETE CASCADE in the schema automatically removes:
      - movie_genres rows  (junction — M:N cleanup)
      - movie_actors rows  (junction — M:N cleanup)
      - ratings rows       (1:N child cleanup)
    """
    db = get_db()
    with db:
        result = db.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    return result.rowcount > 0
