# app/services/post_service.py

from app.extensions import db
from app.models import PostModel, UserModel


class PostService:
    """Service for blog post operations."""

    @staticmethod
    def get_all_posts(
        published_only: bool = True, limit: int | None = None
    ) -> list[PostModel]:
        """Get all posts with optional filtering."""
        query = (
            PostModel.get_published()
            if published_only
            else PostModel.query.order_by(db.desc(PostModel.created_at))
        )

        if limit:
            query = query.limit(limit)

        return query.all()

    @staticmethod
    def get_post_by_id(post_id: int, published_only: bool = True) -> PostModel | None:
        """Get a single post by ID."""
        query = PostModel.query.filter_by(id=post_id)

        if published_only:
            query = query.filter_by(is_published=True)

        return query.first()

    @staticmethod
    def get_post_by_slug(slug: str, published_only: bool = True) -> PostModel | None:
        """Get a single post by slug."""
        query = PostModel.query.filter_by(slug=slug)

        if published_only:
            query = query.filter_by(is_published=True)

        return query.first()

    @staticmethod
    def get_posts_by_author(
        author_id: int, published_only: bool = True
    ) -> list[PostModel]:
        """Get posts by specific author."""
        return PostModel.get_by_author(author_id, published_only).all()

    @staticmethod
    def create_post(title: str, content: str, author_id: int, **kwargs) -> dict:
        """Create a new blog post."""
        try:
            # Verify author exists
            author = UserModel.query.get(author_id)
            if not author:
                return {"error": "Author not found", "post": None}

            post = PostModel(
                title=title, content=content, author_id=author_id, **kwargs
            )

            post.save()
            return {"error": None, "post": post}

        except Exception as e:
            db.session.rollback()
            return {"error": str(e), "post": None}

    @staticmethod
    def update_post(post_id: int, user_id: int, **kwargs) -> dict:
        """Update an existing post."""
        try:
            post = PostModel.query.get(post_id)
            if not post:
                return {"error": "Post not found", "post": None}

            # Check if user owns the post
            if post.author_id != user_id:
                return {"error": "Not authorized to edit this post", "post": None}

            # Update post fields
            for key, value in kwargs.items():
                if hasattr(post, key) and value is not None:
                    setattr(post, key, value)

            post.save()
            return {"error": None, "post": post}

        except Exception as e:
            db.session.rollback()
            return {"error": str(e), "post": None}

    @staticmethod
    def delete_post(post_id: int, user_id: int) -> dict:
        """Delete a post."""
        try:
            post = PostModel.query.get(post_id)
            if not post:
                return {"error": "Post not found", "success": False}

            # Check if user owns the post
            if post.author_id != user_id:
                return {"error": "Not authorized to delete this post", "success": False}

            post.delete()
            return {"error": None, "success": True}

        except Exception as e:
            db.session.rollback()
            return {"error": str(e), "success": False}

    @staticmethod
    def publish_post(post_id: int, user_id: int) -> dict:
        """Publish a post."""
        try:
            post = PostModel.query.get(post_id)
            if not post:
                return {"error": "Post not found", "post": None}

            # Check if user owns the post
            if post.author_id != user_id:
                return {"error": "Not authorized to publish this post", "post": None}

            post.publish()
            return {"error": None, "post": post}

        except Exception as e:
            db.session.rollback()
            return {"error": str(e), "post": None}

    @staticmethod
    def search_posts(search_term: str, published_only: bool = True) -> list[PostModel]:
        """Search posts by title, content, or tags."""
        return PostModel.search_posts(search_term, published_only).all()
