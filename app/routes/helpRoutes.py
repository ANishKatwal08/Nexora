from flask import Blueprint
from app.controllers import helpController

bp = Blueprint("help", __name__)


def register_routes():
    bp.add_url_rule("/help", view_func=helpController.help_page, methods=["GET"])


register_routes()