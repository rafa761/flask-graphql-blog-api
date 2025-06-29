# app/extensions.py
"""Flask extensions initialization."""

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()


def init_extensions(app):
    """Initialize Flask extensions with app instance."""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, origins=app.config["CORS_ORIGINS"])
