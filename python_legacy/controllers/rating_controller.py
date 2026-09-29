"""
controllers/rating_controller.py
=================================
HTTP handlers for rating/review endpoints.
"""

from flask import request, jsonify
from services import rating_service


def get_ratings(movie_id):
    ratings = rating_service.get_ratings_for_movie(movie_id)
    return jsonify({"success": True, "data": ratings}), 200


def create_rating(movie_id):
    """
    POST /api/movies/<movie_id>/ratings
    Body: { "user_name": "...", "score": 8, "review": "..." }
    """
    body = request.get_json()
    if not body:
        return jsonify({"success": False, "error": "Request body required"}), 400

    required = ["user_name", "score"]
    missing = [f for f in required if body.get(f) is None]
    if missing:
        return jsonify({"success": False, "error": f"Missing: {missing}"}), 400

    try:
        rating = rating_service.create_rating({
            "movie_id":  movie_id,
            "user_name": body["user_name"],
            "score":     int(body["score"]),
            "review":    body.get("review", ""),
        })
        return jsonify({"success": True, "data": rating}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def delete_rating(movie_id, rating_id):
    deleted = rating_service.delete_rating(rating_id)
    if not deleted:
        return jsonify({"success": False, "error": "Rating not found"}), 404
    return jsonify({"success": True, "message": "Rating deleted"}), 200
