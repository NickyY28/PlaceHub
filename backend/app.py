from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db, jwt, celery
from models import ensure_sqlite_dir, create_all_tables
from seed import ensure_seed_data


def create_app(config_object: type = Config) -> Flask:

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_object)

    # Ensure SQLite directory exists before initializing extensions
    ensure_sqlite_dir(app.config.get("SQLALCHEMY_DATABASE_URI", ""))

    # Init Extensions
    db.init_app(app)
    jwt.init_app(app)

    # Celery Configuration
    celery.conf.update(app.config["CELERY"])

    class FlaskTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = FlaskTask

    # Register Celery Tasks
    import tasks.student_tasks
    import tasks.admin_tasks

    # Register API blueprints
    from api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/")
    def root():
        return jsonify({"message": "Welcome to the PlaceHub API!"})

   # Create DB and seed minimal data
    with app.app_context():
        create_all_tables()
        ensure_seed_data()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
