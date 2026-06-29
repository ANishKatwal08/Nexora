from flask import Blueprint
from app.controllers import authController

bp = Blueprint("auth", __name__)


def register_routes():
    bp.add_url_rule("/register", view_func=authController.register, methods=["GET", "POST"])


register_routes()