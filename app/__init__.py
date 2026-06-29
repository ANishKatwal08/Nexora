from flask import Flask, render_template
from config import Config
from app.database import create_tables


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    create_tables()

    # Register blueprints
    from app.routes.authRoutes import bp as auth_bp
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app