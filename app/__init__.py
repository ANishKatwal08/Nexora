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
        from flask import url_for
        items = []
        if session.get("user_id"):
            uid = session["user_id"]
            role = session.get("user_role")

            if role == "mentor":
                reqs = user_repo.get_requests_for_mentor(uid)
                pending = [r for r in reqs if r["status"] == "pending"]
                for r in pending:
                    items.append({
                        "text": r["learner_name"] + " requested a session",
                        "link": url_for("session.mentor_requests"),
                    })
            elif role == "learner":
                reqs = user_repo.get_requests_for_learner(uid)
                answered = [r for r in reqs if r["status"] in ("confirmed", "declined")]
                for r in answered:
                    items.append({
                        "text": r["mentor_name"] + " " + r["status"] + " your session",
                        "link": url_for("session.my_requests"),
                    })

            # Unread messages, for everyone
            senders = user_repo.get_unread_senders(uid)
            for s in senders:
                label = "message" if s["unread"] == 1 else "messages"
                items.append({
                    "text": str(s["unread"]) + " new " + label + " from " + s["name"],
                    "link": url_for("message.conversation", other_id=s["id"]),
                })

        return {"notif_items": items, "notif_count": len(items)}

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

    from app.routes.settingsRoutes import bp as settings_bp
    app.register_blueprint(settings_bp)

    from app.routes.mentorRoutes import bp as mentor_bp
    app.register_blueprint(mentor_bp)

    from app.routes.messageRoutes import bp as message_bp
    app.register_blueprint(message_bp)

    from app.routes.adminRoutes import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    from app.routes.helpRoutes import bp as help_bp
    app.register_blueprint(help_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app