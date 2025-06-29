# src/app/__init__.py
from flask import Flask

from app.api import create_graphql_blueprint
from app.config import Config
from app.extensions import db, init_extensions


def create_app(config_class=Config):
    """Create Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    init_extensions(app)

    # Import models so they're registered with SQLAlchemy
    from app.models import PostModel, UserModel  # noqa: F401

    # Register GraphQL API blueprint
    graphql_bp = create_graphql_blueprint()
    app.register_blueprint(graphql_bp, url_prefix="/api")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
