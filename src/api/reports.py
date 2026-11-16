"""Daily production reports API.

TRAINING DEMO: this file contains an INTENTIONAL vulnerability (SQL injection).
"""
from flask import Blueprint, jsonify, request

from src.db import get_db

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/api/reports")
def get_report():
    field_id = request.args.get("field_id", "")
    db = get_db()
    # VULNERABLE (intentional): user input is concatenated directly into the SQL query
    q = f"SELECT * FROM reports WHERE field_id = '{field_id}'"
    rows = db.execute(q).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@reports_bp.route("/api/reports/summary")
def summary():
    db = get_db()
    rows = db.execute(
        "SELECT field_name, SUM(oil_bbl) AS total_bbl FROM reports GROUP BY field_name"
    ).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])
