"""
database/seed.py
================
Seed script — populates the database with 10 realistic movies.

Data relationships seeded:
  - 7 directors  (parent of movies via 1:N FK)
  - 10 movies    (linked to directors)
  - 15 actors    (linked to movies via movie_actors junction — M:N)
  - 8 genres     (linked to movies via movie_genres junction — M:N)
  - ~40 ratings  (linked to movies via 1:N FK)

Run via: python database/init.py
"""

from database.db import get_db

# ── Raw seed data ─────────────────────────────────────────────────────────────

DIRECTORS = [
    {"name": "Frank Darabont",      "bio": "American film director known for adapting Stephen King works.", "birth_year": 1959},
    {"name": "Christopher Nolan",   "bio": "British-American director renowned for mind-bending narratives.", "birth_year": 1970},
    {"name": "Quentin Tarantino",   "bio": "American director celebrated for nonlinear storytelling and stylized violence.", "birth_year": 1963},
    {"name": "Robert Zemeckis",     "bio": "American director and pioneer of visual effects technology.", "birth_year": 1951},
    {"name": "Francis Ford Coppola","bio": "Legendary American director of the Godfather trilogy.", "birth_year": 1939},
    {"name": "Lana Wachowski",      "bio": "American filmmaker and co-creator of The Matrix franchise.", "birth_year": 1965},
    {"name": "David Fincher",       "bio": "American director known for dark psychological thrillers.", "birth_year": 1962},
    {"name": "Steven Spielberg",    "bio": "Iconic American director and one of the most influential filmmakers in history.", "birth_year": 1946},
]

GENRES = [
    "Drama", "Crime", "Action", "Sci-Fi",
    "Thriller", "Romance", "War", "Mystery"
]

ACTORS = [
    {"name": "Tim Robbins",        "bio": "American actor and filmmaker, known for his versatility."},
    {"name": "Morgan Freeman",     "bio": "Legendary American actor with a distinctive voice and powerful screen presence."},
    {"name": "Christian Bale",     "bio": "Welsh actor famous for extreme physical transformations."},
    {"name": "Heath Ledger",       "bio": "Australian actor who delivered an iconic performance as the Joker."},
    {"name": "Leonardo DiCaprio",  "bio": "American actor celebrated for intense, method-driven performances."},
    {"name": "Joseph Gordon-Levitt","bio": "American actor known for roles in independent and blockbuster films."},
    {"name": "John Travolta",      "bio": "American actor and dancer who revived his career through Pulp Fiction."},
    {"name": "Samuel L. Jackson",  "bio": "American actor with one of the highest-grossing filmographies in history."},
    {"name": "Tom Hanks",          "bio": "Beloved American actor with two consecutive Academy Award wins."},
    {"name": "Marlon Brando",      "bio": "Revolutionary American actor who redefined screen acting."},
    {"name": "Al Pacino",          "bio": "American actor famous for intense, passionate performances."},
    {"name": "Keanu Reeves",       "bio": "Canadian actor known for action roles and philosophical curiosity."},
    {"name": "Brad Pitt",          "bio": "American actor and producer with a wide range of dramatic roles."},
    {"name": "Edward Norton",      "bio": "American actor known for intellectual, complex characters."},
    {"name": "Liam Neeson",        "bio": "Irish actor celebrated for dramatic and action roles."},
]

