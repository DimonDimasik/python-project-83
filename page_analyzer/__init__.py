import os
from dotenv import load_dotenv
from flask import Flask


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-dev-key")
    from .app import bp

    app.register_blueprint(bp)
    return app


app = create_app()
__all__ = ["app"]
