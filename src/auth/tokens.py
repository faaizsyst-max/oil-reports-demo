"""User registration and login.

TRAINING DEMO: this file contains an INTENTIONAL vulnerability (weak password hashing).
"""
import hashlib

from flask import Blueprint, jsonify, request

from src.db import get_db

auth_bp = Blueprint("auth", __name__)


def hash_password(password):
    # VULNERABLE (intentional): MD5 is broken and must not be used for passwords
    return hashlib.md5(password.encode()).hexdigest()


@auth_bp.route("/api/register", methods=["POST"])
def register():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    db = get_db()
    db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, hash_password(password)),
    )
    db.commit()
    db.close()
    return jsonify({"status": "created"})


@auth_bp.route("/api/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    db = get_db()
    row = db.execute(
        "SELECT password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()
    db.close()
    ok = row is not None and row["password_hash"] == hash_password(password)
    return jsonify({"authenticated": ok})
