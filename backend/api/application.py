from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import (
    User,
    CompanyProfile,
    StudentProfile,
    PlacementDrive,
    Application,
)

application = Blueprint("application", __name__)


@application.get("")
@jwt_required()
def get_all_applications():
    try:
        user = User.query.get(int(get_jwt_identity()))

        if not user or user.role != "company":
            return jsonify({"error": "Unauthorized"}), 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        drives = PlacementDrive.query.filter_by(company_id=company.id).all()

        result = []

        for drive in drives:

            applications = Application.query.filter_by(
                drive_id=drive.id
            ).all()

            for app in applications:

                student = StudentProfile.query.get(app.student_id)
                student_user = User.query.get(student.user_id)

                result.append({
                    "application_id": app.id,
                    "student_name": student_user.name,
                    "student_email": student_user.email,
                    "college": student.college,
                    "cgpa": student.cgpa,
                    "skills": student.skills,
                    "resume": student.resume,
                    "drive_id": drive.id,
                    "drive_title": drive.title,
                    "status": app.status,
                    "applied_at": app.applied_at,
                })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@application.get("/<int:drive_id>")
@jwt_required()
def get_drive_applications(drive_id):
    try:
        user = User.query.get(int(get_jwt_identity()))

        if not user or user.role != "company":
            return jsonify({"error": "Unauthorized"}), 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        drive = PlacementDrive.query.filter_by(
            id=drive_id,
            company_id=company.id
        ).first()

        if not drive:
            return jsonify({"error": "Drive not found"}), 404

        applications = Application.query.filter_by(
            drive_id=drive.id
        ).all()

        result = []

        for app in applications:

            student = StudentProfile.query.get(app.student_id)
            student_user = User.query.get(student.user_id)

            result.append({
                "application_id": app.id,
                "student_name": student_user.name,
                "student_email": student_user.email,
                "college": student.college,
                "cgpa": student.cgpa,
                "skills": student.skills,
                "resume": student.resume,
                "status": app.status,
                "applied_at": app.applied_at,
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@application.patch("/<int:application_id>")
@jwt_required()
def update_application_status(application_id):
    try:
        user = User.query.get(int(get_jwt_identity()))

        if not user or user.role != "company":
            return jsonify({"error": "Unauthorized"}), 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        application_obj = Application.query.get(application_id)

        if not application_obj:
            return jsonify({"error": "Application not found"}), 404

        drive = PlacementDrive.query.get(application_obj.drive_id)

        if drive.company_id != company.id:
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json() or {}

        allowed_status = [
            "applied",
            "in-touch",
            "shortlisted",
            "rejected",
        ]

        status = data.get("status")

        if status not in allowed_status:
            return jsonify({"error": "Invalid status"}), 400

        application_obj.status = status

        db.session.commit()

        return jsonify({
            "message": "Application status updated successfully"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
