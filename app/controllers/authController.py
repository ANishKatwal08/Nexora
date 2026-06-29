from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.repository import user_repo


def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    # POST, read the submitted form
    name = request.form.get("name", "").strip()
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()
    role = request.form.get("role", "learner")
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")

    # Validation
    if not name or not username or not email or not password:
        flash("Please fill in all required fields.", "danger")
        return render_template("auth/register.html")

    if len(password) < 8:
        flash("Password must be at least 8 characters.", "danger")
        return render_template("auth/register.html")

    if password != confirm:
        flash("Passwords do not match.", "danger")
        return render_template("auth/register.html")

    if role not in ("learner", "mentor"):
        role = "learner"

    # Check for existing account
    if user_repo.get_user_by_email(email):
        flash("An account with that email already exists.", "danger")
        return render_template("auth/register.html")

    if user_repo.get_user_by_username(username):
        flash("That username is already taken.", "danger")
        return render_template("auth/register.html")

    # Hash the password, then store
    password_hash = generate_password_hash(password)
    phone_value = phone if phone else None

    user_repo.create_user(name, username, email, phone_value, password_hash, role)

    flash("Account created. You can now log in.", "success")
    return redirect(url_for("auth.login"))

def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    # POST, read the form
    identifier = request.form.get("identifier", "").strip()
    password = request.form.get("password", "")

    if not identifier or not password:
        flash("Please enter your login details and password.", "danger")
        return render_template("auth/login.html")

    user = user_repo.get_user_by_identifier(identifier)

    # Same message whether the user is missing or the password is wrong
    if not user or not check_password_hash(user["password_hash"], password):
        flash("Invalid login details.", "danger")
        return render_template("auth/login.html")

    if not user["is_active"]:
        flash("This account has been deactivated.", "danger")
        return render_template("auth/login.html")

    # Start the session
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_role"] = user["role"]

    flash("Welcome back, " + user["name"] + ".", "success")
    return redirect(url_for("home"))


def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))