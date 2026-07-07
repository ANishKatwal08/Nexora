from flask import Blueprint
from app.controllers import mentorController

bp = Blueprint("mentor", __name__)


def register_routes():
    bp.add_url_rule("/mentor/profile", view_func=mentorController.mentor_profile, methods=["GET"])
    bp.add_url_rule("/mentor/details", view_func=mentorController.update_mentor_details, methods=["POST"])
    bp.add_url_rule("/mentor/skill/add", view_func=mentorController.add_skill, methods=["POST"])
    bp.add_url_rule("/mentor/skill/remove", view_func=mentorController.remove_skill, methods=["POST"])


register_routes()