MOVIES = [
    {
        "title": "The Shawshank Redemption",
        "release_year": 1994,
        "duration_minutes": 142,
        "synopsis": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "poster_url": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "director": "Frank Darabont",
        "genres": ["Drama", "Crime"],
        "actors": [
            {"name": "Tim Robbins",    "character": "Andy Dufresne"},
            {"name": "Morgan Freeman", "character": "Ellis Boyd 'Red' Redding"},
        ],
        "ratings": [
            {"user": "cinephile_raj", "score": 10, "review": "The greatest film ever made. Timeless."},
            {"user": "priya_watches", "score": 9,  "review": "Morgan Freeman's narration alone is worth watching."},
            {"user": "movie_buff_87", "score": 10, "review": "Changed my perspective on hope and friendship."},
            {"user": "ananya_k",      "score": 9,  "review": "Emotionally overwhelming from start to finish."},
        ],
    },
    {
        "title": "The Dark Knight",
        "release_year": 2008,
        "duration_minutes": 152,
        "synopsis": "Batman raises the stakes in his war on crime, but is forced into a battle of wills with the anarchic Joker.",
        "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "director": "Christopher Nolan",
        "genres": ["Action", "Crime", "Drama"],
        "actors": [
            {"name": "Christian Bale", "character": "Bruce Wayne / Batman"},
            {"name": "Heath Ledger",   "character": "The Joker"},
        ],
        "ratings": [
            {"user": "batman_fan_2024", "score": 10, "review": "Heath Ledger's Joker is unmatched in cinematic history."},
            {"user": "rohan_m",         "score": 9,  "review": "Every scene is tense. Nolan at his absolute peak."},
            {"user": "sneha_v",         "score": 10, "review": "More than a superhero film — a crime epic."},
        ],
    },
    {
        "title": "Inception",
        "release_year": 2010,
        "duration_minutes": 148,
        "synopsis": "A skilled thief is offered a chance to have his criminal record erased if he can successfully plant an idea into a target's subconscious.",
        "poster_url": "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg",
        "director": "Christopher Nolan",
        "genres": ["Action", "Sci-Fi", "Thriller"],
        "actors": [
            {"name": "Leonardo DiCaprio",   "character": "Dom Cobb"},
            {"name": "Joseph Gordon-Levitt","character": "Arthur"},
        ],
        "ratings": [
            {"user": "dream_explorer",  "score": 10, "review": "Mind-bending. Every rewatch reveals something new."},
            {"user": "kartik_s",        "score": 9,  "review": "The hallway fight scene alone earns a 10/10."},
            {"user": "aisha_t",         "score": 8,  "review": "Complex but rewarding. DiCaprio at his finest."},
        ],
    },
    {
        "title": "Pulp Fiction",
        "release_year": 1994,
        "duration_minutes": 154,
        "synopsis": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
        "poster_url": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
        "director": "Quentin Tarantino",
        "genres": ["Crime", "Drama", "Thriller"],
        "actors": [
            {"name": "John Travolta",  "character": "Vincent Vega"},
            {"name": "Samuel L. Jackson", "character": "Jules Winnfield"},
        ],
        "ratings": [
            {"user": "tarantino_lover", "score": 10, "review": "Dialogue like poetry. Changed cinema forever."},
            {"user": "ravi_p",          "score": 9,  "review": "Non-linear storytelling done to perfection."},
            {"user": "meera_j",         "score": 9,  "review": "Every character is unforgettable."},
        ],
    },
    {
        "title": "Forrest Gump",
        "release_year": 1994,
        "duration_minutes": 142,
        "synopsis": "The presidencies of Kennedy and Johnson, Vietnam, Watergate, and other events unfold from the perspective of an Alabama man with a low IQ.",
        "poster_url": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
        "director": "Robert Zemeckis",
        "genres": ["Drama", "Romance"],
        "actors": [
            {"name": "Tom Hanks", "character": "Forrest Gump"},
        ],
        "ratings": [
            {"user": "classic_fan",  "score": 10, "review": "Life is like a box of chocolates — and this film is the best one."},
            {"user": "deepa_n",     "score": 9,  "review": "Tom Hanks delivers the performance of a lifetime."},
            {"user": "arjun_k",     "score": 8,  "review": "Touching, funny, and utterly American."},
            {"user": "sana_m",      "score": 10, "review": "Cried three times. An absolute masterpiece of heart."},
        ],
    },
    {
        "title": "The Godfather",
        "release_year": 1972,
        "duration_minutes": 175,
        "synopsis": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "poster_url": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsLegHnDmni4k.jpg",
        "director": "Francis Ford Coppola",
        "genres": ["Crime", "Drama"],
        "actors": [
            {"name": "Marlon Brando", "character": "Don Vito Corleone"},
            {"name": "Al Pacino",     "character": "Michael Corleone"},
        ],
        "ratings": [
            {"user": "old_school_cinephile", "score": 10, "review": "The standard all crime films are measured against."},
            {"user": "vikram_r",              "score": 10, "review": "Brando makes every second electrifying."},
            {"user": "parul_d",               "score": 9,  "review": "A portrait of power, family, and corruption."},
        ],
    },
    {
        "title": "Interstellar",
        "release_year": 2014,
        "duration_minutes": 169,
        "synopsis": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "director": "Christopher Nolan",
        "genres": ["Sci-Fi", "Drama", "Action"],
        "actors": [
            {"name": "Matthew McConaughey", "character": "Cooper"},
            {"name": "Anne Hathaway",       "character": "Dr. Brand"},
        ],
        "ratings": [
            {"user": "space_nerd_2024", "score": 10, "review": "The docking scene. The tesseract. Nothing comes close."},
            {"user": "nisha_p",         "score": 9,  "review": "Emotionally and scientifically breathtaking."},
            {"user": "karan_v",         "score": 8,  "review": "Long, but every minute earns its place."},
        ],
    },
    {
        "title": "The Matrix",
        "release_year": 1999,
        "duration_minutes": 136,
        "synopsis": "A hacker discovers the true nature of his reality and joins a rebellion against the machines that have enslaved humanity.",
        "poster_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
        "director": "Lana Wachowski",
        "genres": ["Action", "Sci-Fi"],
        "actors": [
            {"name": "Keanu Reeves",    "character": "Neo"},
            {"name": "Laurence Fishburne", "character": "Morpheus"},
        ],
        "ratings": [
            {"user": "redpill_taken",  "score": 10, "review": "Revolutionised action filmmaking. Bullet time forever."},
            {"user": "tech_cinephile", "score": 9,  "review": "Philosophy, action, and style in perfect balance."},
            {"user": "anita_g",        "score": 9,  "review": "Still looks stunning after 25 years."},
        ],
    },
    {
        "title": "Schindler's List",
        "release_year": 1993,
        "duration_minutes": 195,
        "synopsis": "In German-occupied Poland during WWII, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce.",
        "poster_url": "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg",
        "director": "Steven Spielberg",
        "genres": ["Drama", "War"],
        "actors": [
            {"name": "Liam Neeson",  "character": "Oskar Schindler"},
            {"name": "Ben Kingsley", "character": "Itzhak Stern"},
        ],
        "ratings": [
            {"user": "history_student",  "score": 10, "review": "Devastating, necessary, and unforgettable."},
            {"user": "tamara_s",         "score": 10, "review": "Spielberg's greatest achievement. A moral landmark."},
            {"user": "mihail_p",         "score": 9,  "review": "Cinema as a witness to history."},
        ],
    },
    {
        "title": "Fight Club",
        "release_year": 1999,
        "duration_minutes": 139,
        "synopsis": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much more.",
        "poster_url": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "director": "David Fincher",
        "genres": ["Drama", "Thriller", "Mystery"],
        "actors": [
            {"name": "Brad Pitt",    "character": "Tyler Durden"},
            {"name": "Edward Norton","character": "The Narrator"},
        ],
        "ratings": [
            {"user": "first_rule_fan", "score": 10, "review": "Fincher crafted a cultural artefact. Still relevant."},
            {"user": "shreya_m",       "score": 9,  "review": "The twist still gets me every time."},
            {"user": "siddharth_k",    "score": 8,  "review": "Dark, visceral, and brilliantly acted."},
            {"user": "pooja_r",        "score": 10, "review": "Challenges everything you think you know about identity."},
        ],
    },
]


