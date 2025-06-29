# setup_db.py
"""Database initialization script with sample data."""

from dotenv import load_dotenv

from app import create_app
from app.extensions import db
from app.models import PostModel, UserModel

# Load environment variables
load_dotenv()


def create_sample_data():
    """Create sample users and posts for testing."""

    # Create sample users
    admin_user = UserModel.create_user(
        username="admin",
        email="admin@example.com",
        password="admin123",
        first_name="Admin",
        last_name="User",
        bio="Blog administrator and main author.",
    )

    author_user = UserModel.create_user(
        username="johndoe",
        email="john@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
        bio="Passionate writer and technology enthusiast.",
    )

    print(f"✅ Created users: {admin_user.username}, {author_user.username}")

    # Create sample posts
    posts_data = [
        {
            "title": "Welcome to Our Blog",
            "content": """# Welcome to Our Blog

This is our first blog post! We're excited to share our thoughts and insights with you.

## What You Can Expect

- Technical tutorials
- Industry insights
- Personal experiences
- And much more!

Stay tuned for regular updates.""",
            "tags": "welcome, introduction, blog",
            "is_published": True,
            "author_id": admin_user.id,
        },
        {
            "title": "Getting Started with GraphQL",
            "content": """# Getting Started with GraphQL

GraphQL is a powerful query language for APIs that provides a more efficient, powerful and flexible alternative to REST.

## Key Benefits

1. **Single endpoint** - One URL for all data needs
2. **Request exactly what you need** - No over-fetching
3. **Strong type system** - Better developer experience
4. **Real-time subscriptions** - Live data updates

## Basic Query Example

```graphql
query {
  posts {
    title
    author {
      username
    }
  }
}
```

This query fetches all posts with their titles and author usernames.""",
            "tags": "graphql, api, tutorial",
            "is_published": True,
            "author_id": author_user.id,
        },
        {
            "title": "Draft: Upcoming Features",
            "content": """# Upcoming Features

We're working on some exciting new features:

- Comment system
- User profiles
- Post categories
- Search functionality

This post is still in draft mode.""",
            "tags": "features, roadmap",
            "is_published": False,
            "author_id": admin_user.id,
        },
    ]

    for post_data in posts_data:
        post = PostModel(**post_data)
        post.save()
        status = "Published" if post.is_published else "📄 Draft"
        print(f"{status}: {post.title} (by {post.author.username})")

    print(f"\nCreated {len(posts_data)} sample posts")


def main():
    """Initialize database with sample data."""
    app = create_app()

    with app.app_context():
        print("Setting up database...")

        # Create all tables
        db.create_all()
        print("Database tables created")

        # Check if data already exists
        if UserModel.query.first():
            print("Database already contains data. Skipping sample data creation.")
            print("To reset, delete the database file and run this script again.")
            return

        # Create sample data
        print("📝 Creating sample data...")
        create_sample_data()

        print("\n Database setup complete!")
        print("\n Summary:")
        print(f"   Users: {UserModel.query.count()}")
        print(f"   Posts: {PostModel.query.count()}")
        print(
            f"   Published Posts: {PostModel.query.filter_by(is_published=True).count()}"
        )

        print("\n You can now start the server and test the API!")
        print("   GraphQL Playground: http://localhost:5000/api/graphql")


if __name__ == "__main__":
    main()
