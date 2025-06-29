# app/api/graphql_view.py
from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request
from strawberry.flask.views import GraphQLView

from app.schemas.schema import schema


class CustomGraphQLView(GraphQLView):
    """Custom GraphQL view with authentication context."""

    def get_context(self, request, response=None):
        """Add authentication context to GraphQL requests."""
        context = super().get_context(request, response)

        # Try to verify JWT token if present
        try:
            verify_jwt_in_request(optional=True)
        except Exception:
            pass  # Continue without authentication

        return context


def create_graphql_blueprint():
    """Create GraphQL API blueprint."""
    api_bp = Blueprint("api", __name__)

    # GraphQL endpoint
    graphql_view = CustomGraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,  # Enable GraphiQL playground in development
    )

    # Add GraphQL route
    api_bp.add_url_rule("/graphql", view_func=graphql_view, methods=["GET", "POST"])

    @api_bp.route("/health")
    def health_check():
        """Simple health check endpoint."""
        return {"status": "healthy", "service": "GraphQL Blog API"}

    return api_bp
