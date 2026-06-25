from flask import Flask
from config import Config
from app.database import create_tables


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure database tables exist on startup
    create_tables()

    @app.route("/")
    def home():
        return "Nexora is connected and running!"

    return app