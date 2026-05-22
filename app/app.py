import os

from flask import Flask
from app.database import db
from app.routes import main
import time
import sqlalchemy.exc


def create_app():
    app = Flask(__name__)

    postgres_host = os.getenv("POSTGRES_HOST")

    if postgres_host:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql://{os.getenv('POSTGRES_USER')}:"
            f"{os.getenv('POSTGRES_PASSWORD')}@"
            f"{postgres_host}:5432/"
            f"{os.getenv('POSTGRES_DB')}"
        )
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        for i in range(10):
            try:
                db.create_all()
                break
            except sqlalchemy.exc.OperationalError:
                print("DB not ready, retrying...")
                time.sleep(2)
    return app
