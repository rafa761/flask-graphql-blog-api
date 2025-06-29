# setup_db.py

"""Database setup for development."""

from app import create_app
from app.extensions import db
from app.models import Post, User

app = create_app()


def setup_database():
    """Create tables and add sample data."""
    with app.app_context():
        # Create tables
        db.create_all()
        print("Database tables created")

        # Check if data already exists
        if User.query.first():
            print("Database already has data, skipping seed")
            return

        # Create sample users
        admin = User.create_user(
            username="admin",
            email="admin@example.com",
            password="admin123",
            first_name="John",
            last_name="Doe",
        )

        # Create sample posts
        post1 = Post(
            title="Welcome to My Blog",
            content="This is my first blog post using GraphQL!",
            author_id=admin.id,
            is_published=True,
        )
        post1.save()

        post2 = Post(
            title="Learning GraphQL",
            content="GraphQL is amazing for building APIs...",
            author_id=admin.id,
            is_published=False,
        )
        post2.save()

        print(f"Created user: {admin.username}")
        print(f"Created {Post.query.count()} posts")
        print("Database setup complete!")


if __name__ == "__main__":
    setup_database()
