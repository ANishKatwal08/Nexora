from flask import Blueprint
from app.controllers import pagesController

bp = Blueprint("pages", __name__)


def register_routes():
    bp.add_url_rule("/about", view_func=pagesController.about, methods=["GET"])
    bp.add_url_rule("/contact", view_func=pagesController.contact, methods=["GET"])
    bp.add_url_rule("/terms", view_func=pagesController.terms, methods=["GET"])
    bp.add_url_rule("/privacy", view_func=pagesController.privacy, methods=["GET"])


register_routes()