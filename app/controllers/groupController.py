from flask import render_template, request, redirect, url_for, flash, session, abort
from app.auth import login_required, role_required
from app.repository import group_repo, user_repo


@login_required
def group_list():
    """Public-ish list of open group sessions, for learners to browse and join."""
    sessions = group_repo.get_open_group_sessions()
    my_id = session.get("user_id")
    # mark which ones the current learner has already joined
    for s in sessions:
        s["joined"] = group_repo.has_joined(s["id"], my_id) if my_id else False
        s["is_full"] = s["joined_count"] >= s["capacity"]
    return render_template("dashboard/group_list.html", sessions=sessions)


@role_required("mentor")
def my_group_sessions():
    """A mentor's own group sessions."""
    mentor_id = session["user_id"]
    sessions = group_repo.get_group_sessions_for_mentor(mentor_id)
    return render_template("dashboard/group_mine.html", sessions=sessions)


@role_required("mentor")
def create_group():
    """Show the create form (GET) or handle it (POST)."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        skill_id = request.form.get("skill_id") or None
        capacity_raw = request.form.get("capacity", "").strip()
        scheduled_at = request.form.get("scheduled_at") or None

        if not title:
            flash("Please give your group session a title.", "danger")
            return redirect(url_for("group.create_group"))

        capacity = int(capacity_raw) if capacity_raw.isdigit() and int(capacity_raw) > 0 else 5

        group_repo.create_group_session(
            session["user_id"], title, description, skill_id, capacity, scheduled_at
        )
        flash("Your group session was created.", "success")
        return redirect(url_for("group.my_group_sessions"))

    all_skills = user_repo.get_all_skills()
    return render_template("dashboard/group_create.html", all_skills=all_skills)


@login_required
def group_detail(session_id):
    """View one group session, its details and participants."""
    group = group_repo.get_group_session_by_id(session_id)
    if not group:
        abort(404)
    participants = group_repo.get_participants(session_id)
    joined = group_repo.has_joined(session_id, session.get("user_id"))
    is_full = group["joined_count"] >= group["capacity"]
    return render_template(
        "dashboard/group_detail.html",
        group=group, participants=participants, joined=joined, is_full=is_full,
    )


@login_required
def join_group(session_id):
    """A learner joins a group session, if there is room."""
    if session.get("user_role") != "learner":
        flash("Only learners can join group sessions.", "danger")
        return redirect(url_for("group.group_detail", session_id=session_id))

    group = group_repo.get_group_session_by_id(session_id)
    if not group:
        abort(404)

    if group["joined_count"] >= group["capacity"]:
        flash("This group session is already full.", "danger")
        return redirect(url_for("group.group_detail", session_id=session_id))

    group_repo.join_group_session(session_id, session["user_id"])
    flash("You joined the group session.", "success")
    return redirect(url_for("group.group_detail", session_id=session_id))


@login_required
def leave_group(session_id):
    """A learner leaves a group session they had joined."""
    group_repo.leave_group_session(session_id, session["user_id"])
    flash("You left the group session.", "success")
    return redirect(url_for("group.group_detail", session_id=session_id))


@role_required("mentor")
def remove_group(session_id):
    """A mentor deletes their own group session."""
    group_repo.delete_group_session(session_id, session["user_id"])
    flash("Group session deleted.", "success")
    return redirect(url_for("group.my_group_sessions"))