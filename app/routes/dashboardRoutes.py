from flask import Blueprint
from app.controllers import dashboardController

bp = Blueprint("dashboard", __name__)


def register_routes():
    bp.add_url_rule("/dashboard", view_func=dashboardController.dashboard, methods=["GET"])


register_routes()