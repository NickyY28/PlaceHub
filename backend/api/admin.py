import os

from celery.result import AsyncResult
from flask import (
    Blueprint,
    jsonify,
    request,
    send_from_directory,
    current_app,
)
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload

from extensions import db, celery
from models import (
    User,
    CompanyProfile,
    StudentProfile,
    PlacementDrive,
    Application,
)
from tasks.admin_tasks import generate_monthly_report
from utils.decorators import admin_required


admin = Blueprint("admin", __name__)


# =========================================================
# Dashboard
# =========================================================

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


# =========================================================
# Users
# =========================================================

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

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# Companies
# =========================================================

@admin.get("/companies")
@jwt_required()
@admin_required
def get_companies(user):

    try:

        companies = CompanyProfile.query.options(
            joinedload(CompanyProfile.user)
        ).all()

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
                    "status": c.approval_status,
                }
                for c in companies
            ]
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# Students
# =========================================================

@admin.get("/students")
@jwt_required()
@admin_required
def get_students(user):

    try:

        students = StudentProfile.query.options(
            joinedload(StudentProfile.user)
        ).all()

        return jsonify({
            "students": [
                {
                    "id": s.id,
                    "name": s.user.name,
                    "email": s.user.email,
                    "is_blocked": s.user.is_blocked,
                    "college": s.college,
                    "cgpa": s.cgpa,
                    "skills": s.skills,
                }
                for s in students
            ]
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# Drives
# =========================================================

@admin.get("/drives")
@jwt_required()
@admin_required
def get_drives(user):

    try:

        drives = PlacementDrive.query.options(
            joinedload(PlacementDrive.company)
        ).all()

        return jsonify({
            "drives": [
                {
                    "id": d.id,
                    "company": d.company.company_name,
                    "title": d.title,
                    "package": d.package,
                    "deadline": d.deadline,
                }
                for d in drives
            ]
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# Applications
# =========================================================

@admin.get("/applications")
@jwt_required()
@admin_required
def get_applications(user):

    try:

        applications = Application.query.options(
            joinedload(Application.student),
            joinedload(Application.drive),
        ).all()

        return jsonify({
            "applications": [
                {
                    "id": a.id,
                    "student": a.student.user.name,
                    "drive": a.drive.title,
                    "status": a.status,
                    "applied_at": a.applied_at,
                }
                for a in applications
            ]
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# Company Approval
# =========================================================

@admin.patch("/companies/<int:company_id>/approval")
@jwt_required()
@admin_required
def update_company_approval(user, company_id):

    try:

        data = request.get_json() or {}

        status = data.get("status")

        if status not in ["approved", "rejected"]:

            return jsonify({
                "error": "Status must be approved or rejected"
            }), 400

        company = CompanyProfile.query.get(company_id)

        if not company:

            return jsonify({
                "error": "Company not found"
            }), 404

        company.approval_status = status

        db.session.commit()

        return jsonify({
            "message": f"Company {status} successfully",
            "approval_status": company.approval_status,
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# Block User
# =========================================================

@admin.patch("/users/<int:user_id>/block")
@jwt_required()
@admin_required
def block_user(user, user_id):

    u = User.query.get(user_id)

    if not u:

        return jsonify({
            "error": "User not found"
        }), 404

    u.is_blocked = True

    db.session.commit()

    return jsonify({
        "message": "User blocked successfully"
    }), 200


# =========================================================
# Unblock User
# =========================================================

@admin.patch("/users/<int:user_id>/unblock")
@jwt_required()
@admin_required
def unblock_user(user, user_id):

    u = User.query.get(user_id)

    if not u:

        return jsonify({
            "error": "User not found"
        }), 404

    u.is_blocked = False

    db.session.commit()

    return jsonify({
        "message": "User unblocked successfully"
    }), 200


# =========================================================
# Delete User
# =========================================================

@admin.delete("/users/<int:user_id>")
@jwt_required()
@admin_required
def delete_user(user, user_id):

    u = User.query.get(user_id)

    if not u:

        return jsonify({
            "error": "User not found"
        }), 404

    db.session.delete(u)

    db.session.commit()

    return jsonify({
        "message": "User deleted successfully"
    }), 200


# =========================================================
# Delete Drive
# =========================================================

@admin.delete("/drives/<int:drive_id>")
@jwt_required()
@admin_required
def delete_drive(user, drive_id):

    drive = PlacementDrive.query.get(drive_id)

    if not drive:

        return jsonify({
            "error": "Drive not found"
        }), 404

    db.session.delete(drive)

    db.session.commit()

    return jsonify({
        "message": "Drive deleted successfully"
    }), 200


# =========================================================
# Generate Monthly Report
# =========================================================

@admin.post("/generate-monthly-report")
@jwt_required()
@admin_required
def generate_report(user):

    try:

        task = generate_monthly_report.delay()

        return jsonify({
            "message": "Monthly report generation started",
            "task_id": task.id,
        }), 202

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# Monthly Report Status
# =========================================================

@admin.get("/report-status/<task_id>")
@jwt_required()
@admin_required
def report_status(user, task_id):

    task = AsyncResult(
        task_id,
        app=celery,
    )

    if task.state == "PENDING":

        return jsonify({
            "status": "pending"
        }), 200

    if task.state == "FAILURE":

        return jsonify({
            "status": "failed",
            "error": str(task.info),
        }), 500

    if task.state == "SUCCESS":

        result = task.result

        return jsonify({
            "status": "completed",
            "filename": result["filename"],
        }), 200

    return jsonify({
        "status": task.state.lower()
    }), 200


# =========================================================
# Download Monthly Report
# =========================================================

@admin.get("/download-report/<filename>")
@jwt_required()
@admin_required
def download_report(user, filename):

    try:

        report_dir = os.path.join(
            current_app.root_path,
            "reports",
        )

        file_path = os.path.join(
            report_dir,
            filename,
        )

        if not os.path.exists(file_path):

            return jsonify({
                "error": "Report not found"
            }), 404

        return send_from_directory(
            report_dir,
            filename,
            as_attachment=True,
        )

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
