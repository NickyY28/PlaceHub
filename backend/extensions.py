from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

db = SQLAlchemy()
jwt = JWTManager()
celery = Celery(__name__)
