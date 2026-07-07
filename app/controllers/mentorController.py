from flask import render_template, request, redirect, url_for, flash, session
from app.auth import role_required
from app.repository import user_repo


@role_required("mentor")
def mentor_profile():
    mentor_id = session["user_id"]
    user = user_repo.get_user_by_id(mentor_id)
    my_skills = user_repo.get_mentor_skills(mentor_id)
    all_skills = user_repo.get_all_skills()

    my_skill_ids = [s["id"] for s in my_skills]
    available = [s for s in all_skills if s["id"] not in my_skill_ids]

    return render_template(
        "dashboard/mentor_profile.html",
        user=user,
        my_skills=my_skills,
        available=available,
    )


@role_required("mentor")
def update_mentor_details():
    profession = request.form.get("profession", "").strip()
    headline = request.form.get("headline", "").strip()
    rate_raw = request.form.get("hourly_rate", "").strip()
    exp_raw = request.form.get("years_experience", "").strip()

    hourly_rate = int(rate_raw) if rate_raw.isdigit() else None
    years_experience = int(exp_raw) if exp_raw.isdigit() else None

    user_repo.update_mentor_details(session["user_id"], profession, headline, hourly_rate, years_experience)
    flash("Profile updated.", "success")
    return redirect(url_for("mentor.mentor_profile"))


@role_required("mentor")
def add_skill():
    skill_id = request.form.get("skill_id")
    if skill_id:
        user_repo.add_mentor_skill(session["user_id"], skill_id)
        flash("Skill added.", "success")
    return redirect(url_for("mentor.mentor_profile"))


@role_required("mentor")
def remove_skill():
    skill_id = request.form.get("skill_id")
    if skill_id:
        user_repo.remove_mentor_skill(session["user_id"], skill_id)
        flash("Skill removed.", "success")
    return redirect(url_for("mentor.mentor_profile"))