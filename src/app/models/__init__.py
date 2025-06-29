# src/app/models/__init__.py
from app.models.base import BaseModel
from app.models.post import PostModel
from app.models.user import UserModel

__all__ = ["BaseModel", "UserModel", "PostModel"]
