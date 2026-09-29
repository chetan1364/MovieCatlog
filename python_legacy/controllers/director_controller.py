"""
controllers/director_controller.py
====================================
HTTP handlers for director endpoints.
"""

from flask import request, jsonify
from services import director_service


def get_directors():
    directors = director_service.get_all_directors()
    return jsonify({"success": True, "data": directors}), 200


def get_director(director_id):
    director = director_service.get_director_by_id(director_id)
    if not director:
        return jsonify({"success": False, "error": "Director not found"}), 404
    return jsonify({"success": True, "data": director}), 200


def create_director():
    body = request.get_json()
    if not body or not body.get("name"):
        return jsonify({"success": False, "error": "Name is required"}), 400
    director = director_service.create_director(body)
    return jsonify({"success": True, "data": director}), 201


def update_director(director_id):
    body = request.get_json()
    if not body:
        return jsonify({"success": False, "error": "Request body is required"}), 400
    if not director_service.get_director_by_id(director_id):
        return jsonify({"success": False, "error": "Director not found"}), 404
    director = director_service.update_director(director_id, body)
    return jsonify({"success": True, "data": director}), 200


def delete_director(director_id):
    deleted = director_service.delete_director(director_id)
    if not deleted:
        return jsonify({"success": False, "error": "Director not found"}), 404
    return jsonify({"success": True, "message": "Director deleted"}), 200
