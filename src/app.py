# app.py
from dotenv import load_dotenv
from flask import Flask

from app.config import Config

load_dotenv()


def create_app():
    """Application factory"""

    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/")
    def hello_world():  # put application's code here
        return "Hello World!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
