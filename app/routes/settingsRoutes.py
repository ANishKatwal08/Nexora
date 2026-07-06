from flask import Blueprint
from app.controllers import settingsController

bp = Blueprint("settings", __name__)


def register_routes():
    bp.add_url_rule("/settings", view_func=settingsController.settings, methods=["GET"])
    bp.add_url_rule("/settings/password", view_func=settingsController.change_password, methods=["POST"])
    bp.add_url_rule("/settings/delete", view_func=settingsController.delete_account, methods=["POST"])


register_routes()