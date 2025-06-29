# Flask GraphQL Blog API

A modern blog API built with Flask and GraphQL using Strawberry.

## Features

- GraphQL API with Strawberry
- JWT Authentication
- Blog post management
- UserModel management
- GraphQL Playground
- Docker support

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd flask-graphql-blog-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 2. Environment Setup

Copy `.example.env` and update with your settings:

```bash
cp .example.env .env
# Edit .env with your configuration
```

### 3. Initialize Database

```bash
python setup_db.py
```

This creates the database and adds sample data:

- Admin user: `admin` / `admin123`
- Author user: `johndoe` / `password123`
- Sample blog posts

### 4. Run the Application

```bash
python app.py
```

Visit http://localhost:5000/api/graphql for the GraphQL Playground.

## API Usage

### Authentication

First, login to get an access token:

```graphql
mutation {
  login(loginInput: { username: "admin", password: "admin123" }) {
    accessToken
    user {
      id
      username
      fullName
    }
  }
}
```

### Query Posts

```graphql
query {
  posts {
    id
    title
    excerpt
    isPublished
    author {
      username
      fullName
    }
  }
}
```

### Create a PostModel

Include the JWT token in the Authorization header: `Bearer <your-token>`

```graphql
mutation {
  createPost(
    postInput: {
      title: "My New PostModel"
      content: "This is the content of my post..."
      isPublished: true
    }
  ) {
    id
    title
    slug
    author {
      username
    }
  }
}
```

### Search Posts

```graphql
query {
  searchPosts(searchTerm: "GraphQL") {
    id
    title
    excerpt
  }
}
```

![Graphql Login](/docs/images/graphql-api-1.png)

![Graphql Posts](/docs/images/graphql-api-2.png)

## Development

### Project Structure

```
src/
├── app/
│   ├── __init__.py           # App factory
│   ├── config.py             # Configuration
│   ├── extensions.py         # Flask extensions
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # GraphQL types & schema
│   ├── services/             # Business logic
│   └── api/                  # GraphQL endpoints
├── app.py                    # Application entry point
└── setup_db.py              # Database initialization
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check . --fix

# Pre-commit hooks
pre-commit run --all-files
```

### Docker Development

```bash
cd dockerfiles
docker-compose -f docker-compose.dev.yml up --build
```

## Available Queries

- `hello` - Simple test query
- `posts(publishedOnly, limit)` - Get all posts
- `post(id)` - Get post by ID
- `postBySlug(slug)` - Get post by slug
- `postsByAuthor(authorId)` - Get posts by author
- `searchPosts(searchTerm)` - Search posts
- `users` - Get all users
- `user(id)` - Get user by ID
- `me` - Get current user (requires auth)

## Available Mutations

- `register(userInput)` - Register new user
- `login(loginInput)` - Login user
- `createPost(postInput)` - Create post (requires auth)
- `updatePost(id, postInput)` - Update post (requires auth)
- `deletePost(id)` - Delete post (requires auth)
- `publishPost(id)` - Publish post (requires auth)

_This is a portfolio project demonstrating modern Python API development practices._
