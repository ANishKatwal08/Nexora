from flask import render_template, request, redirect, url_for, flash, session
from app.auth import login_required
from app.repository import mentor_repo


@login_required
def mentor_profile():
    if session.get("user_role") != "mentor":
        flash("Only mentors can access that page.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    profile = mentor_repo.get_profile_by_user(session["user_id"])
    return render_template("dashboard/mentor_profile.html", profile=profile)


@login_required
def mentor_profile_save():
    if session.get("user_role") != "mentor":
        flash("Only mentors can do that.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    profession = request.form.get("profession", "").strip()
    headline = request.form.get("headline", "").strip()
    bio = request.form.get("bio", "").strip()
    skills = request.form.get("skills", "").strip()
    years = request.form.get("years_experience", "0").strip()
    rate = request.form.get("hourly_rate", "0").strip()

    if not profession:
        flash("Profession is required.", "danger")
        return redirect(url_for("mentor.mentor_profile"))

    try:
        years = int(years) if years else 0
        rate = float(rate) if rate else 0
    except ValueError:
        flash("Years and rate must be numbers.", "danger")
        return redirect(url_for("mentor.mentor_profile"))

    if years < 0 or rate < 0:
        flash("Years and rate cannot be negative.", "danger")
        return redirect(url_for("mentor.mentor_profile"))

    existing = mentor_repo.get_profile_by_user(session["user_id"])
    if existing:
        mentor_repo.update_profile(session["user_id"], profession, headline, bio, skills, years, rate)
        flash("Mentor profile updated.", "success")
    else:
        mentor_repo.create_profile(session["user_id"], profession, headline, bio, skills, years, rate)
        flash("Mentor profile created.", "success")

    return redirect(url_for("mentor.mentor_profile"))


@login_required
def mentor_profile_delete():
    if session.get("user_role") != "mentor":
        flash("Only mentors can do that.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    mentor_repo.delete_profile(session["user_id"])
    flash("Mentor profile removed.", "success")
    return redirect(url_for("mentor.mentor_profile"))