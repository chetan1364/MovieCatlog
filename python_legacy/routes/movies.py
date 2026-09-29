"""
routes/movies.py
=================
API route definitions for /api/movies
Routes delegate to movie_controller and rating_controller.
"""

from flask import Blueprint
from controllers import movie_controller, rating_controller

# Create a Blueprint — Flask's way of grouping related routes
movies_bp = Blueprint("movies", __name__)

# ── Movie CRUD ─────────────────────────────────────────────────────────────────
movies_bp.route("/",          methods=["GET"]   )(movie_controller.get_movies)
movies_bp.route("/",          methods=["POST"]  )(movie_controller.create_movie)
movies_bp.route("/<int:movie_id>", methods=["GET"]   )(movie_controller.get_movie)
movies_bp.route("/<int:movie_id>", methods=["PUT"]   )(movie_controller.update_movie)
movies_bp.route("/<int:movie_id>", methods=["DELETE"])(movie_controller.delete_movie)

# ── Nested ratings resource: /api/movies/<id>/ratings ─────────────────────────
movies_bp.route("/<int:movie_id>/ratings", methods=["GET"] )(rating_controller.get_ratings)
movies_bp.route("/<int:movie_id>/ratings", methods=["POST"])(rating_controller.create_rating)
movies_bp.route(
    "/<int:movie_id>/ratings/<int:rating_id>",
    methods=["DELETE"]
)(rating_controller.delete_rating)
