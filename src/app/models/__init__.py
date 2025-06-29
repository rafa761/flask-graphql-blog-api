# src/app/models/__init__.py
from app.models.base import BaseModel
from app.models.post import Post
from app.models.user import User

__all__ = ["BaseModel", "User", "Post"]
