## Quick Start

1. **Install dependencies**

   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

2. **Setup database**

   ```bash
   # Configure your database connection in .env
   cp .example.env .env

   # Run migrations
   alembic upgrade head
   ```

3. **Run tests**
   ```bash
   pytest
   ```

_This is a portfolio project demonstrating modern Python API development practices._
