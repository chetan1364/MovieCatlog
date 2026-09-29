"""routes/directors.py — /api/directors"""

from flask import Blueprint
from controllers import director_controller

directors_bp = Blueprint("directors", __name__)

directors_bp.route("/",              methods=["GET"]   )(director_controller.get_directors)
directors_bp.route("/",              methods=["POST"]  )(director_controller.create_director)
directors_bp.route("/<int:director_id>", methods=["GET"]   )(director_controller.get_director)
directors_bp.route("/<int:director_id>", methods=["PUT"]   )(director_controller.update_director)
directors_bp.route("/<int:director_id>", methods=["DELETE"])(director_controller.delete_director)
