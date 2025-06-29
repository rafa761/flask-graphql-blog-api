# app/schemas/schema.py
import strawberry
from flask_jwt_extended import jwt_required
from strawberry.types import Info

from app.models import UserModel
from app.schemas.types import (
    AuthPayloadGType,
    LoginGInput,
    MessageResponseGType,
    PostGInput,
    PostGType,
    UserGInput,
    UserGType,
    convert_post_model,
    convert_user_model,
)
from app.services.auth_service import AuthService
from app.services.post_service import PostService


@strawberry.type
class QueryGType:
    """GraphQL queries."""

    @strawberry.field()
    def hello(self) -> str:
        """Simple hello world query."""
        return "Hello from GraphQL Blog API!"

    @strawberry.field()
    def posts(
        self, published_only: bool = True, limit: int | None = None
    ) -> list[PostGType]:
        """Get all blog posts."""
        posts = PostService.get_all_posts(published_only=published_only, limit=limit)
        return [convert_post_model(post) for post in posts]

    @strawberry.field()
    def post(self, id: int, published_only: bool = True) -> PostGType | None:
        """Get a single post by ID."""
        post = PostService.get_post_by_id(id, published_only=published_only)
        return convert_post_model(post) if post else None

    @strawberry.field()
    def post_by_slug(self, slug: str, published_only: bool = True) -> PostGType | None:
        """Get a single post by slug."""
        post = PostService.get_post_by_slug(slug, published_only=published_only)
        return convert_post_model(post) if post else None

    @strawberry.field()
    def posts_by_author(
        self, author_id: int, published_only: bool = True
    ) -> list[PostGType]:
        """Get posts by a specific author."""
        posts = PostService.get_posts_by_author(
            author_id, published_only=published_only
        )
        return [convert_post_model(post) for post in posts]

    @strawberry.field()
    def search_posts(
        self, search_term: str, published_only: bool = True
    ) -> list[PostGType]:
        """Search posts by title, content, or tags."""
        posts = PostService.search_posts(search_term, published_only=published_only)
        return [convert_post_model(post) for post in posts]

    @strawberry.field()
    def users(self) -> list[UserGType]:
        """Get all users."""
        users = UserModel.query.filter_by(is_active=True).all()
        return [convert_user_model(user) for user in users]

    @strawberry.field()
    def user(self, id: int) -> UserGType | None:
        """Get a single user by ID."""
        user = UserModel.query.filter_by(id=id, is_active=True).first()
        return convert_user_model(user) if user else None

    @strawberry.field()
    def me(self, info: Info) -> UserGType | None:
        """Get current authenticated user."""
        current_user = AuthService.get_current_user()
        return convert_user_model(current_user) if current_user else None


@strawberry.type
class MutationGType:
    """GraphQL mutations"""

    def register(self, user_input: UserGInput) -> AuthPayloadGType:
        """Register a new user."""
        result = AuthService.register_user(
            username=user_input.username,
            email=user_input.email,
            password=user_input.password,
            first_name=user_input.first_name,
            last_name=user_input.last_name,
            bio=user_input.bio,
        )

        if result["error"]:
            raise Exception(result["error"])

        # Generate access token for new user
        auth_result = AuthService.authenticate_user(
            user_input.username, user_input.password
        )

        if auth_result["error"]:
            raise Exception(auth_result["error"])

        return AuthPayloadGType(
            access_token=auth_result["token"],
            user=convert_user_model(auth_result["user"]),
        )

    @strawberry.mutation()
    def login(self, login_input: LoginGInput) -> AuthPayloadGType:
        """Authenticate user and return access token."""
        result = AuthService.authenticate_user(
            login_input.username, login_input.password
        )

        if result["error"]:
            raise Exception(result["error"])

        return AuthPayloadGType(
            access_token=result["token"],
            user=convert_user_model(result["user"]),
        )

    @strawberry.mutation()
    @jwt_required()
    def create_post(self, post_input: PostGInput) -> PostGType:
        """Create a new blog post."""
        current_user = AuthService.get_current_user()
        if not current_user:
            raise Exception("Authentication required")

        result = PostService.create_post(
            title=post_input.title,
            content=post_input.content,
            author_id=current_user.id,
            excerpt=post_input.excerpt,
            tags=post_input.tags,
            is_published=post_input.is_published or False,
        )

        if result["error"]:
            raise Exception(result["error"])

        return convert_post_model(result["post"])

    @strawberry.mutation()
    @jwt_required()
    def update_post(self, id: int, post_input: PostGInput) -> PostGType:
        """Update an existing post."""
        current_user = AuthService.get_current_user()
        if not current_user:
            raise Exception("Authentication required")

        # Build update data
        update_data = {}
        if post_input.title:
            update_data["title"] = post_input.title
        if post_input.content:
            update_data["content"] = post_input.content
        if post_input.excerpt is not None:
            update_data["excerpt"] = post_input.excerpt
        if post_input.tags is not None:
            update_data["tags"] = post_input.tags
        if post_input.is_published is not None:
            update_data["is_published"] = post_input.is_published

        result = PostService.update_post(id, current_user.id, **update_data)

        if result["error"]:
            raise Exception(result["error"])

        return convert_post_model(result["post"])

    @strawberry.mutation()
    @jwt_required()
    def delete_post(self, id: int) -> MessageResponseGType:
        """Delete a blog post."""
        current_user = AuthService.get_current_user()
        if not current_user:
            raise Exception("Authentication required")

        result = PostService.delete_post(id, current_user.id)

        if result["error"]:
            raise Exception(result["error"])

        return MessageResponseGType(message="Post deleted successfully")

    @strawberry.mutation()
    @jwt_required()
    def publish_post(self, id: int) -> PostGType:
        """Publish a blog post."""
        current_user = AuthService.get_current_user()
        if not current_user:
            raise Exception("Authentication required")

        result = PostService.publish_post(id, current_user.id)

        if result["error"]:
            raise Exception(result["error"])

        return convert_post_model(result["post"])


# Create the schema
schema = strawberry.Schema(query=QueryGType, mutation=MutationGType)
