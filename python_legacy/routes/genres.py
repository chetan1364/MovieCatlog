"""routes/genres.py — /api/genres"""

from flask import Blueprint
from controllers import genre_controller

genres_bp = Blueprint("genres", __name__)

genres_bp.route("/",             methods=["GET"]   )(genre_controller.get_genres)
genres_bp.route("/",             methods=["POST"]  )(genre_controller.create_genre)
genres_bp.route("/<int:genre_id>", methods=["DELETE"])(genre_controller.delete_genre)
