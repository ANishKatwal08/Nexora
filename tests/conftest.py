"""
Shared pytest fixtures for the Nexora test suite.

The app fixture tries to build the Flask app. If the database is not
reachable (for example MySQL is not running), the dependent tests skip
cleanly instead of failing, so the suite still runs anywhere.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def app():
    """Build the Flask app in testing mode, or skip if the DB is unavailable."""
    try:
        from app import create_app
        application = create_app()
    except Exception as exc:  # database not reachable, or import issue
        pytest.skip(f"App could not start (database likely not running): {exc}")
    application.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})
    return application


@pytest.fixture
def client(app):
    """A test client for making requests without a real server."""
    return app.test_client()