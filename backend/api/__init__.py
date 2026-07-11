from flask import Blueprint

from api.auth import auth
from api.company import company
from api.drive import drive
from api.student import student
from api.application import application
from api.admin import admin


api_bp = Blueprint("api", __name__, url_prefix="/api")


api_bp.register_blueprint(auth, url_prefix="/auth")
api_bp.register_blueprint(company, url_prefix="/company")
api_bp.register_blueprint(drive, url_prefix="/drives")
api_bp.register_blueprint(student, url_prefix="/student")
api_bp.register_blueprint(application, url_prefix="/applications")
api_bp.register_blueprint(admin, url_prefix="/admin")
