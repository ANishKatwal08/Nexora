from flask import Blueprint
from app.controllers import browseController

bp = Blueprint("browse", __name__)


def register_routes():
    bp.add_url_rule("/browse", view_func=browseController.browse, methods=["GET"])


register_routes()