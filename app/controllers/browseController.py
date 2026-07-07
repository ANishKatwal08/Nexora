
from flask import render_template, request, redirect, url_for, flash
from app.repository import user_repo

def browse():
    # Multi select values come as lists
    selected_skills = request.args.getlist("skill")
    selected_categories = request.args.getlist("category")
    search = request.args.get("q", "").strip()

    all_skills = user_repo.get_all_skills()
    categories = sorted({s["category"] for s in all_skills if s["category"]})

    # Start with all mentors, then attach their skills
    sort = request.args.get("sort", "rating")
    mentors = user_repo.get_all_mentors(sort)
    for mentor in mentors:
        mentor["skills"] = user_repo.get_mentor_skills(mentor["id"])

    # Filter by skills, keep mentors who teach any of the ticked skills
    if selected_skills:
        skill_ids = [int(s) for s in selected_skills]
        mentors = [
            m for m in mentors
            if any(sk["id"] in skill_ids for sk in m["skills"])
        ]

    # Filter by categories, keep mentors who teach in any ticked category
    if selected_categories:
        mentors = [
            m for m in mentors
            if any(sk["category"] in selected_categories for sk in m["skills"])
        ]

    # Filter by name search
    if search:
        mentors = [
            m for m in mentors
            if search.lower() in m["name"].lower()
        ]

    # Turn selected skill ids into ints for the template to compare
    selected_skill_ids = [int(s) for s in selected_skills]

    return render_template(
        "browse.html",
        mentors=mentors,
        all_skills=all_skills,
        categories=categories,
        selected_skill_ids=selected_skill_ids,
        selected_categories=selected_categories,
        search=search,
    )

def mentor_detail(mentor_id):
    mentor = user_repo.get_user_by_id(mentor_id)
    if not mentor or mentor["role"] != "mentor":
        flash("That mentor was not found.", "danger")
        return redirect(url_for("browse.browse"))

    skills = user_repo.get_mentor_skills(mentor_id)
    reviews = user_repo.get_feedback_for_mentor(mentor_id)

    return render_template(
        "mentor_detail.html",
        mentor=mentor,
        skills=skills,
        reviews=reviews,
    )