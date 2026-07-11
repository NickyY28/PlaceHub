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

    data = {
        "users": [],
        "companies": [],
        "students": [],
        "drives": [],
        "applications": [],
    }

    users = User.query.all()

    companies = CompanyProfile.query.options(
        joinedload(CompanyProfile.user)
    ).all()

    students = StudentProfile.query.options(
        joinedload(StudentProfile.user)
    ).all()

    drives = PlacementDrive.query.options(
        joinedload(PlacementDrive.company)
    ).all()

    applications = Application.query.options(
        joinedload(Application.student).joinedload(StudentProfile.user),
        joinedload(Application.drive),
    ).all()

    data["users"] = [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "is_blocked": u.is_blocked,
        }
        for u in users
    ]

    data["companies"] = [
        {
            "id": c.id,
            "company_name": c.company_name,
            "email": c.user.email,
            "website": c.website,
            "location": c.location,
        }
        for c in companies
    ]

    data["students"] = [
        {
            "id": s.id,
            "name": s.user.name,
            "email": s.user.email,
            "college": s.college,
            "cgpa": s.cgpa,
            "skills": s.skills,
        }
        for s in students
    ]

    data["drives"] = [
        {
            "id": d.id,
            "company": d.company.company_name,
            "title": d.title,
            "package": d.package,
            "deadline": d.deadline,
        }
        for d in drives
    ]

    data["applications"] = [
        {
            "id": a.id,
            "student_name": a.student.user.name,
            "student_email": a.student.user.email,
            "drive_title": a.drive.title,
            "status": a.status,
            "applied_at": a.applied_at,
        }
        for a in applications
    ]

    return jsonify(data)


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
