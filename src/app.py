"""Oil Field Daily Reports - training demo application.

Run locally:  python -m src.app
"""
from flask import Flask, send_from_directory

from src.api.errors import errors_bp
from src.api.export import export_bp
from src.api.reports import reports_bp
from src.api.search import search_bp
from src.auth.tokens import auth_bp
from src.db import init_db

app = Flask(__name__, static_folder="../web", static_url_path="/web")

for bp in (reports_bp, export_bp, search_bp, errors_bp, auth_bp):
    app.register_blueprint(bp)


@app.route("/")
def index():
    return send_from_directory("../web", "index.html")


if __name__ == "__main__":
    init_db()
    # VULNERABLE (intentional): debug mode must never be enabled in production
    app.run(host="127.0.0.1", port=5000, debug=True)
