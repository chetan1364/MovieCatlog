"""
controllers/movie_controller.py
================================
Handles HTTP request parsing, validation, and response formatting for movies.
Delegates all database work to movie_service.py (Separation of Concerns).
"""

from flask import request, jsonify
from services import movie_service


def get_movies():
    """
    GET /api/movies
    Query params:
      - search     : keyword (matches title, director, actor)
      - genre      : exact genre name
      - year_from  : minimum release year
      - year_to    : maximum release year
      - sort_by    : 'title' | 'release_year' | 'avg_rating'
      - sort_order : 'ASC' | 'DESC'
    """
    movies = movie_service.get_all_movies(
        search     = request.args.get("search"),
        genre      = request.args.get("genre"),
        year_from  = request.args.get("year_from"),
        year_to    = request.args.get("year_to"),
        sort_by    = request.args.get("sort_by", "title"),
        sort_order = request.args.get("sort_order", "ASC"),
    )
    return jsonify({"success": True, "data": movies, "count": len(movies)}), 200


def get_movie(movie_id):
    """GET /api/movies/<id> — full detail with cast, genres, ratings"""
    movie = movie_service.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({"success": False, "error": "Movie not found"}), 404
    return jsonify({"success": True, "data": movie}), 200


def create_movie():
    """
    POST /api/movies
    Body (JSON):
      {
        "title": "...",
        "release_year": 2024,
        "duration_minutes": 120,
        "synopsis": "...",
        "poster_url": "...",
        "director_id": 1,
        "genre_ids": [1, 2],
        "actors": [{"actor_id": 3, "character_name": "..."}]
      }
    """
    body = request.get_json()
    if not body:
        return jsonify({"success": False, "error": "Request body is required"}), 400

    # ── Required field validation ──────────────────────────────────────────────
    required = ["title", "director_id"]
    missing = [f for f in required if not body.get(f)]
    if missing:
        return jsonify({"success": False, "error": f"Missing fields: {missing}"}), 400

    try:
        movie = movie_service.create_movie(body)
        return jsonify({"success": True, "data": movie}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def update_movie(movie_id):
    """PUT /api/movies/<id> — update movie metadata + genres + actors"""
    body = request.get_json()
    if not body:
        return jsonify({"success": False, "error": "Request body is required"}), 400

    existing = movie_service.get_movie_by_id(movie_id)
    if not existing:
        return jsonify({"success": False, "error": "Movie not found"}), 404

    try:
        movie = movie_service.update_movie(movie_id, body)
        return jsonify({"success": True, "data": movie}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def delete_movie(movie_id):
    """DELETE /api/movies/<id> — cascades to junction tables + ratings"""
    deleted = movie_service.delete_movie(movie_id)
    if not deleted:
        return jsonify({"success": False, "error": "Movie not found"}), 404
    return jsonify({"success": True, "message": "Movie deleted successfully"}), 200
