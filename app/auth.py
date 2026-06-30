from functools import wraps
from flask import session, redirect, url_for, flash, abort


def login_required(view_func):
    """Block access unless a user is logged in."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "danger")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    """Block access unless the logged in user has one of the allowed roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to continue.", "danger")
                return redirect(url_for("auth.login"))
            if session.get("user_role") not in allowed_roles:
                abort(403)
            return view_func(*args, **kwargs)
        return wrapper
    return decorator