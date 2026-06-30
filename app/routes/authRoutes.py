from flask import Blueprint
from app.controllers import authController

bp = Blueprint("auth", __name__)


def register_routes():
    bp.add_url_rule("/register", view_func=authController.register, methods=["GET", "POST"])
    bp.add_url_rule("/login", view_func=authController.login, methods=["GET", "POST"])
    bp.add_url_rule("/verify", view_func=authController.verify, methods=["GET", "POST"])
    bp.add_url_rule("/logout", view_func=authController.logout, methods=["GET"])


register_routes()