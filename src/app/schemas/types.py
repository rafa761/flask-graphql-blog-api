# app/schemas/types.py
from datetime import datetime

import strawberry
from strawberry.types import Info

from app.models import PostModel, UserModel


@strawberry.type
class UserGType:
    """GraphQL User Type"""

    id: int
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    is_active: bool
    created_at: datetime

    @strawberry.field()
    def full_name(self) -> str:
        """User's fill name or username"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.username

    @strawberry.field()
    def post_count(self, info: Info) -> int:
        """Number of posts by this user"""
        return PostModel.query.filter_by(author_id=self.id).count()


@strawberry.type
class PostGType:
    """GraphQL Post Type"""

    id: int
    title: str
    content: str
    excerpt: str | None = None
    slug: str | None = None
    is_published: bool
    published_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    author_id: int

    @strawberry.field()
    def author(self, info: Info) -> UserGType:
        """Post author."""
        author = UserModel.query.get(self.author_id)
        return UserGType(
            id=author.id,
            username=author.username,
            email=author.email,
            first_name=author.first_name,
            last_name=author.last_name,
            bio=author.bio,
            is_active=author.is_active,
            created_at=author.created_at,
        )

    @strawberry.field()
    def tag_list(self) -> list[str]:
        """Post tags as a list."""
        post = PostModel.query.get(self.id)
        return post.tag_list if post else []


@strawberry.input
class UserGInput:
    """Input for creating users"""

    username: str
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None


@strawberry.input
class LoginGInput:
    """Input for user login"""

    username: str
    password: str


@strawberry.input
class PostGInput:
    """Input for creating/updating posts."""

    title: str
    content: str
    excerpt: str | None = None
    tags: str | None = None
    is_published: bool | None = False


@strawberry.type
class AuthPayloadGType:
    """Authentication response payload."""

    access_token: str
    user: UserGType


@strawberry.type
class MessageResponseGType:
    """Simple message response."""

    message: str
    success: bool = True


def convert_user_model(user_model) -> UserGType:
    """Convert SQLAlchemy User model to GraphQL User type."""
    return UserGType(
        id=user_model.id,
        username=user_model.username,
        email=user_model.email,
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        bio=user_model.bio,
        is_active=user_model.is_active,
        created_at=user_model.created_at,
    )


def convert_post_model(post_model) -> PostGType:
    """Convert SQLAlchemy Post model to GraphQL Post type."""
    return PostGType(
        id=post_model.id,
        title=post_model.title,
        content=post_model.content,
        excerpt=post_model.excerpt,
        slug=post_model.slug,
        is_published=post_model.is_published,
        published_at=post_model.published_at,
        created_at=post_model.created_at,
        updated_at=post_model.updated_at,
        author_id=post_model.author_id,
    )
