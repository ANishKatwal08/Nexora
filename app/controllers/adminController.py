from flask import render_template, request, redirect, url_for, flash, session
from app.auth import role_required
from app.repository import user_repo


@role_required("admin")
def admin_users():
    search = request.args.get("q", "").strip()
    stats = user_repo.get_platform_stats()
    users = user_repo.get_all_users(search)
    return render_template("dashboard/admin_users.html", stats=stats, users=users, search=search)


@role_required("admin")
def toggle_user(user_id):
    user = user_repo.get_user_by_id(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin.admin_users"))

    # Do not let an admin deactivate their own account
    if user_id == session["user_id"]:
        flash("You cannot deactivate your own account.", "danger")
        return redirect(url_for("admin.admin_users"))

    new_state = not user["is_active"]
    user_repo.set_user_active(user_id, new_state)
    flash("User " + ("activated" if new_state else "deactivated") + ".", "success")
    return redirect(url_for("admin.admin_users"))