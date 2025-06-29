# src/app/__init__.py
"""Simple Flask app factory."""

from flask import Flask

from app.config import Config
from app.extensions import init_extensions


def create_app(config_class=Config):
    """Create Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    init_extensions(app)

    # Import models so they're registered with SQLAlchemy
    from app.models import Post, User  # noqa: F401

    return app
