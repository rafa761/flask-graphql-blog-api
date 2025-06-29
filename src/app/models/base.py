# app/models/base.py
from datetime import UTC, datetime

from app.extensions import db


class BaseModel(db.Model):
    """Abstract base model with common fields."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    def save(self):
        """Save instance to database."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Delete instance from database."""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """Update instance with provided kwargs."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = datetime.now(UTC)
        db.session.commit()
        return self

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
