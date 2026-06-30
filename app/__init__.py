from flask import Flask, render_template, session, request, abort
from config import Config
from app.database import create_tables
import secrets


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    create_tables()

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

    # Register blueprints
    from app.routes.authRoutes import bp as auth_bp
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app