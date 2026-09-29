"""
controllers/actor_controller.py
================================
HTTP handlers for actor endpoints.
"""

from flask import request, jsonify
from services import actor_service


def get_actors():
    actors = actor_service.get_all_actors()
    return jsonify({"success": True, "data": actors}), 200


def get_actor(actor_id):
    actor = actor_service.get_actor_by_id(actor_id)
    if not actor:
        return jsonify({"success": False, "error": "Actor not found"}), 404
    return jsonify({"success": True, "data": actor}), 200


def create_actor():
    body = request.get_json()
    if not body or not body.get("name"):
        return jsonify({"success": False, "error": "Name is required"}), 400
    actor = actor_service.create_actor(body)
    return jsonify({"success": True, "data": actor}), 201


def update_actor(actor_id):
    body = request.get_json()
    if not body:
        return jsonify({"success": False, "error": "Request body is required"}), 400
    if not actor_service.get_actor_by_id(actor_id):
        return jsonify({"success": False, "error": "Actor not found"}), 404
    actor = actor_service.update_actor(actor_id, body)
    return jsonify({"success": True, "data": actor}), 200


def delete_actor(actor_id):
    deleted = actor_service.delete_actor(actor_id)
    if not deleted:
        return jsonify({"success": False, "error": "Actor not found"}), 404
    return jsonify({"success": True, "message": "Actor deleted"}), 200
