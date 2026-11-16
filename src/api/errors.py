"""Error handling.

TRAINING DEMO: this file contains an INTENTIONAL vulnerability (stack trace exposure).
"""
import traceback

from flask import Blueprint

errors_bp = Blueprint("errors", __name__)


@errors_bp.app_errorhandler(Exception)
def handle_error(error):
    # VULNERABLE (intentional): internal error details are sent to the user
    return traceback.format_exc(), 500
