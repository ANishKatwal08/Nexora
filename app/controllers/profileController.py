import os
from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from app.auth import login_required
from app.repository import user_repo


def _allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@login_required
def profile():
    user = user_repo.get_user_by_id(session["user_id"])
    return render_template("dashboard/profile.html", user=user)


@login_required
def profile_update():
    name = request.form.get("name", "").strip()
    bio = request.form.get("bio", "").strip()

    if not name:
        flash("Name cannot be empty.", "danger")
        return redirect(url_for("profile.profile"))

    user_repo.update_user_profile(session["user_id"], name, bio)
    session["user_name"] = name

    file = request.files.get("photo")
    if file and file.filename:
        if not _allowed_file(file.filename):
            flash("Photo must be a png, jpg, jpeg, or webp.", "danger")
            return redirect(url_for("profile.profile"))

        ext = secure_filename(file.filename).rsplit(".", 1)[1].lower()
        filename = f"user_{session['user_id']}.{ext}"
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        user_repo.update_user_avatar(session["user_id"], filename)
        session["user_avatar"] = filename

    flash("Profile updated.", "success")
    return redirect(url_for("profile.profile"))