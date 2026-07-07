from flask import Blueprint
from app.controllers import messageController

bp = Blueprint("message", __name__)


def register_routes():
    bp.add_url_rule("/messages", view_func=messageController.inbox, methods=["GET"])
    bp.add_url_rule("/messages/<int:other_id>", view_func=messageController.conversation, methods=["GET"])
    bp.add_url_rule("/messages/<int:other_id>/send", view_func=messageController.send, methods=["POST"])


register_routes()