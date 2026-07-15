from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models import (
    User,
    CompanyProfile,
    StudentProfile,
    PlacementDrive,
    Application,
)
from sqlalchemy.orm import joinedload

from utils.decorators import admin_required

admin = Blueprint("admin", __name__)


@admin.get("/dashboard")
@jwt_required()
@admin_required
def dashboard(user):

    return jsonify({
        "total_users": User.query.count(),
        "total_students": User.query.filter_by(role="student").count(),
        "total_companies": CompanyProfile.query.count(),
        "total_applications": Application.query.count(),
        "total_drives": PlacementDrive.query.count(),

    })


@admin.get("/users")
@jwt_required()
@admin_required
def get_users(user):
    try:
        return jsonify({
            "users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "email": u.email,
                    "role": u.role,
                    "is_blocked": u.is_blocked,
                }
                for u in User.query.all()
            ]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin.get("/companies")
@jwt_required()
@admin_required
def get_companies(user):
    try:
        return jsonify({
            "companies": [
                {
                    "id": c.id,
                    "company_name": c.company_name,
                    "email": c.user.email,
                    "website": c.website,
                    "location": c.location,
                    "description": c.description,
                    "user_id": c.user.id,
                    "is_blocked": c.user.is_blocked,

                }
                for c in CompanyProfile.query.options(joinedload(CompanyProfile.user)).all()
            ]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin.get("/students")
@jwt_required()
@admin_required
def get_students(user):
    try:
        return jsonify({
            "students": [
                {
                    "id": s.id,
                    "name": s.user.name,
                    "email": s.user.email,
                    "is_blocked": s.user.is_blocked,
                    "college": s.college,
                    "cgpa": s.cgpa,
                    "skills": s.skills

                }
                for s in StudentProfile.query.options(joinedload(StudentProfile.user)).all()
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin.get("/drives")
@jwt_required()
@admin_required
def get_drives(user):
    try:
        return jsonify({
            "drives": [
                {
                    "id": d.id,
                    "company": d.company.company_name,
                    "title": d.title,
                    "package": d.package,
                    "deadline": d.deadline,
                }
                for d in PlacementDrive.query.options(joinedload(PlacementDrive.company)).all()
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin.get("/applications")
@jwt_required()
@admin_required
def get_applications(user):
    try:
        return jsonify({
            "applications": [
                {
                    "id": a.id,
                    "student": a.student.user.name,
                    "drive": a.drive.title,
                    "status": a.status,
                    "applied_at": a.applied_at,
                }
                for a in Application.query.options(joinedload(Application.student), joinedload(Application.drive)).all()
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin.patch("/users/<int:user_id>/block")
@jwt_required()
@admin_required
def block_user(user, user_id):

    u = User.query.get(user_id)

    if not u:
        return jsonify({"error": "User not found"}), 404

    u.is_blocked = True

    db.session.commit()

    return jsonify({
        "message": "User blocked successfully"
    })


@admin.patch("/users/<int:user_id>/unblock")
@jwt_required()
@admin_required
def unblock_user(user, user_id):

    u = User.query.get(user_id)

    if not u:
        return jsonify({"error": "User not found"}), 404

    u.is_blocked = False

    db.session.commit()

    return jsonify({
        "message": "User unblocked successfully"
    })


@admin.delete("/users/<int:user_id>")
@jwt_required()
@admin_required
def delete_user(user, user_id):

    u = User.query.get(user_id)

    if not u:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(u)
    db.session.commit()

    return jsonify({
        "message": "User deleted successfully"
    })


@admin.delete("/drives/<int:drive_id>")
@jwt_required()
@admin_required
def delete_drive(user, drive_id):

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    db.session.delete(drive)
    db.session.commit()

    return jsonify({
        "message": "Drive deleted successfully"
    })
