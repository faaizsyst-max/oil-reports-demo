"""Search page for field names.

TRAINING DEMO: this file contains an INTENTIONAL vulnerability (reflected XSS).
"""
from flask import Blueprint, request

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
def search():
    term = request.args.get("q", "")
    # VULNERABLE (intentional): user input is returned inside HTML without escaping
    return f"<h2>Search results for: {term}</h2><p>No matching fields.</p>"
