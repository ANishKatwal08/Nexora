from flask import Blueprint
from app.controllers import profileController

bp = Blueprint("profile", __name__)


def register_routes():
    bp.add_url_rule("/profile", view_func=profileController.profile, methods=["GET"])
    bp.add_url_rule("/profile/update", view_func=profileController.profile_update, methods=["POST"])


register_routes()