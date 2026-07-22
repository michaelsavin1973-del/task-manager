import os

from flask import Flask
from flask_migrate import Migrate
from app.db.db import db

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        database_url = (
            f"postgresql://{os.environ['DB_USER']}:"
            f"{os.environ['DB_PASSWORD']}@"
            f"{os.environ['DB_HOST']}:5432/"
            f"{os.environ['DB_NAME']}"
        )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.task import Task
    from app.routes.task_routes import task_bp

    app.register_blueprint(task_bp)

    return app
