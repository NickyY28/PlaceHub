from flask import Blueprint

from api.auth import auth
# from api.admin import admin
# from api.company import company
# from api.student import student

api_bp = Blueprint("api", __name__, url_prefix="/api")


api_bp.register_blueprint(auth, url_prefix="/auth")
# api_bp.register_blueprint(student, url_prefix="/student")
# api_bp.register_blueprint(company, url_prefix="/company")
# api_bp.register_blueprint(admin, url_prefix="/admin")
