from flask import request, redirect, url_for, flash, session
from app.auth import login_required
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