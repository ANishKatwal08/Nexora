from flask import request, redirect, url_for, flash, session, render_template
from app.auth import login_required, role_required
from app.repository import user_repo


@login_required
def request_session(mentor_id):
    # Only learners request sessions
    if session.get("user_role") != "learner":
        flash("Only learners can request sessions.", "danger")
        return redirect(url_for("browse.browse"))

    mentor = user_repo.get_user_by_id(mentor_id)
    if not mentor or mentor["role"] != "mentor":
        flash("That mentor was not found.", "danger")
        return redirect(url_for("browse.browse"))

    skill_id = request.form.get("skill_id") or None
    note = request.form.get("note", "").strip()

    user_repo.create_session_request(session["user_id"], mentor_id, skill_id, note)

    flash("Your session request was sent to " + mentor["name"] + ".", "success")
    return redirect(url_for("browse.browse"))

@role_required("mentor")
def mentor_requests():
    mentor_id = session["user_id"]
    requests_list = user_repo.get_requests_for_mentor(mentor_id)
    return render_template("dashboard/mentor_requests.html", requests=requests_list)


@role_required("mentor")
def respond_request(request_id):
    req = user_repo.get_request_by_id(request_id)

    # Make sure this request belongs to this mentor
    if not req or req["mentor_id"] != session["user_id"]:
        flash("That request was not found.", "danger")
        return redirect(url_for("session.mentor_requests"))

    action = request.form.get("action")

    if action == "confirm":
        scheduled_at = request.form.get("scheduled_at") or None
        user_repo.update_request_status(request_id, "confirmed", scheduled_at)
        flash("Session confirmed.", "success")
    elif action == "decline":
        user_repo.update_request_status(request_id, "declined")
        flash("Session declined.", "success")
    elif action == "complete":
        user_repo.update_request_status(request_id, "completed")
        flash("Session marked as completed.", "success")

    return redirect(url_for("session.mentor_requests"))
@login_required
def my_requests():
    if session.get("user_role") != "learner":
        return redirect(url_for("dashboard.dashboard"))
    learner_id = session["user_id"]
    requests_list = user_repo.get_requests_for_learner(learner_id)
    return render_template("dashboard/my_requests.html", requests=requests_list)