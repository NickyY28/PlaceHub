from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from models import User


def company_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = User.query.get(int(get_jwt_identity()))

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role != "company":
            return jsonify({"error": "Unauthorized"}), 403

        return fn(user, *args, **kwargs)

    return wrapper


def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = User.query.get(int(get_jwt_identity()))

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role != "student":
            return jsonify({"error": "Unauthorized"}), 403

        return fn(user, *args, **kwargs)

    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = User.query.get(int(get_jwt_identity()))

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        return fn(user, *args, **kwargs)

    return wrapper
