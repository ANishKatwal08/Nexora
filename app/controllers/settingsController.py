from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import login_required
from app.repository import user_repo


@login_required
def settings():
    return render_template("dashboard/settings.html")


@login_required
def change_password():
    current = request.form.get("current_password", "")
    new = request.form.get("new_password", "")
    confirm = request.form.get("confirm_password", "")

    if not current or not new or not confirm:
        flash("Please fill in all password fields.", "danger")
        return redirect(url_for("settings.settings"))

    if new != confirm:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("settings.settings"))

    if len(new) < 8:
        flash("New password must be at least 8 characters.", "danger")
        return redirect(url_for("settings.settings"))

    stored_hash = user_repo.get_password_hash(session["user_id"])
    if not stored_hash or not check_password_hash(stored_hash, current):
        flash("Your current password is incorrect.", "danger")
        return redirect(url_for("settings.settings"))

    user_repo.update_password(session["user_id"], generate_password_hash(new))
    flash("Password changed successfully.", "success")
    return redirect(url_for("settings.settings"))


@login_required
def delete_account():
    confirm = request.form.get("confirm_delete", "")
    if confirm != "DELETE":
        flash('Type DELETE in the box to confirm account deletion.', "danger")
        return redirect(url_for("settings.settings"))

    user_repo.delete_user(session["user_id"])
    session.clear()
    flash("Your account has been deleted.", "success")
    return redirect(url_for("home"))