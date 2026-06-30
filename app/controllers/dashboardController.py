from flask import render_template, session
from app.auth import login_required


@login_required
def dashboard():
    role = session.get("user_role")
    name = session.get("user_name")

    if role == "mentor":
        return render_template("dashboard/mentor.html", name=name)
    elif role == "admin":
        return render_template("dashboard/admin.html", name=name)
    else:
        return render_template("dashboard/learner.html", name=name)