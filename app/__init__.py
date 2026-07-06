from flask import Flask, render_template, session, request, abort
from config import Config
from app.database import create_tables, seed_skills
import secrets
import os



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    create_tables()
    seed_skills()

    # Make sure the uploads folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Make a CSRF token available, creating one per session if needed
    def get_csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(32)
        return session["csrf_token"]

    # Expose it to all templates
    app.jinja_env.globals["csrf_token"] = get_csrf_token

    # Check the token on every POST before the request is handled
    @app.before_request
    def csrf_protect():
        if request.method == "POST":
            token = session.get("csrf_token")
            form_token = request.form.get("csrf_token")
            if not token or token != form_token:
                abort(403)
                
    # Provide a notification count to all templates
    @app.context_processor
    def inject_notifications():
        from app.repository import user_repo
        count = 0
        if session.get("user_id"):
            role = session.get("user_role")
            if role == "mentor":
                reqs = user_repo.get_requests_for_mentor(session["user_id"])
                count = sum(1 for r in reqs if r["status"] == "pending")
            elif role == "learner":
                reqs = user_repo.get_requests_for_learner(session["user_id"])
                count = sum(1 for r in reqs if r["status"] in ("confirmed", "declined"))
        return {"notif_count": count}

    # Register blueprints
    from app.routes.authRoutes import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.browseRoutes import bp as browse_bp
    app.register_blueprint(browse_bp)
    
    from app.routes.dashboardRoutes import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.sessionRoutes import bp as session_bp
    app.register_blueprint(session_bp)

    from app.routes.profileRoutes import bp as profile_bp
    app.register_blueprint(profile_bp)

    from app.routes.mentorRoutes import bp as mentor_bp
    app.register_blueprint(mentor_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app