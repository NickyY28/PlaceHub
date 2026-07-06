from flask import Flask, jsonify

from config import Config
from extensions import db
from models import ensure_sqlite_dir, create_all_tables


def create_app(config_object: type = Config) -> Flask:

    app = Flask(__name__)
    app.config.from_object(config_object)

    # Ensure SQLite directory exists before initializing extensions
    ensure_sqlite_dir(app.config.get("SQLALCHEMY_DATABASE_URI", ""))

    # Init Extensions
    db.init_app(app)

    @app.route("/", methods=["GET"])
    def root():
        return jsonify({"message": "Welcome to the PlaceHub API!"})

    with app.app_context():
        create_all_tables()  # Create all tables in the database

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
