from flask import Flask
from app.routes.task_routes import task_bp
from app.db.db import db
from app.models.task import Task
from app import create_app
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

import os
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")


db.init_app(app)

app.register_blueprint(task_bp)

@app.route("/api/health")
def health():
    logger.info("Health check called")
    return {"status": "ok"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000)
