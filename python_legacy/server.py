"""
server.py
=========
Movie Catalog — Flask application entry point.

Architecture:
  server.py  →  routes/  →  controllers/  →  services/  →  database/

Environment:
  Reads from .env file via python-dotenv (PORT, DATABASE_URL, SECRET_KEY)
"""

import os
import sys
from pathlib import Path

# ── Load environment variables from .env ──────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, send_from_directory
from flask_cors import CORS

# ── Import route Blueprints ───────────────────────────────────────────────────
from routes.movies    import movies_bp
from routes.directors import directors_bp
from routes.actors    import actors_bp
from routes.genres    import genres_bp

# ── Create Flask app ──────────────────────────────────────────────────────────
app = Flask(
    __name__,
    static_folder="public",   # Serve frontend from /public directory
    static_url_path=""
)

app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# Enable CORS for all API routes (allows frontend on same or different port)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ── Register API Blueprints ───────────────────────────────────────────────────
app.register_blueprint(movies_bp,    url_prefix="/api/movies")
app.register_blueprint(directors_bp, url_prefix="/api/directors")
app.register_blueprint(actors_bp,    url_prefix="/api/actors")
app.register_blueprint(genres_bp,    url_prefix="/api/genres")


# ── Frontend routes ───────────────────────────────────────────────────────────

@app.route("/")
def catalog():
    """Serve the movie catalog page (index.html)."""
    return send_from_directory("public", "index.html")


@app.route("/movie")
def movie_detail():
    """Serve the movie detail page (movie.html)."""
    return send_from_directory("public", "movie.html")


@app.route("/admin")
def admin():
    """Serve the admin panel (admin.html)."""
    return send_from_directory("public", "admin.html")


# ── Global error handlers ─────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    from flask import jsonify, request
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Endpoint not found"}), 404
    return send_from_directory("public", "index.html")


@app.errorhandler(500)
def server_error(e):
    from flask import jsonify
    return jsonify({"success": False, "error": "Internal server error"}), 500


# ── Teardown: close DB connection on app shutdown ─────────────────────────────
from database.db import close_db

@app.teardown_appcontext
def shutdown_db(exception=None):
    pass  # Singleton connection persists; close_db() called at process exit


# ── Start server ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n🎬 Movie Catalog server starting on http://localhost:{port}")
    print(f"   Catalog  →  http://localhost:{port}/")
    print(f"   Admin    →  http://localhost:{port}/admin")
    print(f"   API      →  http://localhost:{port}/api/movies\n")
    app.run(host="0.0.0.0", port=port, debug=True)
