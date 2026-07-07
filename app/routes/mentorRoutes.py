from flask import Blueprint
from app.controllers import mentorController

bp = Blueprint("mentor", __name__)


def register_routes():
    bp.add_url_rule("/mentor/profile", view_func=mentorController.mentor_profile, methods=["GET"])
    bp.add_url_rule("/mentor/profile/save", view_func=mentorController.mentor_profile_save, methods=["POST"])
    bp.add_url_rule("/mentor/profile/delete", view_func=mentorController.mentor_profile_delete, methods=["POST"])


register_routes()