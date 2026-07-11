from datetime import date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import (
    User,
    StudentProfile,
    PlacementDrive,
    CompanyProfile,
    Application,
)

student = Blueprint("student", __name__)


@student.get("/profile")
@jwt_required()
def get_profile():

    try:

        user = User.query.get(int(get_jwt_identity()))

        if user.role != "student":
            return jsonify({"error": "Unauthorized"}), 403

        profile = StudentProfile.query.filter_by(
            user_id=user.id
        ).first()

        return jsonify({
            "name": user.name,
            "email": user.email,
            "college": profile.college,
            "cgpa": profile.cgpa,
            "skills": profile.skills,
            "resume": profile.resume,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@student.put("/profile")
@jwt_required()
def update_profile():

    try:

        user = User.query.get(int(get_jwt_identity()))

        if user.role != "student":
            return jsonify({"error": "Unauthorized"}), 403

        profile = StudentProfile.query.filter_by(
            user_id=user.id
        ).first()

        data = request.get_json() or {}

        profile.college = data.get(
            "college",
            profile.college,
        )

        profile.cgpa = data.get(
            "cgpa",
            profile.cgpa,
        )

        profile.skills = data.get(
            "skills",
            profile.skills,
        )

        profile.resume = data.get(
            "resume",
            profile.resume,
        )

        db.session.commit()

        return jsonify({
            "message": "Profile updated successfully"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.get("/drives")
@jwt_required()
def get_drives():

    try:

        user = User.query.get(int(get_jwt_identity()))

        if user.role != "student":
            return jsonify({"error": "Unauthorized"}), 403

        today = date.today()

        drives = PlacementDrive.query.filter(
            PlacementDrive.deadline >= today
        ).all()

        result = []

        for d in drives:

            company = CompanyProfile.query.get(d.company_id)

            result.append({
                "id": d.id,
                "company": company.company_name,
                "title": d.title,
                "package": d.package,
                "location": d.location,
                "deadline": d.deadline,
                "eligibility": d.eligibility,
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@student.post("/apply/<int:drive_id>")
@jwt_required()
def apply(drive_id):

    try:

        user = User.query.get(int(get_jwt_identity()))

        if user.role != "student":
            return jsonify({"error": "Unauthorized"}), 403

        student_profile = StudentProfile.query.filter_by(
            user_id=user.id
        ).first()

        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return jsonify({
                "error": "Drive not found"
            }), 404

        already = Application.query.filter_by(
            student_id=student_profile.id,
            drive_id=drive.id,
        ).first()

        if already:
            return jsonify({
                "error": "Already applied"
            }), 400

        application = Application(
            student_id=student_profile.id,
            drive_id=drive.id,
        )

        db.session.add(application)
        db.session.commit()

        return jsonify({
            "message": "Applied successfully"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@student.get("/applications")
@jwt_required()
def my_applications():

    try:

        user = User.query.get(int(get_jwt_identity()))

        if user.role != "student":
            return jsonify({"error": "Unauthorized"}), 403

        student_profile = StudentProfile.query.filter_by(
            user_id=user.id
        ).first()

        applications = Application.query.filter_by(
            student_id=student_profile.id
        ).all()

        result = []

        for app in applications:

            drive = PlacementDrive.query.get(app.drive_id)

            company = CompanyProfile.query.get(
                drive.company_id
            )

            result.append({
                "application_id": app.id,
                "company": company.company_name,
                "drive": drive.title,
                "status": app.status,
                "applied_at": app.applied_at,
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
