# app/models/post.py
from datetime import UTC, datetime

from app.extensions import db
from app.models.base import BaseModel


class Post(BaseModel):
    """Blog post model with content and metadata."""

    __tablename__ = "posts"

    # Content fields
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500), nullable=True)

    # SEO and organization
    slug = db.Column(db.String(200), unique=True, nullable=True, index=True)
    tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags

    # Publishing
    is_published = db.Column(db.Boolean, default=False, nullable=False, index=True)
    published_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )

    def __repr__(self):
        return f'<Post "{self.title}">'

    @property
    def tag_list(self):
        """Return tags as a list."""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
        return []

    @tag_list.setter
    def tag_list(self, tags):
        """Set tags from a list."""
        if isinstance(tags, list):
            self.tags = ", ".join(tags)
        else:
            self.tags = tags

    def publish(self):
        """Mark post as published with current timestamp."""

        self.is_published = True
        self.published_at = datetime.now(UTC)
        return self.save()

    def unpublish(self):
        """Mark post as unpublished."""
        self.is_published = False
        self.published_at = None
        return self.save()

    def generate_slug(self):
        """Generate URL-friendly slug from title."""
        import re

        if not self.title:
            return None

        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r"[^\w\s-]", "", self.title.lower())
        slug = re.sub(r"[\s_-]+", "-", slug)
        slug = slug.strip("-")

        # Ensure uniqueness
        base_slug = slug
        counter = 1
        while Post.query.filter_by(slug=slug).filter(Post.id != self.id).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def auto_generate_excerpt(self, max_length=200):
        """Generate excerpt from content if not provided."""
        if self.excerpt:
            return self.excerpt

        if self.content:
            # Remove HTML tags if any and truncate
            import re

            clean_content = re.sub(r"<[^>]+>", "", self.content)

            if len(clean_content) <= max_length:
                return clean_content
            else:
                # Find last complete word within limit
                truncated = clean_content[:max_length]
                last_space = truncated.rfind(" ")
                if last_space > 0:
                    truncated = truncated[:last_space]
                return truncated + "..."

        return None

    @classmethod
    def get_published(cls):
        """Get all published posts ordered by publication date."""
        return cls.query.filter_by(is_published=True).order_by(
            db.desc(cls.published_at)
        )

    @classmethod
    def get_by_author(cls, author_id, published_only=True):
        """Get posts by specific author."""
        query = cls.query.filter_by(author_id=author_id)

        if published_only:
            query = query.filter_by(is_published=True)

        return query.order_by(db.desc(cls.created_at))

    @classmethod
    def search_posts(cls, search_term, published_only=True):
        """Search posts by title or content."""
        query = cls.query.filter(
            db.or_(
                cls.title.contains(search_term),
                cls.content.contains(search_term),
                cls.tags.contains(search_term),
            )
        )

        if published_only:
            query = query.filter_by(is_published=True)

        return query.order_by(db.desc(cls.published_at))

    def save(self):
        """Override save to auto-generate slug and excerpt."""
        if not self.slug:
            self.slug = self.generate_slug()

        if not self.excerpt:
            self.excerpt = self.auto_generate_excerpt()

        return super().save()
