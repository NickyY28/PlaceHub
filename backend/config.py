import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()  # Load environment variables from .env file


def _default_sqlite_uri():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "instance"))
    os.makedirs(base, exist_ok=True)
    return f"sqlite:///{os.path.join(base, 'PlaceHub.db')}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI", _default_sqlite_uri())
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get(
        "JWT_ACCESS_TOKEN_EXPIRES", timedelta(hours=8))

    # Redis
    REDIS_URL = os.environ.get(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    # Celery
    CELERY = {
        "broker_url": REDIS_URL,
        "result_backend": REDIS_URL,
        "task_ignore_result": False,
    }
