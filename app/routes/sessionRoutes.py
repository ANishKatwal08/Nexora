from flask import Blueprint
from app.controllers import sessionController

bp = Blueprint("session", __name__)


def register_routes():
    bp.add_url_rule("/session/request/<int:mentor_id>", view_func=sessionController.request_session, methods=["POST"])
    bp.add_url_rule("/mentor/requests", view_func=sessionController.mentor_requests, methods=["GET"])
    bp.add_url_rule("/session/respond/<int:request_id>", view_func=sessionController.respond_request, methods=["POST"])


register_routes()