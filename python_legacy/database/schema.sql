-- =============================================================================
-- Movie Catalog — Database Schema (DDL)
-- =============================================================================
-- All tables use SQLite. Enable FK enforcement before running:
--   PRAGMA foreign_keys = ON;
--
-- Entity Relationships:
--   directors  ──(1:N)──▶  movies
--   movies     ──(1:N)──▶  ratings
--   movies  ◀──(M:N via movie_actors)──▶  actors
--   movies  ◀──(M:N via movie_genres)──▶  genres
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Table 1: directors
-- Parent of movies via 1:N relationship (one director → many movies)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS directors (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,  -- surrogate PK
    name       TEXT    NOT NULL,                   -- director's full name
    bio        TEXT,                               -- short biography
    birth_year INTEGER                             -- year of birth
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Table 2: movies
-- Central entity. References directors via director_id (FK).
-- ON DELETE CASCADE: deleting a director deletes all their movies.
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS movies (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    title            TEXT    NOT NULL,
    release_year     INTEGER,
    duration_minutes INTEGER,
    synopsis         TEXT,
    poster_url       TEXT,
    director_id      INTEGER NOT NULL,
    FOREIGN KEY (director_id)
        REFERENCES directors(id)
        ON DELETE CASCADE            -- remove movies when director is deleted
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Table 3: actors
-- Standalone entity; linked to movies via movie_actors junction table (M:N).
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS actors (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    bio  TEXT
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Table 4: genres
-- Standalone entity; linked to movies via movie_genres junction table (M:N).
-- UNIQUE constraint prevents duplicate genre names.
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS genres (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Table 5: movie_actors  (JUNCTION TABLE — Many-to-Many: movies ↔ actors)
-- ─────────────────────────────────────────────────────────────────────────────
-- A movie can have many actors; an actor can appear in many movies.
-- The COMPOSITE PRIMARY KEY (movie_id, actor_id) prevents duplicate pairings.
-- character_name stores the role the actor plays in that specific movie.
-- ON DELETE CASCADE: removing a movie or actor cleans up this junction row.
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS movie_actors (
    movie_id       INTEGER NOT NULL,
    actor_id       INTEGER NOT NULL,
    character_name TEXT,                              -- role in this movie
    PRIMARY KEY (movie_id, actor_id),                 -- composite PK
    FOREIGN KEY (movie_id)
        REFERENCES movies(id)
        ON DELETE CASCADE,
    FOREIGN KEY (actor_id)
        REFERENCES actors(id)
        ON DELETE CASCADE
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Table 6: movie_genres  (JUNCTION TABLE — Many-to-Many: movies ↔ genres)
-- ─────────────────────────────────────────────────────────────────────────────
-- A movie can belong to many genres; a genre can tag many movies.
-- The COMPOSITE PRIMARY KEY (movie_id, genre_id) prevents duplicate pairings.
-- ON DELETE CASCADE: removing a movie or genre cleans up this junction row.
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),                 -- composite PK
    FOREIGN KEY (movie_id)
        REFERENCES movies(id)
        ON DELETE CASCADE,
    FOREIGN KEY (genre_id)
        REFERENCES genres(id)
        ON DELETE CASCADE
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Table 7: ratings
-- Child of movies via 1:N relationship (one movie → many ratings/reviews).
-- ON DELETE CASCADE: deleting a movie removes all its ratings.
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ratings (
    id         INTEGER  PRIMARY KEY AUTOINCREMENT,
    movie_id   INTEGER  NOT NULL,
    user_name  TEXT     NOT NULL,
    score      INTEGER  NOT NULL CHECK(score BETWEEN 1 AND 10), -- validated 1-10
    review     TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id)
        REFERENCES movies(id)
        ON DELETE CASCADE            -- remove ratings when movie is deleted
);
