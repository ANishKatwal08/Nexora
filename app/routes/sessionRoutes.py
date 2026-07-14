from flask import Blueprint
from app.controllers import sessionController

bp = Blueprint("session", __name__)


def register_routes():
    bp.add_url_rule("/session/request/<int:mentor_id>", view_func=sessionController.request_session, methods=["POST"])
    bp.add_url_rule("/mentor/requests", view_func=sessionController.mentor_requests, methods=["GET"])
    bp.add_url_rule("/session/respond/<int:request_id>", view_func=sessionController.respond_request, methods=["POST"])
    bp.add_url_rule("/my/requests", view_func=sessionController.my_requests, methods=["GET"])
    bp.add_url_rule("/session/feedback/<int:request_id>", view_func=sessionController.leave_feedback, methods=["POST"])
    bp.add_url_rule("/session/cancel/<int:request_id>", view_func=sessionController.cancel_request, methods=["POST"])
    bp.add_url_rule("/session/feedback/<int:request_id>/edit", view_func=sessionController.edit_feedback, methods=["POST"])
    bp.add_url_rule("/session/feedback/<int:request_id>/delete", view_func=sessionController.remove_feedback, methods=["POST"])
    bp.add_url_rule("/session/pay/<int:request_id>", view_func=sessionController.mark_paid, methods=["POST"])
register_routes()