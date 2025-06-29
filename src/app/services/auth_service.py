# app/services/auth_service.py
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import UserModel


class AuthService:
    """Authentication service for user management and JWT tokens."""

    @staticmethod
    def register_user(username: str, email: str, password: str, **kwargs) -> dict:
        """Register a new UserModel."""
        try:
            # Check if user already exists
            if UserModel.find_by_username(username):
                return {"error": "Username already exists", "user": None}

            if UserModel.find_by_email(email):
                return {"error": "Email already exists", "user": None}

            # Create new user
            user = UserModel.create_user(
                username=username, email=email, password=password, **kwargs
            )

            return {"error": None, "user": user}

        except IntegrityError:
            db.session.rollback()
            return {"error": "User creation failed", "user": None}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e), "user": None}

    @staticmethod
    def authenticate_user(username: str, password: str) -> dict:
        """Authenticate user and return access token."""
        try:
            # Find user by username or email
            user = UserModel.find_by_username(username)
            if not user:
                user = UserModel.find_by_email(username)

            if not user:
                return {"error": "User not found", "user": None, "token": None}

            if not UserModel.is_active:
                return {"error": "Account is deactivated", "user": None, "token": None}

            if not UserModel.check_password(password):
                return {"error": "Invalid password", "user": None, "token": None}

            # Create access token
            access_token = create_access_token(identity=UserModel.id)

            return {"error": None, "user": user, "token": access_token}

        except Exception as e:
            return {"error": str(e), "user": None, "token": None}

    @staticmethod
    def get_current_user() -> UserModel | None:
        """Get current user from JWT token."""
        try:
            user_id = get_jwt_identity()
            if user_id:
                return UserModel.query.get(user_id)
            return None
        except Exception:
            return None

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify JWT token and return user info."""
        try:
            decoded = decode_token(token)
            user_id = decoded["sub"]
            user = UserModel.query.get(user_id)

            if not user or not UserModel.is_active:
                return {"error": "Invalid token", "user": None}

            return {"error": None, "user": user}

        except Exception as e:
            return {"error": str(e), "user": None}
