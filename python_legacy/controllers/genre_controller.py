"""
controllers/genre_controller.py
================================
HTTP handlers for genre endpoints.
"""

from flask import request, jsonify
from services import genre_service


def get_genres():
    genres = genre_service.get_all_genres()
    return jsonify({"success": True, "data": genres}), 200


def create_genre():
    body = request.get_json()
    if not body or not body.get("name"):
        return jsonify({"success": False, "error": "Genre name is required"}), 400
    genre = genre_service.create_genre(body)
    return jsonify({"success": True, "data": genre}), 201


def delete_genre(genre_id):
    deleted = genre_service.delete_genre(genre_id)
    if not deleted:
        return jsonify({"success": False, "error": "Genre not found"}), 404
    return jsonify({"success": True, "message": "Genre deleted"}), 200
