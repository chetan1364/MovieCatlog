"""routes/actors.py — /api/actors"""

from flask import Blueprint
from controllers import actor_controller

actors_bp = Blueprint("actors", __name__)

actors_bp.route("/",             methods=["GET"]   )(actor_controller.get_actors)
actors_bp.route("/",             methods=["POST"]  )(actor_controller.create_actor)
actors_bp.route("/<int:actor_id>", methods=["GET"]   )(actor_controller.get_actor)
actors_bp.route("/<int:actor_id>", methods=["PUT"]   )(actor_controller.update_actor)
actors_bp.route("/<int:actor_id>", methods=["DELETE"])(actor_controller.delete_actor)
