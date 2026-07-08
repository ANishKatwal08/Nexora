from flask import render_template, session
from app.auth import login_required
from app.repository import user_repo


@login_required
def dashboard():
    role = session.get("user_role")
    name = session.get("user_name")
    user_id = session.get("user_id")

    if role == "mentor":
        requests = user_repo.get_requests_for_mentor(user_id)
        confirmed = [r for r in requests if r["status"] == "confirmed"]
        completed = [r for r in requests if r["status"] == "completed"]
        bookings = len([r for r in requests if r["status"] in ("confirmed", "completed")])
        user = user_repo.get_user_by_id(user_id)
        rating = user["rating"] if user and user["rating"] and user["rating"] > 0 else None
        upcoming = confirmed
        return render_template(
            "dashboard/mentor.html",
            name=name,
            sessions_hosted=len(completed),
            bookings=bookings,
            rating=rating,
            upcoming=upcoming,
        )

    elif role == "admin":
        stats = user_repo.get_platform_stats()
        return render_template("dashboard/admin.html", name=name, stats=stats)
    else:
        requests = user_repo.get_requests_for_learner(user_id)
        booked = [r for r in requests if r["status"] in ("pending", "confirmed")]
        completed = [r for r in requests if r["status"] == "completed"]
        mentor_ids = {r["mentor_id"] for r in requests}
        upcoming = [r for r in requests if r["status"] == "confirmed"]
        return render_template(
            "dashboard/learner.html",
            name=name,
            booked=len(booked),
            completed=len(completed),
            mentors=len(mentor_ids),
            upcoming=upcoming,
        )