# app/models/user.py
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.base import BaseModel


class UserModel(BaseModel):
    """UserModel model for authentication and blog authoring."""

    __tablename__ = "users"

    # UserModel identification
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    # Authentication
    password_hash = db.Column(db.String(255), nullable=False)

    # UserModel information
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    posts = db.relationship(
        "Post", backref="author", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<UserModel {self.username}>"

    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches stored hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        """Return user's full name or username if names not provided."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.username

    @property
    def post_count(self):
        """Return number of posts by this user."""
        return self.posts.count()

    def get_recent_posts(self, limit=5):
        """Get user's most recent posts."""
        return self.posts.order_by(db.desc("created_at")).limit(limit).all()

    @classmethod
    def find_by_username(cls, username):
        """Find user by username."""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        """Find user by email."""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        """Create a new user with hashed password."""
        user = cls(username=username, email=email, **kwargs)
        user.set_password(password)
        return user.save()
