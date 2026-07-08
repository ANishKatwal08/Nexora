from flask import Blueprint
from app.controllers import adminController

bp = Blueprint("admin", __name__)


def register_routes():
    bp.add_url_rule("/admin/users", view_func=adminController.admin_users, methods=["GET"])
    bp.add_url_rule("/admin/users/<int:user_id>/toggle", view_func=adminController.toggle_user, methods=["POST"])


register_routes()