from flask import Blueprint
from app.controllers import groupController

bp = Blueprint("group", __name__)


def register_routes():
    bp.add_url_rule("/groups", view_func=groupController.group_list, methods=["GET"])
    bp.add_url_rule("/groups/mine", view_func=groupController.my_group_sessions, methods=["GET"])
    bp.add_url_rule("/groups/create", view_func=groupController.create_group, methods=["GET", "POST"])
    bp.add_url_rule("/groups/<int:session_id>", view_func=groupController.group_detail, methods=["GET"])
    bp.add_url_rule("/groups/<int:session_id>/join", view_func=groupController.join_group, methods=["POST"])
    bp.add_url_rule("/groups/<int:session_id>/leave", view_func=groupController.leave_group, methods=["POST"])
    bp.add_url_rule("/groups/<int:session_id>/delete", view_func=groupController.remove_group, methods=["POST"])


register_routes()