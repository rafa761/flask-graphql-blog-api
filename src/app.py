# app.py
from dotenv import load_dotenv

from app import create_app

load_dotenv()

app = create_app()


@app.route("/")
def home():
    """Simple home endpoint."""
    return {"message": "Flask GraphQL Blog API", "status": "running"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