def seed_database():
    """
    Inserts all seed data into the database using a single transaction.
    If any insert fails, the entire seed is rolled back (atomicity).
    """
    db = get_db()
    cursor = db.cursor()

    # ── Check if already seeded ───────────────────────────────────────────────
    existing = cursor.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    if existing > 0:
        print(f"  ↳ Database already contains {existing} movies. Skipping seed.")
        return

    print("  Seeding directors...")
    director_ids = {}
    for d in DIRECTORS:
        cursor.execute(
            "INSERT INTO directors (name, bio, birth_year) VALUES (?, ?, ?)",
            (d["name"], d["bio"], d["birth_year"])
        )
        director_ids[d["name"]] = cursor.lastrowid

    print("  Seeding genres...")
    genre_ids = {}
    for g in GENRES:
        cursor.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (g,))
        row = cursor.execute("SELECT id FROM genres WHERE name = ?", (g,)).fetchone()
        genre_ids[g] = row[0]

    print("  Seeding actors...")
    actor_ids = {}
    for a in ACTORS:
        cursor.execute(
            "INSERT OR IGNORE INTO actors (name, bio) VALUES (?, ?)",
            (a["name"], a["bio"])
        )
        row = cursor.execute("SELECT id FROM actors WHERE name = ?", (a["name"],)).fetchone()
        if row:
            actor_ids[a["name"]] = row[0]

    print("  Seeding movies, cast, genres, and ratings...")
    for m in MOVIES:
        # ── Insert movie with director FK ─────────────────────────────────────
        d_id = director_ids.get(m["director"])
        cursor.execute(
            """
            INSERT INTO movies (title, release_year, duration_minutes, synopsis, poster_url, director_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (m["title"], m["release_year"], m["duration_minutes"],
             m["synopsis"], m["poster_url"], d_id)
        )
        movie_id = cursor.lastrowid

        # ── Insert into movie_genres junction table (M:N) ─────────────────────
        for g_name in m["genres"]:
            g_id = genre_ids.get(g_name)
            if g_id:
                cursor.execute(
                    "INSERT OR IGNORE INTO movie_genres (movie_id, genre_id) VALUES (?, ?)",
                    (movie_id, g_id)
                )

        # ── Insert into movie_actors junction table (M:N) ─────────────────────
        for a_entry in m["actors"]:
            a_name = a_entry["name"]
            # Some seed actors (Fishburne, Hathaway, McConaughey, Kingsley) are
            # not in the main ACTORS list — insert them on the fly.
            if a_name not in actor_ids:
                cursor.execute(
                    "INSERT OR IGNORE INTO actors (name, bio) VALUES (?, ?)",
                    (a_name, "")
                )
                row = cursor.execute("SELECT id FROM actors WHERE name = ?", (a_name,)).fetchone()
                actor_ids[a_name] = row[0]
            a_id = actor_ids[a_name]
            cursor.execute(
                """
                INSERT OR IGNORE INTO movie_actors (movie_id, actor_id, character_name)
                VALUES (?, ?, ?)
                """,
                (movie_id, a_id, a_entry["character"])
            )

        # ── Insert ratings (1:N child of movie) ───────────────────────────────
        for r in m["ratings"]:
            cursor.execute(
                """
                INSERT INTO ratings (movie_id, user_name, score, review)
                VALUES (?, ?, ?, ?)
                """,
                (movie_id, r["user"], r["score"], r["review"])
            )

    db.commit()
    print("  ✓ Seed complete.")
