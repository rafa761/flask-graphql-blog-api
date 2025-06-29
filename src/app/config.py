# app/config.py
import os
from datetime import timedelta


class Config:
    """Base configuration with common settings."""

    # Flask Core Settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///blog.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get("JWT_ACCESS_TOKEN_HOURS", 24))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_REFRESH_TOKEN_DAYS", 30))
    )

    # CORS Configuration
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")

    # GraphQL Configuration
    GRAPHQL_PLAYGROUND = os.environ.get("GRAPHQL_PLAYGROUND", "true").lower() == "true"
