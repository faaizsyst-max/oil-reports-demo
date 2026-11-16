"""Export saved report files.

TRAINING DEMO: this file contains an INTENTIONAL vulnerability (path traversal).
"""
import os

from flask import Blueprint, request

export_bp = Blueprint("export", __name__)

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "exports")


@export_bp.route("/api/export")
def export_file():
    name = request.args.get("file", "")
    # VULNERABLE (intentional): the file name is not validated, so "../../" can read any file
    path = os.path.join(EXPORT_DIR, name)
    with open(path, encoding="utf-8") as f:
        return f.read()
